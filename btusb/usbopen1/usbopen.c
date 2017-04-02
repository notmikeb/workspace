#include <windows.h>
#include <stdio.h>

#include <windows.h>   
#include <winioctl.h>   
#include <io.h>   
#include <stdlib.h>   
#include <stdio.h>   
#include <assert.h>   
#include <string.h>   
   
//#define PKT_DUMP   
   
#define CSRBC01_IOCTL_INDEX 0x0000   
   
#define IOCTL_CSRBC01_SEND_HCI_COMMAND  CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_GET_HCI_EVENT CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+1, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_GET_VERSION   CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+2, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_GET_DRIVER_NAME   CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+3, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_GET_CONFIG_DESCRIPTOR CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+4, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_GET_DEVICE_DESCRIPTOR CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+5,\   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_RESET_DEVICE  CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+6,\   
                    METHOD_BUFFERED,\   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_RESET_PIPE    CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+7,\   
                    METHOD_BUFFERED,\   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_BLOCK_HCI_EVENT   CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+12, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_BLOCK_HCI_DATA    CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+13, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_SEND_CONTROL_TRANSFER CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+14,\   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_SELECT_ALTERNATE_INTERFACE CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+15, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_START_SCO_DATA    CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+16, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_SEND_SCO_DATA CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+17, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define IOCTL_CSRBC01_RECV_SCO_DATA CTL_CODE(FILE_DEVICE_UNKNOWN, \   
                    CSRBC01_IOCTL_INDEX+18, \   
                    METHOD_BUFFERED, \   
                    FILE_ANY_ACCESS)   
   
#define BCCMD_GETREQ    0x0000   
#define BCCMD_GETRESP   0x0001   
#define BCCMD_SETREQ    0x0002   
   
/* these bits can be or'ed */   
#define PSSTORE_DEFAULT 0x0000 /* on write: psi,psram; on read: psram,psi,psf,psrom */   
#define PSSTORE_PSI     0x0001   
#define PSSTORE_PSF     0x0002   
#define PSSTORE_PSROM   0x0004   
#define PSSTORE_PSRAM   0x0008   
   
#define PSKEY_BDADDR                    0x0001   
#define PSKEY_HOSTIO_UART_PS_BLOCK      0x0191   
#define PSKEY_HOST_INTERFACE            0x01F9   
   
#define PSKEY_DEEP_SLEEP_STATE          0x0229   
#define PSKEY_DEEP_SLEEP_WAKE_CTS       0x023C   
#define PSKEY_UART_SLEEP_TIMEOUT        0x0222   
#define PSKEY_HOSTIO_UART_RESET_TIMEOUT 0x01A4   
#define PSKEY_HOSTIO_BREAK_POLL_PERIOD  0x01AD   
#define PSKEY_WD_PERIOD                 0x01F8   
#define PSKEY_WD_TIMEOUT                0x01F7   
#define PSKEY_MKT_TASK_ACTIVE           0x01FA   
#define PSKEY_DEBUG_TASK_PERIOD         0x0218   
   
#ifndef uint16   
#define uint16 USHORT   
#endif   
   
/* 18 bytes -long device descriptor */   
typedef struct {   
    UCHAR type;   
    UCHAR length;   
    USHORT bcdUSB;   
    UCHAR bDeviceClass;   
    UCHAR bDeviceSubClass;   
    UCHAR bDeviceProtocol;   
    UCHAR bMaxPacketSize0;   
    USHORT idVendor;   
    USHORT idProduct;   
    USHORT bcdDevice;   
    UCHAR iManufacturer;   
    UCHAR iProduct;   
    UCHAR iSerialNumber;   
    UCHAR bNumConfigurations;   
} dev_desc;   

dev_desc g_desc;
unsigned long g_desc_written = 0;
/////

HANDLE g_hci_handle = INVALID_HANDLE_VALUE;

#if 0 
#define debugf
#else
#define debugf printf 
#endif

void close_connection_on_error(char *fn);

int btusb_init(){
int status; 

if( g_hci_handle != INVALID_HANDLE_VALUE ){
debugf("already open as %d\n", g_hci_handle);

}else{
g_hci_handle = CreateFile("\\\\.\\CSR0", GENERIC_READ | GENERIC_WRITE, 0, 0, OPEN_EXISTING, 0, 0 );
if (g_hci_handle == INVALID_HANDLE_VALUE) 
{ 
printf ("Cannot open %d\r\n", GetLastError());
return 0;
}

    memset(&g_desc, 0, sizeof(g_desc));   
   
    status = DeviceIoControl(g_hci_handle,   
                            IOCTL_CSRBC01_GET_DEVICE_DESCRIPTOR,   
                            0,   
                            0,   
                            &g_desc,   
                            sizeof(g_desc), /* must be 18 */   
                            &g_desc_written,   
                            0);   
   
    if (!status)   
        close_connection_on_error ("IOCTL_CSRBC01_GET_DEVICE_DESCRIPTOR");  
    }

return 1;
}

int btusb_deinit(){

if( g_hci_handle != INVALID_HANDLE_VALUE ){
debugf("close %d done\n", g_hci_handle);
CloseHandle(g_hci_handle);
g_hci_handle = INVALID_HANDLE_VALUE;
g_desc_written = 0;
}

return 1;

}

void close_connection_on_error(char *fn)   
{   
    printf("ERROR: %s, error#%d", fn, GetLastError());   
   
    btusb_deinit();  
}   

/* should return the number of bytes written, but it never does? */   
int send_hci_command(void *buffer, unsigned long length)   
{   
    int status = 0;   
    unsigned long written = 0;  
    if( 0 == btusb_init() ){
        return 0;
    } 
   
    status = DeviceIoControl( g_hci_handle ,
                            IOCTL_CSRBC01_SEND_HCI_COMMAND,   
                            buffer,   
                            length,   
                            0,   
                            0,   
                            &written,   
                            NULL);
   
    if (!status)   
        close_connection_on_error ("send_hci_command");   
   
    return written;   
}   
   
// hci event max is ?. caution: this is non-blocking
int get_hci_event(void *buffer)   
{   
    int status = 0;   
    unsigned long written = 0;   
   
    if( 0 == btusb_init() ){
        return 0;
    } 
   
    status = DeviceIoControl(g_hci_handle ,
                            IOCTL_CSRBC01_GET_HCI_EVENT,   
                            0,   
                            0,   
                            buffer,   
                            16,         /* length is always 16 */   
                            &written,   
                            NULL);   
       
    if (!status)   
        close_connection_on_error ("send_hci_command");   
   
    return written;   
}   

int main(){
debugf("useless main() , build shared libraray instead\n");
btusb_init();
btusb_deinit();
return 0;
}