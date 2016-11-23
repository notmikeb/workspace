
#include <stdio.h>
#include "testdata.h"

//typedef int (*data_callback)(const struct strdata d, int timeout);

data_callback fptr = 0;

char temp[100];
struct strdata tempdata;

int getint(int i){
  return i+1;
}

short getshort(short j){
  return j+1;
}

// copy string below 254
int getmessage(const char *msg, char *out){
int j = 0;
if(msg != 0){
 for(int i = 0; i<254;i++){
  if(msg[i] != 0){
   j = j+1;
   out[i] = msg[i];
  }
 }
}
return j; // return the copy length
}

int register_callback(data_callback ptr){
struct strdata tempd;

if( ptr == 0 ){
  return -1;
}
fptr = ptr;

fptr(tempd, -1);

return 0;
}



