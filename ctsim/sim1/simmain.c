#include <stdio.h>

#include "sim1_dll.h"

int main(void){
  char data[100];
  int r = 0;
  int i = 0;

  r = sim1_test1(1,9, 100, sizeof(data), data);
  printf("r = %d ...\n", r);
  for (i = 0; i< r; i++){
    printf("%02x,", data[i]);
  }
}