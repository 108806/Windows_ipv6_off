import sys, os
print(os.getcwd(), sys.version)
import winreg
#import ctypes Not used in this ver.
from functools import lru_cache

#This script is supposed to disable the IPV6 protocol in Windows 10 system.
#NOTE : Its functionality may be completely nulled with Win updates
#Last tested on $Microsoft Windows [Version 10.0.19042.789]

__author__ = 0x1a906
__VER__ = 0.1
__IT_IS_KNOWN__ = 'ipv6 suxxx'


#There are 2  entries we need to perform, their absoulte path in reg is :
#Computer\HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\Tcpip6
#Computer\HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\Tcpip6\Parameters
tcpip6_k1 = 'SYSTEM\\ControlSet001\\Services\\Tcpip6'
tcpip6_k2 = 'SYSTEM\\ControlSet001\\Services\\Tcpip6\\Parameters'

#This is data we need to put in the key.
val = 0xffffffff

#This is the kay that will store the data:
kName = 'DisabledComponents'

@lru_cache(maxsize=None)
def regEdit(path:str, show:bool=False):
    #show - Used only for debugging.
    #part of full registry path, without the COMPUTER/HKEY_CHOICE part,
    #because this will be passed via ConnectRegistry below:
    with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:

        showDict = {}

        for i in range(0, 16):
            with winreg.OpenKey(hkey, path,  0,
                winreg.KEY_ALL_ACCESS) as sKey:
                try:
                    contains = winreg.EnumValue(sKey, i)
                    showDict[contains[0]] = contains[1]
                except WindowsError:
                    pass

        if show: print(showDict)

        if not showDict[kName] == val:
            with winreg.CreateKey(hkey, path) as nKey:
                winreg.SetValueEx(nKey, kName, 0, winreg.REG_DWORD, val)

        else:
            print(f'{path} : {kName} : {val}')
            print('[INFO] This key already has the target value, nothing to do here.')

#EXEC CHAIN:
regEdit(tcpip6_k1)
regEdit(tcpip6_k2)
