// http://read.pudn.com/downloads107/sourcecode/comm/wireless/442791/usb2uart/usb2uart.c__.htm
/*  
 * written by albertr, (c) 2004  
 *  
 * Not a production quality code!  
 * Use with causion, it can kill your CSR module.  
 *   
 * For examples on using CSR USB driver, please see  
 * "BlueCore USB Kernel Device Driver Interface (bcore-an-013Pa).pdf"  
 * which is a part of CSR USB driver download at:  
 * http://www.csrsupport.com/document.php?did=454&path=72  
 *  
 */   
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
   
   
static uint16 bccmd_seq = 0x0000;               /* BCCMD sequence number */   
static HANDLE handle = INVALID_HANDLE_VALUE;   
   
void close_connection_on_error(char *fn)   
{   
    LPVOID lpMsgBuf;   
   
    FormatMessage(    
                    FORMAT_MESSAGE_ALLOCATE_BUFFER |    
                    FORMAT_MESSAGE_FROM_SYSTEM |    
                    FORMAT_MESSAGE_IGNORE_INSERTS,   
                    NULL,   
                    GetLastError(),   
                    MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),   
                    (LPTSTR) &lpMsgBuf,   
                    0,   
                    NULL    
    );   
   
    printf("ERROR: %s, error#%d:%s", fn, GetLastError(), lpMsgBuf);   
    LocalFree( lpMsgBuf );   
   
    if (handle != INVALID_HANDLE_VALUE)   
        CloseHandle(handle);   
   
    exit(1);   
}   
   
   
/* should return the number of bytes written, but it never does? */   
int send_hci_command(void *buffer, unsigned long length)   
{   
    int status = 0;   
    unsigned long written = 0;   
   
    status = DeviceIoControl(handle,   
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
   
int get_hci_event(void *buffer)   
{   
    int status;   
    unsigned long written;   
   
    status = DeviceIoControl(handle,   
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
   
/* read length of pfkey from the persistent store, the key should exist */   
static uint16 pfkey_len(uint16 pfkey)   
{   
    uint16 bccmd_req, bccmd_varid, bccmd_len, pskey_len, psstore;   
    unsigned char buf[258];   
    int len = 0, chunk = 0;   
   
    bccmd_req = BCCMD_GETREQ;   
    psstore = PSSTORE_DEFAULT;   
       
    bccmd_seq++;   
    bccmd_varid = 0x3006;           /* varid: PS value size */   
    bccmd_len = 9;                  /* minimum possible length, one uint16 is wasted */   
    pskey_len = 0x0000;   
   
    memset(&buf, 0, sizeof(buf));   
   
    /* need to construct a hand-crafted HCI cmd pkt */   
    buf[0] = 0x00; buf[1] = 0xFC;   /* OGF = 0x3F & OCF = 0x00 */   
   
    buf[2] = bccmd_len * 2 + 1;     /* pkt len - 3 */   
   
    buf[3] = 0xC2;                  /* payload descriptor: last frag =1;   
                                    first frag = 1; channel = 2 */   
   
    buf[4] = bccmd_req & 0xFF; buf[5] = bccmd_req >> 8;   
   
    buf[6] = bccmd_len & 0xFF; buf[7] = bccmd_len >> 8;   
   
    buf[8]  = bccmd_seq & 0xFF; buf[9] = bccmd_seq >> 8;   
   
    buf[10] = bccmd_varid & 0xFF; buf[11] = bccmd_varid >> 8;   
   
    buf[12] = 0x00; buf[13] = 0x00; /* status */   
   
    buf[14] = pfkey & 0xFF; buf[15] = pfkey >> 8;   
       
    buf[16] = pskey_len & 0xFF; buf[17] = pskey_len >> 8;   
   
    buf[18] = psstore & 0xFF; buf[19] = psstore >> 8;   
   
    /*  FIXME: IOCTL_CSRBC01_SEND_HCI_COMMAND doesn't return the number of bytes written? */   
    send_hci_command (&buf, buf[2] + 3);   
   
#ifdef PKT_DUMP   
    printf("HCI cmd[%d]: ", buf[2] + 3);   
    for (chunk=0; chunk != buf[2] + 3; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    /* not really efficient, but who cares? */   
    while (!(chunk = get_hci_event (&buf)))   
        Sleep(10);   
       
    if (chunk == 1)                 /* too short to read packet length */   
    {      
        while (!(chunk = get_hci_event (&buf[1])))   
            Sleep(10);   
        chunk++;   
    }   
   
    for (len = chunk; len != buf[1] + 2; len = len + chunk)   
    {   
        while (!(chunk = get_hci_event (&buf[len])))   
            Sleep(10);   
    }   
   
#ifdef PKT_DUMP   
    printf("Event  [%d]:    ", len);   
    for (chunk=0; chunk!=len; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    if (buf[0] != 0xFF)         /* manuf-specific HCI event */   
        close_connection_on_error ("invalid packet received");   
   
    if (buf[1] != 9 * 2 + 1)   
        close_connection_on_error ("hci event has invalid length");   
   
    if (buf[2] != 0xC2)         /* payload descriptor */   
        close_connection_on_error ("invalid payload descriptor");   
       
    if ((buf[3] + (buf[4] << 8)) != BCCMD_GETRESP)   
        close_connection_on_error ("!= GETRESP");   
   
    if ((buf[5] + (buf[6] << 8)) != 9)   
        close_connection_on_error ("invalid length");   
   
    if ((buf[7] + (buf[8] << 8)) != bccmd_seq)   
        close_connection_on_error ("invalid sequence number");   
   
    if ((buf[9] + (buf[10] << 8)) != bccmd_varid)   
        close_connection_on_error ("invalid varid");   
   
    switch  (buf[11] + (buf[12] << 8))   
    {   
        case 0x0000:   
            /* OK status, continue */   
            break;   
        case 0x0001:   
            close_connection_on_error ("status NO_SUCH_VARID");   
            break;   
        case 0x0002:   
            close_connection_on_error ("status TOO_BIG");   
            break;   
        case 0x0003:   
            close_connection_on_error ("status NO_VALUE");   
            break;   
        case 0x0004:   
            close_connection_on_error ("status BAD_REQ");   
            break;   
        case 0x0005:   
            close_connection_on_error ("status NO_ACCESS");   
            break;   
        case 0x0006:   
            close_connection_on_error ("status READ_ONLY");   
            break;   
        case 0x0007:   
            close_connection_on_error ("status WRITE_ONLY");   
            break;   
        case 0x0008:   
            close_connection_on_error ("status ERROR");   
            break;   
        case 0x0009:   
            close_connection_on_error ("status PERMISSION_DENIED");   
            break;   
        default:   
            close_connection_on_error ("invalid status");   
            break;   
    }   
   
    if ((buf[13] + (buf[14] << 8)) != pfkey)   
        close_connection_on_error ("incorrect pfkey");   
   
    pskey_len = buf[15] + (buf[16] << 8);   
   
#ifdef PKT_DUMP   
    printf("PSKey length: %d\n", pskey_len);   
#endif   
   
    return pskey_len;   
   
}   
   
   
/* Read/write pfkey.   
 *   
 * Parameters:  
 *  
 * - write: if 0 then read performed, write otherwise.  
 * - pfkey: pfkey  
 * - data:  buffer to store the data to read/write  
 * - data_len: size of the data in buffer to write (in bytes)  
 *  
 * Returns the number of bytes read, or 0 on write.  
*/   
static int pfkey(int write, uint16 pfkey, unsigned char *data, int data_len)   
{   
    uint16 bccmd_req, bccmd_varid, bccmd_len, pskey_len, psstore;   
    unsigned char buf[258];   
    int len = 0, chunk = 0;   
   
    if (write)   
    {   
        if (data_len % 2)    
            pskey_len = (data_len + 1) / 2;   
        else       
            pskey_len = data_len / 2;   
        bccmd_req = BCCMD_SETREQ;   
        psstore = PSSTORE_PSRAM;    /* write to RAM */   
//      psstore = PSSTORE_DEFAULT;   
        bccmd_len = pskey_len + 8;   
   
    }   
    else   
    {   
        pskey_len = pfkey_len(pfkey);   
        if (!pskey_len)   
            close_connection_on_error ("pfkey has zero length");   
        bccmd_req = BCCMD_GETREQ;   
        psstore = PSSTORE_DEFAULT;   
        bccmd_len = pskey_len + 8;     
        if (bccmd_len < 9)   
            bccmd_len = 9;          /* min allowed length == 9 */   
    }   
   
   
    bccmd_seq++;   
    bccmd_varid = 0x7003;           /* varid: Read/Write PS key */   
   
    memset(&buf, 0, sizeof(buf));   
   
    /* need to construct a hand-crafted HCI cmd pkt */   
    buf[0] = 0x00; buf[1] = 0xFC;   /* OGF = 0x3F & OCF = 0x00 */   
    buf[2] = bccmd_len * 2 + 1;     /* pkt len - 3 */   
   
    buf[3] = 0xC2;                  /* payload descriptor: last frag =1;   
                                    first frag = 1; channel = 2 */   
   
    buf[4] = bccmd_req & 0xFF; buf[5] = bccmd_req >> 8;   
   
    buf[6] = bccmd_len & 0xFF; buf[7] = bccmd_len >> 8;   
   
    buf[8]  = bccmd_seq & 0xFF; buf[9] = bccmd_seq >> 8;   
   
    buf[10] = bccmd_varid & 0xFF; buf[11] = bccmd_varid >> 8;   
   
    buf[12] = 0x00; buf[13] = 0x00; /* status */   
   
    buf[14] = pfkey & 0xFF; buf[15] = pfkey >> 8;   
       
    buf[16] = pskey_len & 0xFF; buf[17] = pskey_len >> 8;   
   
    buf[18] = psstore & 0xFF; buf[19] = psstore >> 8;   
   
    if (write)   
        memcpy(&buf[20], data, data_len);   
   
    /*  FIXME: IOCTL_CSRBC01_SEND_HCI_COMMAND doesn't return the number of bytes written? */   
    send_hci_command (&buf, buf[2] + 3);   
   
#ifdef PKT_DUMP   
    printf("HCI cmd[%d]: ", buf[2] + 3);   
    for (chunk=0; chunk != buf[2] + 3; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    /* not really efficient, but who cares? */   
    while (!(chunk = get_hci_event (&buf)))   
        Sleep(10);   
       
    if (chunk == 1)             /* too short to read packet length */   
    {      
        while (!(chunk = get_hci_event (&buf[1])))   
            Sleep(10);   
        chunk++;   
    }   
   
    for (len = chunk; len != buf[1] + 2; len = len + chunk)   
    {   
        while (!(chunk = get_hci_event (&buf[len])))   
            Sleep(10);   
    }   
   
#ifdef PKT_DUMP   
    printf("Event  [%d]:    ", len);   
    for (chunk=0; chunk!=len; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    if (buf[0] != 0xFF)         /* manuf-specific HCI event */   
        close_connection_on_error ("invalid packet received");   
   
    if (buf[1] != ((buf[5] + (buf[6] << 8)) * 2 + 1))   
        close_connection_on_error ("invalid length");   
   
    if (buf[2] != 0xC2)         /* payload descriptor */   
        close_connection_on_error ("invalid payload descriptor");   
       
    if ((buf[3] + (buf[4] << 8)) != BCCMD_GETRESP)   
        close_connection_on_error ("!= GETRESP");   
   
    if ((buf[5] + (buf[6] << 8)) != bccmd_len)   
        close_connection_on_error ("invalid length");   
   
    if ((buf[7] + (buf[8] << 8)) != bccmd_seq)   
        close_connection_on_error ("invalid sequence number");   
   
    if ((buf[9] + (buf[10] << 8)) != bccmd_varid)   
        close_connection_on_error ("invalid varid");   
   
    switch  (buf[11] + (buf[12] << 8))   
    {   
        case 0x0000:   
            /* OK status, continue */   
            break;   
        case 0x0001:   
            close_connection_on_error ("status NO_SUCH_VARID");   
            break;   
        case 0x0002:   
            close_connection_on_error ("status TOO_BIG");   
            break;   
        case 0x0003:   
            close_connection_on_error ("status NO_VALUE");   
            break;   
        case 0x0004:   
            close_connection_on_error ("status BAD_REQ");   
            break;   
        case 0x0005:   
            close_connection_on_error ("status NO_ACCESS");   
            break;   
        case 0x0006:   
            close_connection_on_error ("status READ_ONLY");   
            break;   
        case 0x0007:   
            close_connection_on_error ("status WRITE_ONLY");   
            break;   
        case 0x0008:   
            close_connection_on_error ("status ERROR");   
            break;   
        case 0x0009:   
            close_connection_on_error ("status PERMISSION_DENIED");   
            break;   
        default:   
            close_connection_on_error ("invalid status");   
            break;   
    }   
   
    if ((buf[13] + (buf[14] << 8)) != pfkey)   
        close_connection_on_error ("incorrect pfkey");   
   
    if ((buf[15] + (buf[16] << 8)) != pskey_len)   
        close_connection_on_error ("incorrect pfkey length");   
   
    if ((buf[17] + (buf[18] << 8)) != psstore)   
        close_connection_on_error ("incorrect psstore");   
   
    if (!write)   
    {   
        memcpy(data, &buf[19], pskey_len * 2);   
        return pskey_len * 2;   
    }   
    else   
        return 0;   
   
}   
   
/* read CSR firmware build id/number */   
static uint16 buildid(void)   
{   
    uint16 bccmd_req, bccmd_varid, bccmd_len;   
    unsigned char buf[258];   
    int len = 0, chunk = 0;   
   
    bccmd_req = BCCMD_GETREQ;   
       
    bccmd_seq++;   
    bccmd_varid = 0x2819;           /* varid: BUILDID */   
    bccmd_len = 9;                  /* minimum possible length, one uint16 is wasted */   
   
    memset(&buf, 0, sizeof(buf));   
   
    /* need to construct a hand-crafted HCI cmd pkt */   
    buf[0] = 0x00; buf[1] = 0xFC;   /* OGF = 0x3F & OCF = 0x00 */   
   
    buf[2] = bccmd_len * 2 + 1;     /* pkt len - 3 */   
   
    buf[3] = 0xC2;                  /* payload descriptor: last frag =1;   
                                    first frag = 1; channel = 2 */   
   
    buf[4] = bccmd_req & 0xFF; buf[5] = bccmd_req >> 8;   
   
    buf[6] = bccmd_len & 0xFF; buf[7] = bccmd_len >> 8;   
   
    buf[8]  = bccmd_seq & 0xFF; buf[9] = bccmd_seq >> 8;   
   
    buf[10] = bccmd_varid & 0xFF; buf[11] = bccmd_varid >> 8;   
   
    buf[12] = 0x00; buf[13] = 0x00; /* status */   
   
   
    /*  FIXME: IOCTL_CSRBC01_SEND_HCI_COMMAND doesn't return the number of bytes written? */   
    send_hci_command (&buf, buf[2] + 3);   
   
#ifdef PKT_DUMP   
    printf("HCI cmd[%d]: ", buf[2] + 3);   
    for (chunk=0; chunk != buf[2] + 3; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    /* not really efficient, but who cares? */   
    while (!(chunk = get_hci_event (&buf)))   
        Sleep(10);   
       
    if (chunk == 1)                 /* too short to read packet length */   
    {      
        while (!(chunk = get_hci_event (&buf[1])))   
            Sleep(10);   
        chunk++;   
    }   
   
    for (len = chunk; len != buf[1] + 2; len = len + chunk)   
    {   
        while (!(chunk = get_hci_event (&buf[len])))   
            Sleep(10);   
    }   
   
#ifdef PKT_DUMP   
    printf("Event  [%d]:    ", len);   
    for (chunk=0; chunk!=len; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    if (buf[0] != 0xFF)         /* manuf-specific HCI event */   
        close_connection_on_error ("invalid packet received");   
   
    if (buf[1] != 9 * 2 + 1)   
        close_connection_on_error ("hci event has invalid length");   
   
    if (buf[2] != 0xC2)         /* payload descriptor */   
        close_connection_on_error ("invalid payload descriptor");   
       
    if ((buf[3] + (buf[4] << 8)) != BCCMD_GETRESP)   
        close_connection_on_error ("!= GETRESP");   
   
    if ((buf[5] + (buf[6] << 8)) != 9)   
        close_connection_on_error ("invalid length");   
   
    if ((buf[7] + (buf[8] << 8)) != bccmd_seq)   
        close_connection_on_error ("invalid sequence number");   
   
    if ((buf[9] + (buf[10] << 8)) != bccmd_varid)   
        close_connection_on_error ("invalid varid");   
   
    switch  (buf[11] + (buf[12] << 8))   
    {   
        case 0x0000:   
            /* OK status, continue */   
            break;   
        case 0x0001:   
            close_connection_on_error ("status NO_SUCH_VARID");   
            break;   
        case 0x0002:   
            close_connection_on_error ("status TOO_BIG");   
            break;   
        case 0x0003:   
            close_connection_on_error ("status NO_VALUE");   
            break;   
        case 0x0004:   
            close_connection_on_error ("status BAD_REQ");   
            break;   
        case 0x0005:   
            close_connection_on_error ("status NO_ACCESS");   
            break;   
        case 0x0006:   
            close_connection_on_error ("status READ_ONLY");   
            break;   
        case 0x0007:   
            close_connection_on_error ("status WRITE_ONLY");   
            break;   
        case 0x0008:   
            close_connection_on_error ("status ERROR");   
            break;   
        case 0x0009:   
            close_connection_on_error ("status PERMISSION_DENIED");   
            break;   
        default:   
            close_connection_on_error ("invalid status");   
            break;   
    }   
   
    return buf[13] + (buf[14] << 8);   
   
}   
   
   
/* set UART baud rate, stop bit(s), parity   
 *  
 * The change happens immediately, most probably the response on this command will be received back  
 * after the new UART settings took effect.  
 *   
 * Parameters:  
 *  
 * baud = baud rate, the value is used as a clock divisor, any value can be programmed.  
 *        the common values are: 9600, 19200, ... 115200, 230400, 460800, 921600.  
 * stop = number of stop bits, either 1 or 2  
 * parity = parity, 0 - no parity, 1 - even parity, 2 - odd parity  
 *  
*/   
static void uart_config(int baud, int stop, int parity)   
{   
    uint16 bccmd_req, bccmd_varid, bccmd_len, divisor;   
    unsigned char buf[258];   
    int len = 0, chunk = 0;   
   
    bccmd_req = BCCMD_SETREQ;   
       
    bccmd_seq++;   
    bccmd_varid = 0x6802;           /* varid: CONFIG_UART */   
    bccmd_len = 9;                  /* minimum possible length, one uint16 is wasted */   
   
    memset(&buf, 0, sizeof(buf));   
   
    /* need to construct a hand-crafted HCI cmd pkt */   
    buf[0] = 0x00; buf[1] = 0xFC;   /* OGF = 0x3F & OCF = 0x00 */   
   
    buf[2] = bccmd_len * 2 + 1;     /* pkt len - 3 */   
   
    buf[3] = 0xC2;                  /* payload descriptor: last frag =1;   
                                    first frag = 1; channel = 2 */   
   
    buf[4] = bccmd_req & 0xFF; buf[5] = bccmd_req >> 8;   
   
    buf[6] = bccmd_len & 0xFF; buf[7] = bccmd_len >> 8;   
   
    buf[8]  = bccmd_seq & 0xFF; buf[9] = bccmd_seq >> 8;   
   
    buf[10] = bccmd_varid & 0xFF; buf[11] = bccmd_varid >> 8;   
   
    buf[12] = 0x00; buf[13] = 0x00; /* status */   
   
    divisor = (baud*64+7812)/15625;   
   
    if (stop == 1)   
        divisor |= 0x0000;   
    else if (stop == 2)   
        divisor |= 0x2000;   
    else   
        close_connection_on_error ("invalid stop bit number");   
       
    if (parity == 0)   
        divisor |= 0x0000;   
    else if (parity == 1)   
        divisor |= 0xC000;   
    else if (parity == 2)   
        divisor |= 0x4000;   
    else   
        close_connection_on_error ("invalid parity bit value");   
   
    buf[14] = divisor & 0xFF; buf[15] = divisor >> 8;   
   
    /*  FIXME: IOCTL_CSRBC01_SEND_HCI_COMMAND doesn't return the number of bytes written? */   
    send_hci_command (&buf, buf[2] + 3);   
   
#ifdef PKT_DUMP   
    printf("HCI cmd[%d]: ", buf[2] + 3);   
    for (chunk=0; chunk != buf[2] + 3; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    /* not really efficient, but who cares? */   
    while (!(chunk = get_hci_event (&buf)))   
        Sleep(10);   
       
    if (chunk == 1)                 /* too short to read packet length */   
    {      
        while (!(chunk = get_hci_event (&buf[1])))   
            Sleep(10);   
        chunk++;   
    }   
   
    for (len = chunk; len != buf[1] + 2; len = len + chunk)   
    {   
        while (!(chunk = get_hci_event (&buf[len])))   
            Sleep(10);   
    }   
   
#ifdef PKT_DUMP   
    printf("Event  [%d]:    ", len);   
    for (chunk=0; chunk!=len; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    if (buf[0] != 0xFF)         /* manuf-specific HCI event */   
        close_connection_on_error ("invalid packet received");   
   
    if (buf[1] != 9 * 2 + 1)   
        close_connection_on_error ("hci event has invalid length");   
   
    if (buf[2] != 0xC2)         /* payload descriptor */   
        close_connection_on_error ("invalid payload descriptor");   
       
    if ((buf[3] + (buf[4] << 8)) != BCCMD_GETRESP)   
        close_connection_on_error ("!= GETRESP");   
   
    if ((buf[5] + (buf[6] << 8)) != 9)   
        close_connection_on_error ("invalid length");   
   
    if ((buf[7] + (buf[8] << 8)) != bccmd_seq)   
        close_connection_on_error ("invalid sequence number");   
   
    if ((buf[9] + (buf[10] << 8)) != bccmd_varid)   
        close_connection_on_error ("invalid varid");   
   
    switch  (buf[11] + (buf[12] << 8))   
    {   
        case 0x0000:   
            /* OK status, continue */   
            break;   
        case 0x0001:   
            close_connection_on_error ("status NO_SUCH_VARID");   
            break;   
        case 0x0002:   
            close_connection_on_error ("status TOO_BIG");   
            break;   
        case 0x0003:   
            close_connection_on_error ("status NO_VALUE");   
            break;   
        case 0x0004:   
            close_connection_on_error ("status BAD_REQ");   
            break;   
        case 0x0005:   
            close_connection_on_error ("status NO_ACCESS");   
            break;   
        case 0x0006:   
            close_connection_on_error ("status READ_ONLY");   
            break;   
        case 0x0007:   
            close_connection_on_error ("status WRITE_ONLY");   
            break;   
        case 0x0008:   
            close_connection_on_error ("status ERROR");   
            break;   
        case 0x0009:   
            close_connection_on_error ("status PERMISSION_DENIED");   
            break;   
        default:   
            close_connection_on_error ("invalid status");   
            break;   
    }   
   
    return;   
   
}   
   
/* enter DEEP_SLEEP mode  
 *  
 * The change happens approx. 0.5s after sending event back  
 *  
*/   
static void deep_sleep(void)   
{   
    uint16 bccmd_req, bccmd_varid, bccmd_len, testid;   
    unsigned char buf[258];   
    int len = 0, chunk = 0;   
   
    bccmd_req = BCCMD_SETREQ;   
       
    bccmd_seq++;   
    bccmd_varid = 0x5004;           /* varid: RADIOTEST */   
    bccmd_len = 9;                  /* minimum possible length, one uint16 is wasted */   
   
    memset(&buf, 0, sizeof(buf));   
   
    /* need to construct a hand-crafted HCI cmd pkt */   
    buf[0] = 0x00; buf[1] = 0xFC;   /* OGF = 0x3F & OCF = 0x00 */   
   
    buf[2] = bccmd_len * 2 + 1;     /* pkt len - 3 */   
   
    buf[3] = 0xC2;                  /* payload descriptor: last frag =1;   
                                    first frag = 1; channel = 2 */   
   
    buf[4] = bccmd_req & 0xFF; buf[5] = bccmd_req >> 8;   
   
    buf[6] = bccmd_len & 0xFF; buf[7] = bccmd_len >> 8;   
   
    buf[8]  = bccmd_seq & 0xFF; buf[9] = bccmd_seq >> 8;   
   
    buf[10] = bccmd_varid & 0xFF; buf[11] = bccmd_varid >> 8;   
   
    buf[12] = 0x00; buf[13] = 0x00; /* status */   
   
    testid = 10;            /* DEEP_SLEEP */   
   
    buf[14] = testid & 0xFF; buf[15] = testid >> 8;   
   
    /*  FIXME: IOCTL_CSRBC01_SEND_HCI_COMMAND doesn't return the number of bytes written? */   
    send_hci_command (&buf, buf[2] + 3);   
   
#ifdef PKT_DUMP   
    printf("HCI cmd[%d]: ", buf[2] + 3);   
    for (chunk=0; chunk != buf[2] + 3; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    /* not really efficient, but who cares? */   
    while (!(chunk = get_hci_event (&buf)))   
        Sleep(10);   
       
    if (chunk == 1)                 /* too short to read packet length */   
    {      
        while (!(chunk = get_hci_event (&buf[1])))   
            Sleep(10);   
        chunk++;   
    }   
   
    for (len = chunk; len != buf[1] + 2; len = len + chunk)   
    {   
        while (!(chunk = get_hci_event (&buf[len])))   
            Sleep(10);   
    }   
   
#ifdef PKT_DUMP   
    printf("Event  [%d]:    ", len);   
    for (chunk=0; chunk!=len; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    if (buf[0] != 0xFF)         /* manuf-specific HCI event */   
        close_connection_on_error ("invalid packet received");   
   
    if (buf[1] != 9 * 2 + 1)   
        close_connection_on_error ("hci event has invalid length");   
   
    if (buf[2] != 0xC2)         /* payload descriptor */   
        close_connection_on_error ("invalid payload descriptor");   
       
    if ((buf[3] + (buf[4] << 8)) != BCCMD_GETRESP)   
        close_connection_on_error ("!= GETRESP");   
   
    if ((buf[5] + (buf[6] << 8)) != 9)   
        close_connection_on_error ("invalid length");   
   
    if ((buf[7] + (buf[8] << 8)) != bccmd_seq)   
        close_connection_on_error ("invalid sequence number");   
   
    if ((buf[9] + (buf[10] << 8)) != bccmd_varid)   
        close_connection_on_error ("invalid varid");   
   
    switch  (buf[11] + (buf[12] << 8))   
    {   
        case 0x0000:   
            /* OK status, continue */   
            break;   
        case 0x0001:   
            close_connection_on_error ("status NO_SUCH_VARID");   
            break;   
        case 0x0002:   
            close_connection_on_error ("status TOO_BIG");   
            break;   
        case 0x0003:   
            close_connection_on_error ("status NO_VALUE");   
            break;   
        case 0x0004:   
            close_connection_on_error ("status BAD_REQ");   
            break;   
        case 0x0005:   
            close_connection_on_error ("status NO_ACCESS");   
            break;   
        case 0x0006:   
            close_connection_on_error ("status READ_ONLY");   
            break;   
        case 0x0007:   
            close_connection_on_error ("status WRITE_ONLY");   
            break;   
        case 0x0008:   
            close_connection_on_error ("status ERROR");   
            break;   
        case 0x0009:   
            close_connection_on_error ("status PERMISSION_DENIED");   
            break;   
        default:   
            close_connection_on_error ("invalid status");   
            break;   
    }   
   
    return;   
   
}   
   
/* Forces the module to reboot immediately  
 *  
 * Parameters:  
 *  
 * warm = 1 (warm reboot, RAM store is preserved) or 0 (cold reboot, the same as   
 *           power-cycling the module)  
 *  
 * It's most probable that response will never be able to make it back, so don't bother  
*/   
static void reboot(int warm)   
{   
    uint16 bccmd_req, bccmd_varid, bccmd_len;   
    unsigned char buf[258];   
    int len = 0, chunk = 0;   
   
    bccmd_req = BCCMD_SETREQ;   
       
    bccmd_seq++;   
       
    if (warm == 0)   
        bccmd_varid = 0x4001;           /* varid: COLF_RESET */   
    else if (warm == 1)   
        bccmd_varid = 0x4002;           /* varid: WARM_RESET */   
    else   
        close_connection_on_error ("invalid reset type");   
   
    bccmd_len = 9;                  /* minimum possible length, one uint16 is wasted */   
   
    memset(&buf, 0, sizeof(buf));   
   
    /* need to construct a hand-crafted HCI cmd pkt */   
    buf[0] = 0x00; buf[1] = 0xFC;   /* OGF = 0x3F & OCF = 0x00 */   
   
    buf[2] = bccmd_len * 2 + 1;     /* pkt len - 3 */   
   
    buf[3] = 0xC2;                  /* payload descriptor: last frag =1;   
                                    first frag = 1; channel = 2 */   
   
    buf[4] = bccmd_req & 0xFF; buf[5] = bccmd_req >> 8;   
   
    buf[6] = bccmd_len & 0xFF; buf[7] = bccmd_len >> 8;   
   
    buf[8]  = bccmd_seq & 0xFF; buf[9] = bccmd_seq >> 8;   
   
    buf[10] = bccmd_varid & 0xFF; buf[11] = bccmd_varid >> 8;   
   
    buf[12] = 0x00; buf[13] = 0x00; /* status */   
   
    /*  FIXME: IOCTL_CSRBC01_SEND_HCI_COMMAND doesn't return the number of bytes written? */   
    send_hci_command (&buf, buf[2] + 3);   
   
#ifdef PKT_DUMP   
    printf("HCI cmd[%d]: ", buf[2] + 3);   
    for (chunk=0; chunk != buf[2] + 3; chunk++)   
        printf("%02x ", buf[chunk]);   
    printf("\n");   
#endif   
   
    return;   
   
}   
   
static void usb_reset(void)   
{   
    unsigned long written;   
    int status;   
   
    status = DeviceIoControl(handle,   
                            IOCTL_CSRBC01_RESET_DEVICE,   
                            0,   
                            0,   
                            0,   
                            0,   
                            &written,   
                            0);   
   
    if (!status)   
        close_connection_on_error ("IOCTL_CSRBC01_RESET_DEVICE");   
   
}   
   
/*   
 * We only try to open the first CSR device found, if you have multiply  
 * devices, please unplug all but the last one or change device name from  
 * CSR0 to CSRn.  
 */   
   
int main (int arvc, char* arvgv)   
{   
   
    unsigned char buf[258];   
    unsigned long written;   
    dev_desc desc;   
    uint16 len;   
    int baud_rate;   
    uint16 divisor, uart_conf, retries, host_if;   
    int status;   
   
   
    /* open device */   
    handle = CreateFile("\\\\.\\CSR0",   
                        GENERIC_READ | GENERIC_WRITE,   
                        0,   
                        NULL,   
                        OPEN_EXISTING,   
                        0,   
                        NULL);   
   
    if ( handle == INVALID_HANDLE_VALUE)   
        close_connection_on_error ("CreateFile");   
       
    memset(&desc, 0, sizeof(desc));   
   
    status = DeviceIoControl(handle,   
                            IOCTL_CSRBC01_GET_DEVICE_DESCRIPTOR,   
                            0,   
                            0,   
                            &desc,   
                            sizeof(desc), /* must be 18 */   
                            &written,   
                            0);   
   
    if (!status)   
        close_connection_on_error ("IOCTL_CSRBC01_GET_DEVICE_DESCRIPTOR");   
   
    printf("Found CSR USB device:       VID=%04X, PID=%04X\n", desc.idVendor, desc.idProduct);   
   
    /* reset device to known state */   
    printf("Resetting...\n");   
    usb_reset();   
   
    if (handle != INVALID_HANDLE_VALUE)   
        CloseHandle (handle);   
   
    /* wait for hardware to settle */   
    Sleep(500);    
   
    /* re-open device */   
    handle = CreateFile("\\\\.\\CSR0",   
                        GENERIC_READ | GENERIC_WRITE,   
                        0,   
                        NULL,   
                        OPEN_EXISTING,   
                        0,   
                        NULL);   
   
    if ( handle == INVALID_HANDLE_VALUE)   
        close_connection_on_error ("CreateFile");   
   
    printf("CSR firmware build ID:      0x%X\n", buildid());   
   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_BDADDR, buf, 0);   
    if (len != 8)   
        close_connection_on_error ("PSKEY_BDADDR");   
    /* It's hard to make it more akward than that ;) */   
    printf("read:PSKEY_BDADDR:      %02X-%02X-%02X-%02X-%02X-%02X\n\n", 0,   
                                                            buf[6] + (buf[7] << 8),   
                                                            buf[4] + (buf[5] << 8),   
                                                            buf[0] + (buf[1] << 8),   
                                                            buf[3],   
                                                            buf[2]);   
/*  
//  printf("read:PSKEY_BDADDR:      %02X %02X %02X %02X %02X %02X %02X %02X\n\n",  
//                                  buf[0], buf[1], buf[2], buf[3], buf[4], buf[5], buf[6], buf[7]);  
  
    buf[0] = 0x1c;  
    buf[2] = 0x6a;  
    buf[3] = 0x8d;  
    buf[4] = 0xc7;  
    buf[6] = 0x02;  
      
//  printf("read:PSKEY_BDADDR:      %02X %02X %02X %02X %02X %02X %02X %02X\n\n",  
//                                  buf[0], buf[1], buf[2], buf[3], buf[4], buf[5], buf[6], buf[7]);      
    pfkey(1, PSKEY_BDADDR, buf, 8);  
      
    memset(&buf, 0, sizeof(buf));  
    len = pfkey(0, PSKEY_BDADDR, buf, 0);  
    if (len != 8)  
        close_connection_on_error ("PSKEY_BDADDR");  
  
    printf("read:PSKEY_BDADDR:      %02X-%02X-%02X-%02X-%02X-%02X\n\n", 0,  
                                                            buf[6] + (buf[7] << 8),  
                                                            buf[4] + (buf[5] << 8),  
                                                            buf[0] + (buf[1] << 8),  
                                                            buf[3],  
                                                            buf[2]);  
    goto Exit;  
*/   
   
   
   
/* Here's the structure of PSKEY_HOSTIO_UART_PS_BLOCK:  
  
PSKEY_HOSTIO_UART_PS_BLOCK (0x191):  
  
0       1       2       3       4       5       6       7       8       9  
  
3B0     A8      FA      14      4       0       4       1E      64      A  
  
  
0. PSKEY_UART_BAUD_RATE (0x204)  
   0x3B0 == 230400 bps  
=> 0x1D8 == 115200 bps  
  
1. PSKEY_UART_CONFIG (0x205)  
   0xA8 == hardware flow control, RTS on 1st bit, non-BCSP hardware  
=> 6    == one parity bit, even parity (BCSP)  
  
2. PSKEY_UART_SEQ_TIMEOUT (0x405)  
   0xFA == 250ms  
  
3. PSKEY_UART_SEQ_RETRIES (0x406)  
   0x14 == 20 retries.  
=> 0 == retry indefinitely  
  
4. PSKEY_UART_SEQ_WINSIZE (0x407)  
  
   4 == number of unacknowledged packets that can be sent before waiting   
   for an acknowledgment  
  
5. PSKEY_UART_USE_CRC_ON_TX (0x408)  
   0 == disabled  
  
6. PSKEY_UART_HOST_INITIAL_STATE (0x409)  
   4 == host never sleeps  
  
7. PSKEY_UART_HOST_ATTENTION_SPAN (0x40A) ????  
   0x1E == 30 seconds  
  
8. PSKEY_UART_HOST_WAKEUP_TIME (0x40B) ???  
   0x64 == 100ms  
  
9. PSKEY_UART_HOST_WAKEUP_WAIT (0x40C) ???  
   0xA == 10ms  
  
*/   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_HOSTIO_UART_PS_BLOCK, buf, 0);   
    if (len != 20)   
        close_connection_on_error ("PSKEY_HOST_INTERFACE");   
    printf("read:PSKEY_HOSTIO_UART_PS_BLOCK:    ");   
    for (len = 0; len < 20; len = len + 2)   
        printf("%02x ", buf[len] + (buf[len+1] << 8));   
    printf("\n");   
   
    baud_rate = 115200*8;   
    divisor = (baud_rate * 64 + 7812) / 15625;   
    buf[0] = divisor & 0xFF ; buf[1] = (divisor >> 8) & 0xFF;    
   
    uart_conf = 6; /* one stop bit, even parity, no RTS/CTS flow control,  
                    non-BCSP hardware disabled */   
    buf[2] = uart_conf & 0xFF ; buf[3] = (uart_conf >> 8) & 0xFF;    
   
    retries = 0; /* retry indefinitely on BCSP packet transmission */   
    buf[6] = retries & 0xFF ; buf[7] = (retries >> 8) & 0xFF;    
   
/* it should look like the following:  
  
    buf[0] = 0xD8;  
    buf[1] = 1;  
    buf[2] = 6;  
    buf[3] = 0;  
    buf[4] = 0xFA;  
    buf[5] = 0;  
    buf[6] = 0;  
    buf[7] = 0;  
    buf[8] = 4;  
    buf[9] = 0;  
    buf[10] = 0;  
    buf[11] = 0;  
    buf[12] = 4;  
    buf[13] = 0;  
    buf[14] = 0x1E;  
    buf[15] = 0;  
    buf[16] = 0x64;  
    buf[17] = 0;  
    buf[18] = 0xA;  
    buf[19] = 0;  
*/   
    printf("write:PSKEY_HOSTIO_UART_PS_BLOCK:   ");   
    for (len = 0; len < 10*2; len = len + 2)   
        printf("%02x ", buf[len] + (buf[len+1] << 8));   
    printf("\n");   
    pfkey(1, PSKEY_HOSTIO_UART_PS_BLOCK, buf, 20);   
   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_HOSTIO_UART_PS_BLOCK, buf, 0);   
    if (len != 20)   
        close_connection_on_error ("PSKEY_HOST_INTERFACE");   
    printf("read:PSKEY_HOSTIO_UART_PS_BLOCK:    ");   
    for (len = 0; len < 20; len = len + 2)   
        printf("%02x ", buf[len] + (buf[len+1] << 8));   
    printf("\n");   
   
/* ---------------------------------------------------------------------------- */   
    /* PSKEY_HOST_INTERFACE should be change at the same time as PSKEY_HOSTIO_UART_PS_BLOCK */   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_HOST_INTERFACE, buf, 0);   
    if (len != 2)   
        close_connection_on_error ("PSKEY_HOST_INTERFACE");   
    printf("read:PSKEY_HOST_INTERFACE:      %d\n", buf[0] + (buf[1] << 8));   
   
    host_if = 1; /* UART in BCSP mode */   
    buf[0] = host_if & 0xFF ; buf[1] = (host_if >> 8) & 0xFF;    
   
    printf("write:PSKEY_HOST_INTERFACE:     %d\n", buf[0] + (buf[1] << 8));   
    pfkey(1, PSKEY_HOST_INTERFACE, buf, 2);   
   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_HOST_INTERFACE, buf, 0);   
    if (len != 2)   
        close_connection_on_error ("PSKEY_HOST_INTERFACE");   
    printf("read:PSKEY_HOST_INTERFACE:      %d\n", buf[0] + (buf[1] << 8));   
   
/* ---------------------------------------------------------------------------- */   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_DEEP_SLEEP_STATE, buf, 0);   
    if (len != 2)   
        close_connection_on_error ("PSKEY_DEEP_SLEEP_STATE");   
    printf("read:PSKEY_DEEP_SLEEP_STATE:        %d\n", buf[0] + (buf[1] << 8));   
   
/* ---------------------------------------------------------------------------- */   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_DEEP_SLEEP_WAKE_CTS, buf, 0);   
    if (len != 2)   
        close_connection_on_error ("PSKEY_DEEP_SLEEP_WAKE_CTS");   
    printf("read:PSKEY_DEEP_SLEEP_WAKE_CTS:     %d\n", buf[0] + (buf[1] << 8));   
   
/* ---------------------------------------------------------------------------- */   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_UART_SLEEP_TIMEOUT, buf, 0);   
    if (len != 2)   
        close_connection_on_error ("PSKEY_UART_SLEEP_TIMEOUT");   
    printf("read:PSKEY_UART_SLEEP_TIMEOUT:      %d ms\n", buf[0] + (buf[1] << 8));   
   
/* ---------------------------------------------------------------------------- */   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_WD_PERIOD, buf, 0);   
    if (len != 4)   
        close_connection_on_error ("PSKEY_WD_PERIOD");   
    printf("read:PSKEY_WD_PERIOD:           %d ms\n", ((buf[0] << 16) + (buf[1] << 24) + buf[2] + (buf[3] << 8))/1000);   
   
/* ---------------------------------------------------------------------------- */   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_WD_TIMEOUT, buf, 0);   
    if (len != 4)   
        close_connection_on_error ("PSKEY_WD_TIMEOUT");   
    printf("read:PSKEY_WD_TIMEOUT:          %d ms\n", ((buf[0] << 16) + (buf[1] << 24) + buf[2] + (buf[3] << 8))/1000);   
   
/* ---------------------------------------------------------------------------- */   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_HOSTIO_UART_RESET_TIMEOUT, buf, 0);   
    if (len != 4)   
        close_connection_on_error ("PSKEY_HOSTIO_UART_RESET_TIMEOUT");   
    printf("read:PSKEY_HOSTIO_UART_RESET_TIMEOUT:   %d ms\n", ((buf[0] << 16) + (buf[1] << 24) + buf[2] + (buf[3] << 8))/1000);   
   
/* ---------------------------------------------------------------------------- */   
    memset(&buf, 0, sizeof(buf));   
    len = pfkey(0, PSKEY_HOSTIO_BREAK_POLL_PERIOD, buf, 0);   
    if (len != 4)   
        close_connection_on_error ("PSKEY_HOSTIO_BREAK_POLL_PERIOD");   
    printf("read:PSKEY_HOSTIO_BREAK_POLL_PERIOD:    %d ms\n", ((buf[0] << 16) + (buf[1] << 24) + buf[2] + (buf[3] << 8))/1000);   
   
    printf("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");   
    printf("!!!!  Rebooting device.... It should come up in UART BCSP mode now  !!!!\n");   
    printf("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");   
   
Exit:   
    /* warm reboot */   
    //reboot(1);   
   
    if (handle != INVALID_HANDLE_VALUE)   
        CloseHandle (handle);   
   
    return 0;   
   
} 