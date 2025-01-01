// script used to get keycard on tryhackme room T5: An Avalanche of Web Apps part of Advent of Cyber '24 Side Quest.
// Script with Assistance from ChatpGPT and Claudi AI
// youtube video walk through: https://www.youtube.com/watch?v=AL3E5s38Z5w

Interceptor.attach(Module.findExportByName(null, "_Z14create_keycardPKc"), {
  onEnter: function(args) {
    console.log("[+] Intercepting _Z14create_keycardPKc");
    // Make sure the password is correct
    this.arg0 = args[0];
    
    // Set the integer arguments that we see in the logs
    args[1] = ptr(9);
    args[2] = ptr(72);
    
    try {
      const input = Memory.readUtf8String(args[0]);
      console.log("[+] Input: " + input);
    } catch(e) {
      console.log("[+] Could not read input string");
    }
  },
  onLeave: function(retval) {
    console.log("[+] Original return value: " + retval);
    // Force success return value
    retval.replace(1);
    
    // Try to trigger the file creation by calling the function again with the same args
    const func = new NativeFunction(Module.findExportByName(null, "_Z14create_keycardPKc"), 'int', ['pointer', 'int', 'int']);
    const result = func(this.arg0, 9, 72);
    console.log("[+] Additional call result: " + result);
  }
});

// First, identify the correct library
const libraryName = "libaocgame.so";

try {
    // Get function from the correct library
    const functionAddress = Module.findExportByName(libraryName, "_Z14create_keycardPKc");
    console.log("[+] Function found at: " + functionAddress);
    
    // Create function wrapper with correct signature (just needs string pointer)
    const createKeycard = new NativeFunction(functionAddress, 'int', ['pointer']);
    
    // Allocate memory for correct string (23 chars)
    const stringMemory = Memory.allocUtf8String("one_two_three_four_five");
    console.log("[+] Allocated string at: " + stringMemory);
    
    // Call function directly
    const result = createKeycard(stringMemory);
    console.log("[+] Function call result: " + result);
    
} catch (error) {
    console.log("[-] Error: " + error.message);
}
