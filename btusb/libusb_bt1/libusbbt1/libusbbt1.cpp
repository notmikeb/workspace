// libusbbt1.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"

#include <stdio.h>
extern "C" {
#include "libusb.h"
}

#pragma comment( lib, "libusb-1.0.lib" )


extern "C" {

ssize_t g_cnt = 0;  // device number

__declspec(dllexport) int myrun1(int i){
	return i;
}

__declspec(dllexport) int myrun2(int i[], int max){
	char tmpmsg[100];
	sprintf(tmpmsg, "myrun2 %d\n", i);
	OutputDebugStringA(tmpmsg);
	int j = 0;
	if( max > 0){
		for (j = 0; j < max && j < 256; j++){
			i[j] = j;
		}
		return j;
	}	
	return -1;
}

__declspec(dllexport) int myrun3(int i, char *msg, int max){
	char tmpmsg[100];
	sprintf(tmpmsg, "myrun3 %d\n", i);
	OutputDebugStringA(tmpmsg);

	if( msg != 0 ){
		sprintf(msg, tmpmsg);
		return i+2;
	}
	return -1;
}

static void print_devs(libusb_device **devs)
{
	libusb_device *dev;
	int i = 0, j = 0;
	uint8_t path[8]; 
	char tmpmsg[256];

	while ((dev = devs[i++]) != NULL) {
		struct libusb_device_descriptor desc;
		int r = libusb_get_device_descriptor(dev, &desc);
		if (r < 0) {
			fprintf(stderr, "failed to get device descriptor");
			return;
		}

		sprintf(tmpmsg, "index:%d %04x:%04x (bus %d, device %d)", i-1,
			desc.idVendor, desc.idProduct,
			libusb_get_bus_number(dev), libusb_get_device_address(dev));
        OutputDebugStringA(tmpmsg);

		r = libusb_get_port_numbers(dev, path, sizeof(path));
		if (r > 0) {
			sprintf(tmpmsg, " path: %d r:%d", path[0], r);
			OutputDebugStringA(tmpmsg);
			for (j = 1; j < r; j++){
				sprintf(tmpmsg, ".%d", path[j]);
			    OutputDebugStringA(tmpmsg);
			}
		}
		sprintf(tmpmsg, "\n");
		OutputDebugStringA(tmpmsg);
	}
}

libusb_device **g_devs;

__declspec(dllexport) int bt1_init(){
	
	int r;
	ssize_t cnt;

	r = libusb_init(NULL);
	if (r < 0)
		return r;

	cnt = libusb_get_device_list(NULL, &g_devs);
	if (cnt < 0)
		return (int) cnt;

	g_cnt = cnt;
	print_devs(g_devs);

	return 0;
}

__declspec(dllexport) int bt1_list(int i){
	char tmpmsg[100];
	sprintf(tmpmsg, "myrun3 %d\n", i);
	OutputDebugStringA(tmpmsg);

	return 0;
}

__declspec(dllexport) int bt1_getall(int index[], int max){
	if(max > 0 && max < 256){
	}
	return g_cnt;
}

__declspec(dllexport) int bt1_getDeviceIndex(int uid, int pid, int index){
	int i;
	int r = -1;
	char tmpmsg[100];

	for (i =0; i< g_cnt; i++){
		struct libusb_device_descriptor desc;
		int r = libusb_get_device_descriptor(g_devs[i], &desc);
		if (r < 0) {
			fprintf(stderr, "failed to get device descriptor");
			continue;
		}
		if( uid == desc.idVendor && pid == desc.idProduct ){
			sprintf(tmpmsg, "found at %d left:%d\n", i, index);
			OutputDebugStringA(tmpmsg);
			if( index == 0 ){
				r = i;
				return i;
			}else{
				index = index-1;
			}
		}
	}
	sprintf(tmpmsg, "not found !\n");
	OutputDebugStringA(tmpmsg);
	return r;
}

__declspec(dllexport) int bt1_open(){
	return -1;
}

__declspec(dllexport) int bt1_deinit(){

	char tmpmsg[100];
	sprintf(tmpmsg, "bt1_deinit\n");
	OutputDebugStringA(tmpmsg);

	libusb_free_device_list(g_devs, 1);
	g_devs = 0;

	libusb_exit(NULL);

	return 0;
}


}

int CALLBACK WinMain(
  _In_ HINSTANCE hInstance,
  _In_ HINSTANCE hPrevInstance,
  _In_ LPSTR     lpCmdLine,
  _In_ int       nCmdShow
){
	int r = 0;
	char tmpmsg[100];

	printf("hello");
	OutputDebugStringA("My output string.\n");
	r = bt1_init();
	sprintf(tmpmsg, "bt1_init %d\n", r);

	OutputDebugStringA(tmpmsg);

	bt1_deinit();
	return 0;
}
