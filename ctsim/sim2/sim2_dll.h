#ifndef SIM1_DLL_H
#define SIM1_DLL_H


#ifdef __cplusplus
extern "C" {
#endif

int __stdcall sim1_test1(char c, int i , long l, int max, void *pout);
int __stdcall hci_write(int i, void *data);
int __stdcall hci_read(int max, void *data);

#ifdef __cplusplus
}
#endif

#endif
