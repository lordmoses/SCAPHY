import pefile

pe = pefile.PE("C:\Program Files (x86)\MHJ-Software\WinSPS-S7-V6\ws7v6.exe")

pe.print_info()