#! /usr/bin/env python3

import json
import os
import subprocess
import sys
import threading
from typing import Union


WELCOME_MSG = """
==============================================================================
Welcome to the LLDB-DAP REPL.
This REPL allows you to start a custom lldb-dap and send DAP messages to it.

To start a custom lldb-dap, run the following command in terminal:
  > ENV_VAR1=VAL1 ./lldb_dap_repl.py /path/to/lldb-dap --arg1 val1
E.g.
  > ./lldb_dap_repl.py /opt/llvm/bin/lldb-dap --keep-alive 999

You can then send DAP messages to the lldb-dap process.
Type "help" to see all valid input.
See D72906362 for an example input sequence and corresponding DAP messages.

Press Ctrl+D to terminate the REPL and lldb-dap.
==============================================================================
"""

HELP_MSG = """You can input:
  1. A JSON object, which will be sent to lldb-dap as a DAP message.
  2. A supported command:
        help                                Print this message
  3. A supported DAP request:
        initialize                          Send a "initialize" request
        launch TARGET BUILD_DIR [CWD]       Send a "launch" request
        setBreakpoints FILE LINE            Send a "setBreakpoints" request
        configurationDone                   Send a "configurationDone" request
        threads                             Send a "threads" request
        stackTrace THREAD_ID                Send a "stackTrace" request
        scopes FRAME_ID                     Send a "scopes" request
        variables                           Send a "variables" request
        evaluate FRAME_ID EXPRESSION        Send a "evaluate" request
        disconnect                          Send a "disconnect" request
  4. Everything else will be interpreted as an LLDB command and be sent to
     lldb-dap as an "evaluate" request with the last used frame ID."""

last_frame_id = None


def print_with_separator(msg: str, separator: str) -> None:
    print(separator)
    print(msg)
    print("-" * len(separator))
    print("")


def print_response(stdout) -> None:
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
    except Exception:
        print("Stopping printing responses")
    finally:
        stdout.close()


# The return of a processor is either:
# - String. The input is processed and converted to a DAP message.
# - True. The input is processed and yielded no DAP message.
# - False. The input is not processed. Next processor will be called.
def process_as_dap_message_content(input_text: str) -> Union[str, bool]:
    # Validate the content
    try:
        json.loads(input_text)
    except json.JSONDecodeError:
        return False

    # Prepare the DAP message
    content_length = len(input_text)
    dap_message = f"Content-Length: {content_length}\r\n\r\n{input_text}"

    return dap_message


def process_as_supported_command_or_request(input_text: str) -> Union[str, bool]:
    global last_frame_id

    parts = input_text.split(" ")
    command = parts[0]

    if command == "help":
        print_with_separator(HELP_MSG, "---")
        return True
    elif command == "initialize":
        return process_as_dap_message_content(
            '{"command":"initialize","arguments":{"clientID":"vscode","clientName":"Visual Studio Code @ Meta","adapterID":"fb-lldb","pathFormat":"path","linesStartAt1":true,"columnsStartAt1":true,"supportsVariableType":true,"supportsVariablePaging":true,"supportsRunInTerminalRequest":true,"locale":"en","supportsProgressReporting":true,"supportsInvalidatedEvent":true,"supportsMemoryReferences":true,"supportsArgsCanBeInterpretedByShell":true,"supportsMemoryEvent":true,"supportsStartDebuggingRequest":true,"supportsANSIStyling":true},"type":"request","seq":1}'
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
            + '"]],"timeout":600,"type":"fb-lldb","stopOnEntry":false,"runInTerminal":false,"disableASLR":true,"disableSTDIO":false,"detachOnError":false,"terminateCommands":[],"preferLLDBCommandsInDebugConsole":true,"repeatLastLLDBCommandInDebugConsole":true,"reuseLLDBDap":false,"customThreadFormat":"${thread.name} [tid: ${thread.id%tid}]","__sessionId":"lldb_dap_repl_yyyymmdd_hhmmss_royshi"},"type":"request","seq":2}'
        )
    elif command == "setBreakpoints":
        path = parts[1]
        filename = path.split("/")[-1]
        line = int(parts[2])
        return process_as_dap_message_content(
            '{"command":"setBreakpoints","arguments":{"source":{"name":"'
            + filename
            + '","path":"'
            + path
            + '"},"lines":['
            + str(line)
            + '],"breakpoints":[{"line":'
            + str(line)
            + '}],"sourceModified":false},"type":"request","seq":3}'
        )
    elif command == "configurationDone":
        return process_as_dap_message_content(
            '{"command":"configurationDone","type":"request","seq":29}'
        )
    elif command == "threads":
        return process_as_dap_message_content(
            '{"command":"threads","type":"request","seq":51}'
        )
    elif command == "stackTrace":
        thread_id = int(parts[1])
        return process_as_dap_message_content(
            '{"command":"stackTrace","arguments":{"threadId":'
            + str(thread_id)
            + ',"startFrame":0,"levels":1},"type":"request","seq":52}'
        )
    elif command == "scopes":
        last_frame_id = frame_id = int(parts[1])
        return process_as_dap_message_content(
            '{"command":"scopes","arguments":{"frameId":'
            + str(frame_id)
            + '},"type":"request","seq":55}'
        )
    elif command == "variables":
        return process_as_dap_message_content(
            '{"command":"variables","arguments":{"variablesReference":1,"format":{"hex":false}},"type":"request","seq":56}'
        )
    elif command == "evaluate":
        last_frame_id = frame_id = int(parts[1])
        expression = " ".join(parts[2:])
        return process_as_dap_message_content(
            '{"command":"evaluate","arguments":{"expression":"'
            + expression
            + '","frameId":'
            + str(frame_id)
            + ',"context":"repl"},"type":"request","seq":59}'
        )
    elif command == "disconnect":
        return process_as_dap_message_content(
            '{"command":"disconnect","arguments":{"restart":false,"terminateDebuggee":true},"type":"request","seq":40}'
        )
    else:
        return False


def process_as_lldb_command(input_text: str) -> Union[str, bool]:
    global last_frame_id
    return process_as_supported_command_or_request(
        f"evaluate {last_frame_id} {input_text}"
    )


def repl(lldb_dap: subprocess.Popen) -> None:
    # Setup a daemon thread to process the response from lldb-dap.
    # The termination sequence is:
    # 1. The user enters EOF (Ctrl+D)
    # 2. The REPL (this script) closes the stdio to lldb-dap
    # 3. lldb-dap terminates after detecting the EOF
    # 4. The stdout_thread reads an empty content_length_line because of the closed stdout
    # 5. The stdout_thread terminates
    # Note: Since it's a daemon thread, it can be terminated before steps 4 and 5 occur, which is fine.
    stdout_thread = threading.Thread(
        target=print_response, args=[lldb_dap.stdout], daemon=True
    )
    stdout_thread.start()

    processors = [
        process_as_dap_message_content,
        process_as_supported_command_or_request,
        process_as_lldb_command,
    ]

    # REPL
    while True:
        try:
            input_text = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("Exiting")
            break

        # Go through processors one by one, until the input can be processed
        process_result = False
        for processor in processors:
            process_result = processor(input_text)
            if process_result is not False:
                break

        if process_result is False:
            # Input cannot be processed
            print("Invalid input")
            continue

        # Send the DAP message to lldb-dap
        if type(process_result) is str:
            dap_message = process_result
            print_with_separator(dap_message, "-->")
            lldb_dap.stdin.write(dap_message)
            lldb_dap.stdin.flush()


def terminate_lldb_dap(lldb_dap: subprocess.Popen) -> None:
    # Try to close lldb-dap gracefully
    try:
        lldb_dap.stdin.close()
        lldb_dap.wait()
    except KeyboardInterrupt:
        # Closing the above stdin will sometimes cause KeyboardInterrupt
        pass


def start_lldb_dap_and_repl() -> None:
    if len(sys.argv) < 2:
        return

    lldb_dap_command_and_args = sys.argv[1:]

    with subprocess.Popen(
        lldb_dap_command_and_args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    ) as lldb_dap:
        try:
            repl(lldb_dap)
        finally:
            terminate_lldb_dap(lldb_dap)


def main() -> None:
    print(WELCOME_MSG)
    print("help")
    print_with_separator(HELP_MSG, "---")

    start_lldb_dap_and_repl()


if __name__ == "__main__":
    main()
