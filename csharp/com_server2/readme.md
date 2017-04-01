# CSharp COM-service & CPP COM-client tutorial
source code and instruction summary
https://msdn.microsoft.com/zh-tw/library/aa288456(v=vs.71).aspx
command lines summary
https://msdn.microsoft.com/en-us/library/t9yw5271(v=vs.90).aspx

complex tutorial (not try yet)
https://msdn.microsoft.com/en-us/library/aa645736(v=vs.71).aspx#vcwlkcominteroppart1cclienttutorialanchor1

## summary of files convention and usage

*.cs --(cl.exe /target:library)--> *.dll --(tlbexp.exe /out:xxx.tlb0 --> *.tlb

*.ild --(midl.exe )--> *.tlb  (python's comtypes module tutorial)
*.tlb --(tlbimp.exe /out:dll) --> *.dll

*.dll, il dll --(regasm.exe /tlb:xxx.tlb)--> register COM and xxx.tlb
dos>C:\Windows\Microsoft.NET\Framework\v4.0.30319\regasm.exe CSharpServer.dll /tlb:CSharpServer.tlb



## tlb imp (tlbimpo.exe, Type Library to Assembly Converter)
tlbimp c:\winnt\system32\quartz.dll /out:QuartzTypeLib.dll 
- tlbimp is a Type Library to Assembly Converter

## il dasm (ildasm.exe)
location
C:\Program Files (x86)\Microsoft SDKs\Windows\v8.0A\bin\NETFX 4.0 Tools

check a .NET's dll files
Ildasm QuartzTypeLib.dll

use it with csc compiling
csc xxx.c /R:QuartzTypeLib.dll


