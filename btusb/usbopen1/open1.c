#include <windows.h>
#include <stdio.h>

    int main()
    {
        HANDLE hComm;

        const WCHAR FileFullPath[] = {L"COM1"} ;


        hComm = CreateFile( (LPCTSTR)FileFullPath,
                            GENERIC_READ | GENERIC_WRITE,
                            0,
                            0,
                            OPEN_EXISTING,
                            FILE_FLAG_OVERLAPPED,
                            0);

        if (hComm == INVALID_HANDLE_VALUE) {
            printf("Invalid value: %d\r\n", GetLastError());
        }
    }