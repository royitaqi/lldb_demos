import Foundation

class HelloWorld {
    // Define a stored property
    var greeting: String
    
    // Initialize the property when creating an instance
    init(greeting: String) {
        self.greeting = greeting
    }
    
    // Define a method to print the greeting
    func sayHello() {
        print(greeting)
    }
}
