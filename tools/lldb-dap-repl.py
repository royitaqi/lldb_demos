#! /usr/bin/env python3

import json
import os
import socket
import subprocess
import sys
import threading
from datetime import datetime
from time import sleep
from typing import cast, Callable, Union


WELCOME_MSG = """
==============================================================================
Welcome to the LLDB-DAP REPL.
This REPL allows you to interactive with a lldb-dap process and send DAP
messages to it.

To start a custom lldb-dap process:
  > ENV_VAR1=VAL1 ./lldb_dap_repl.py run /path/to/lldb-dap --arg1 val1
E.g.
  > ./lldb_dap_repl.py run /opt/llvm/bin/lldb-dap --keep-alive 999

To connect to an existing lldb-dap process:
  > ./lldb_dap_repl.py connect /path/to/lldb-dap port
E.g.
  > ./lldb_dap_repl.py connect /opt/llvm/bin/lldb-dap 65337

You can then send DAP messages to the lldb-dap process.
Type "help" to see all valid input.

Press Ctrl+D to terminate the REPL and lldb-dap.
==============================================================================
"""

HELP_MSG = """You can input:
  1. A JSON object, which will be sent to lldb-dap as a DAP message.
  2. A supported command:
        help                                Print this message
        autoTerminate                       Terminate lldb-dap process after
                                            the "terminated" event is received
        EOF                                 Close the stdin of lldb-dap process
  3. A supported DAP request:
        initialize                          Send a "initialize" request
        launch TARGET BUILD_DIR [CWD]       Send a "launch" request
        attach PID|PROGRAM                  Send a "attach" request
        setBreakpoints FILE LINE            Send a "setBreakpoints" request
        configurationDone                   Send a "configurationDone" request
        threads                             Send a "threads" request
        stackTrace THREAD_ID                Send a "stackTrace" request
        scopes FRAME_ID                     Send a "scopes" request
        variables                           Send a "variables" request
        evaluate FRAME_ID|None LLDB_CMD     Send a "evaluate" request
        continue [THREAD_ID]                Send a "continue" request
        disconnect                          Send a "disconnect" request
  4. A file (path), which contains one or more inputs, one per line.
  5. Everything else will be interpreted as an LLDB command and be sent to
     lldb-dap as an "evaluate" request with the latest frame ID.

In all input, the following macros are supported:
        {DATE}      The current date in the format YYYY-MM-DD
        {TIME}      The current time in the format HH:MM
"""


lldb_dap = None
lldb_dap_stdin = None
lldb_dap_stdout = None

last_frame_id = None
last_thread_id = None
auto_terminate = False


def try_get_psutil():
    try:
        import psutil
        return psutil
    except:
        return None


def try_get_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return None


# Override log() so that it will print a timestamp first.
def log(*args, **kwargs):
    ts = datetime.now().strftime("%H:%M:%S")
    print(ts, *args, **kwargs)


def print_with_separator(msg: str, separator: str) -> None:
    log(separator)
    log(msg)
    log("-" * len(separator))
    log("")


def print_dap_status() -> None:
    global lldb_dap
    if lldb_dap is None:
        log("lldb-dap is not initialized. Won't monitor its status.")
        return

    exit_code = lldb_dap.wait()
    log("lldb-dap has terminated with exit code", exit_code)


def print_response() -> None:
    global lldb_dap_stdout
    assert lldb_dap_stdout is not None, "lldb_dap_stdout is not initialized"

    stdout = lldb_dap_stdout
    try:
        while not stdout.closed:
            # First line should be "Content-Length: LENGTH"
            content_length_line = stdout.readline().strip()
            if content_length_line == "":
                # This usually indicates a closed stream and the termination of lldb-dap
                break
            if not content_length_line.startswith("Content-Length: "):
                raise RuntimeError(
                    f"Invalid response. Missing Content-Length: '{content_length_line}'"
                )

            # An empty line should follow
            next_line = stdout.readline().strip()
            if next_line != "":
                raise RuntimeError(
                    f"Invalid response - next line should be empty: '{next_line}'"
                )

            # Read the actual message content
            content_length = int(content_length_line[16:])
            content = stdout.read(content_length)

            # Print the DAP message
            dap_message = f"Content-Length: {content_length}\r\n\r\n{content}"
            print_with_separator(dap_message, "<--")

            # Update global state
            json_content = json.loads(content)
            if json_content["type"] == "event":
                if json_content["event"] == "stopped":
                    global last_thread_id
                    last_thread_id = int(json_content["body"]["threadId"])
                elif json_content["event"] == "terminated":
                    global auto_terminate
                    if auto_terminate:
                        terminate_lldb_dap()
    except Exception:
        pass
    finally:
        stdout.close()
    log("lldb-dap output stream has been closed")


type actionableFunc = Callable[[], None]
type actionableDapMessage = str
type actionable = Union[actionableDapMessage, actionableFunc]

# The return of a processor is either:
# - String. The input is processed and converted to a DAP message.
# - True. The input is processed and yielded no DAP message.
# - False. The input is not processed. Next processor will be called.
def process_as_dap_message_content(input_text: str, should_succeed: bool = False) -> Union[list[actionable], None]:
    # Validate the content
    try:
        json.loads(input_text)
    except json.JSONDecodeError as e:
        if should_succeed:
            raise ValueError("Invalid JOSN: " + input_text, e)
        else:
            return None

    # Replace predefined macros
    input_text = input_text.replace(
        "{DATE}", datetime.now().strftime("%Y-%m-%d")
    ).replace(
        "{TIME}", datetime.now().strftime("%H:%M")
    )

    # Prepare the DAP message
    content_length = len(input_text)
    dap_message = f"Content-Length: {content_length}\r\n\r\n{input_text}"

    return [dap_message]


def process_as_supported_command_or_request(input_text: str) -> Union[list[actionable], None]:
    global last_frame_id
    global last_thread_id

    parts = input_text.split(" ")
    command = parts[0]
    # log("Processing command: [" + command + "]")

    if command == "help":
        def print_help():
            print_with_separator(HELP_MSG, "---")
        return [print_help]
    elif command == "autoTerminate":
        def flip_auto_terminate():
            global auto_terminate
            auto_terminate = not auto_terminate
            log("autoTerminate is", "on" if auto_terminate else "off")
            log("")
        return [flip_auto_terminate]
    elif command == "EOF":
        return [close_lldb_dap_input_stream]
    elif command == "initialize":
        return process_as_dap_message_content(
            '{"command":"initialize","arguments":{"clientID":"vscode","clientName":"Visual Studio Code @ Meta","adapterID":"fb-lldb","pathFormat":"path","linesStartAt1":true,"columnsStartAt1":true,"supportsVariableType":true,"supportsVariablePaging":true,"supportsRunInTerminalRequest":true,"locale":"en","supportsProgressReporting":true,"supportsInvalidatedEvent":true,"supportsMemoryReferences":true,"supportsArgsCanBeInterpretedByShell":true,"supportsMemoryEvent":true,"supportsStartDebuggingRequest":true,"supportsANSIStyling":true},"type":"request","seq":1}',
            True,
        )
    elif command == "launch":
        target = parts[1]
        build_dir = parts[2]
        cwd = parts[3] if len(parts) >= 4 else os.getcwd()
        return process_as_dap_message_content(
            '{"command":"launch","arguments":{"isDebugWithoutBuild":true,"useFocusedBreakpoints":false,"name":"lldb-dap REPL","args":[],"client":"lldb_dap_repl.py","cwd":"'
            + cwd
            + '","debuggerRoot":"'
            + cwd
            + '","enableSingleStoppedEvent":false,"enableSingleThreadStepping":false,"env":[],"initCommands":["script import importlib","script import importlib.util","script importlib.import_module(\'fblldbinit\') if importlib.util.find_spec(\'fblldbinit\') else None","settings set symbols.load-on-demand true"],"postRunCommands":["run-to-binary-entry"],"preRunCommands":[],"program":"'
            + target
            + '","request":"launch","sourceMap":[[".","'
            + build_dir
            + '"]],"timeout":600,"type":"fb-lldb","stopOnEntry":false,"runInTerminal":false,"disableASLR":true,"disableSTDIO":false,"detachOnError":false,"terminateCommands":[],"preferLLDBCommandsInDebugConsole":true,"repeatLastLLDBCommandInDebugConsole":true,"reuseLLDBDap":false,"customThreadFormat":"${thread.name} [tid: ${thread.id%tid}]","__sessionId":"lldb_dap_repl_yyyymmdd_hhmmss_royshi"},"type":"request","seq":2}',
            True,
        )
    elif command == "attach":
        # Example of attach request:
        # - DAP messages: P1928554145
        # - Attach request: P1928555816
        pid = program = None
        try:
            pid = int(parts[1])
        except ValueError:
            program = parts[1]
        return process_as_dap_message_content(
            '{"command":"attach","arguments":{"name":"lldb-dap REPL","request":"attach",'
            + ('"pid":' + str(pid) if program is None else '"program":"' + program + '"')
            + ',"initCommands":["script import importlib","script import importlib.util","script importlib.import_module(\'fblldbinit\') if importlib.util.find_spec(\'fblldbinit\') else None","settings set symbols.load-on-demand true"]},"type":"request","seq":2}',
            True,
        )
    elif command == "setBreakpoints":
        path = parts[1]
        filename = path.split("/")[-1]
        lines = parts[2:]
        return process_as_dap_message_content(
            '{"command":"setBreakpoints","arguments":{"source":{"name":"'
            + filename
            + '","path":"'
            + path
            + '"},"lines":['
            + ','.join(lines)
            + '],"breakpoints":['
            + ','.join(['{"line":' + line + '}' for line in lines])
            + '],"sourceModified":false},"type":"request","seq":3}',
            True,
        )
    elif command == "configurationDone":
        return process_as_dap_message_content(
            '{"command":"configurationDone","type":"request","seq":29}',
            True,
        )
    elif command == "threads":
        return process_as_dap_message_content(
            '{"command":"threads","type":"request","seq":51}',
            True,
        )
    elif command == "stackTrace":
        thread_id = int(parts[1])
        return process_as_dap_message_content(
            '{"command":"stackTrace","arguments":{"threadId":'
            + str(thread_id)
            + ',"startFrame":0,"levels":1},"type":"request","seq":52}',
            True,
        )
    elif command == "scopes":
        last_frame_id = frame_id = int(parts[1])
        return process_as_dap_message_content(
            '{"command":"scopes","arguments":{"frameId":'
            + str(frame_id)
            + '},"type":"request","seq":55}',
            True,
        )
    elif command == "variables":
        return process_as_dap_message_content(
            '{"command":"variables","arguments":{"variablesReference":1,"format":{"hex":false}},"type":"request","seq":56}',
            True,
        )
    elif command == "evaluate":
        if parts[1] == "None":
            frame_id = None
        else:
            last_frame_id = frame_id = int(parts[1])
        expression = " ".join(parts[2:])
        return process_as_dap_message_content(
            '{"command":"evaluate","arguments":{"expression":"'
            + expression
            + '",'
            + ('"frameId":' + str(frame_id) + ',' if frame_id is not None else "")
            + '"context":"repl"},"type":"request","seq":59}',
            True,
        )
    elif command == "continue":
        thread_id = int(parts[1]) if len(parts) > 1 else last_thread_id
        return process_as_dap_message_content(
            '{"command":"continue","arguments":{"threadId":'
            + str(thread_id)
            + '},"type":"request","seq":21}',
            True,
        )
    elif command == "disconnect":
        return process_as_dap_message_content(
            '{"command":"disconnect","arguments":{"restart":false,"terminateDebuggee":false},"type":"request","seq":40}',
            True,
        )
    else:
        return None


def process_as_file(input_text: str) -> Union[list[actionable], None]:
    if not os.path.exists(input_text):
        return None
    output = []
    with open(input_text) as f:
        lines = f.readlines()
    for line in lines:
        process_result = process(line.strip())
        if process_result is None:
            return None
        output += process_result
    return output


def process_as_lldb_command(input_text: str) -> Union[list[actionable], None]:
    global last_frame_id
    return process_as_supported_command_or_request(
        f"evaluate {last_frame_id} {input_text}"
    )


processors = [
    process_as_dap_message_content,
    process_as_supported_command_or_request,
    process_as_file,
    process_as_lldb_command,
]

def process(input_text: str) -> Union[list[actionable], None]:
    for processor in processors:
        process_result = processor(input_text)
        if process_result is not None:
            return process_result
    return None


def repl() -> None:
    global lldb_dap_stdin
    assert lldb_dap_stdin is not None, "lldb_dap_stdin is not initialized"

    # Setup a daemon thread to process the response from lldb-dap.
    # The termination sequence is:
    # 1. The user enters EOF (Ctrl+D)
    # 2. The REPL (this script) closes the stdio to lldb-dap
    # 3. lldb-dap terminates after detecting the EOF
    # 4. The stdout_thread reads an empty content_length_line because of the closed stdout
    # 5. The stdout_thread terminates
    # Note: Since it's a daemon thread, it can be terminated before steps 4 and 5 occur, which is fine.
    stdout_thread = threading.Thread(
        target=print_response, args=[], daemon=True
    )
    stdout_thread.start()

    status_thread = threading.Thread(
        target=print_dap_status, args=[], daemon=True
    )
    status_thread.start()

    # REPL
    while True:
        try:
            input_text = input().strip()
            print("^" * len(input_text))
        except (EOFError):
            terminate_lldb_dap()
            break
        except (KeyboardInterrupt):
            log("Exiting")
            break

        # Go through processors one by one, until the input can be processed
        process_result = process(input_text)

        if process_result is None:
            # Input cannot be processed
            log("Invalid input")
            continue

        # Send the DAP messages to lldb-dap
        for actionableItem in process_result:
            if type(actionableItem) == str:
                dap_message = cast(actionableDapMessage, actionableItem)
                print_with_separator(dap_message, "-->")
                lldb_dap_stdin.write(dap_message)
                lldb_dap_stdin.flush()
            else:
                func = cast(actionableFunc, actionableItem)
                func()


def close_lldb_dap_input_stream() -> None:
    global lldb_dap_stdin
    assert lldb_dap_stdin is not None, "lldb_dap_stdin is not initialized"

    log("Closing lldb-dap's input stream")
    lldb_dap_stdin.close()


def terminate_lldb_dap() -> None:
    global lldb_dap
    if lldb_dap is None:
        log("lldb-dap is not initialized. Won't terminate it.")
        return

    try:
        if lldb_dap.is_running():
            close_lldb_dap_input_stream()

        # Wait for lldb-dap to terminate
        lldb_dap.wait()
    except KeyboardInterrupt:
        log("Wasn't able to confirm lldb-dap termination")


def start_lldb_dap_and_repl() -> None:
    if len(sys.argv) < 3:
        return

    mode = sys.argv[1]
    if mode == "help" or mode == "--help" or mode == "-h":
        log(HELP_MSG)
        return

    global lldb_dap
    global lldb_dap_stdin
    global lldb_dap_stdout
    if mode == "run":
        lldb_dap_command_and_args = sys.argv[2:]
        lldb_dap = subprocess.Popen(
            lldb_dap_command_and_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        lldb_dap_stdin = lldb_dap.stdin
        lldb_dap_stdout = lldb_dap.stdout
        pid = lldb_dap.pid
        lldb_dap = try_get_psutil().Process(pid)
    elif mode == "connect":
        # Find the lldb-dap process
        target = sys.argv[2]
        if try_get_psutil() is None:
            log("psutil is not installed. Cannot find the lldb-dap process.")
        else:
            candidates = []
            for proc in psutil.process_iter(['cmdline', 'exe']):
                proc_cmdline = proc.info['cmdline']
                proc_exe = proc.info['exe']
                if proc_cmdline is not None and len(proc_cmdline) > 1 and proc.info['cmdline'][0] == target:
                    candidates.append(proc)
                    break
                if proc_exe == target:
                    candidates.append(proc)
                    break
            if len(candidates) == 0:
                log("Could not find lldb-dap process")
                return
            elif len(candidates) > 1:
                log("Found multiple lldb-dap processes:")
                for idx, proc in enumerate(candidates):
                    log(f"{idx} - ({lldb_dap.pid}) {lldb_dap.cmdline()}")
                idx = input(f"Which one do you want to connect to [0-{len(candidates) - 1}]?")
                lldb_dap = candidates[int(idx)]
            else:
                lldb_dap = candidates[0]
            log(f"Found lldb-dap process: ({lldb_dap.pid}) {lldb_dap.cmdline()}")

        # Connect to the port
        port = int(sys.argv[3])
        log(f"Connecting to lldb-dap server: port {port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", port))

        stream = s.makefile('rw')
        lldb_dap_stdin = stream
        lldb_dap_stdout = stream
        log(f"Connected to lldb-dap process on port {port}")

    try:
        repl()
    except (KeyboardInterrupt):
        pass
    finally:
        terminate_lldb_dap()


def main() -> None:
    log(WELCOME_MSG)
    log("help")
    print_with_separator(HELP_MSG, "---")

    start_lldb_dap_and_repl()


if __name__ == "__main__":
    main()
