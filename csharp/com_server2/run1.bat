echo "https://msdn.microsoft.com/en-us/library/aa645738(v=vs.71).aspx"
csc /target:library CSharpServer.cs
C:\Windows\Microsoft.NET\Framework\v4.0.30319\regasm.exe CSharpServer.dll /tlb:CSharpServer.tlb