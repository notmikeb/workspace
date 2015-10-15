#include <stdio.h>
#include <string.h>
#include "sim2_dll.h"

__stdcall int sim1_test1(char c, int i , long l, int max, void *pout)
{
char *out = (char *)pout;
// compose c, i, l to out  out
if(max > (sizeof(c) + sizeof(i) + sizeof(l))){
  out[0] = c;

  out[1] = i & 0xf;
  out[2] = (i >> 4) & 0xf;
  out[3] = (i >> 8) & 0xf;
  out[4] = (i >> 12) & 0xf;

  out[5] = l & 0xf;
  out[6] = (l >> 4) & 0xf;
  out[7] = (l >> 8) & 0xf;
  out[8] = (l >> 12) & 0xf;

  printf("%d %d %d  %d %d %d\n", c, i, l, c, i&0xf, l&0xf );
  return (sizeof(c)+sizeof(i)+sizeof(l));
}
return 0;
}

int __stdcall hci_write(int i, void *data)
{
   // always success
   return i;
}

static int choose = 0;
int __stdcall hci_read(int max, void *data)
{
    char data1[3] = {3, 2,3}; // 2 char
    char data2[5] = {5, 0x01, 0, 0x02, 0}; // uint16, uint16
    char data3[9] = {9, 1,0, 0, 0, 3, 4,5,6}; // uint32, char, char, char, char
   
   int write = 0;
   choose = choose % 3;
   switch (choose){
       case 0:
	   if( max >=3 ){
	   memcpy(data, data1, 3);
	   write = 3;
	   }
	   break;
	   case 1:
	   if( max >=5 ){
	   memcpy(data, data3, 5);
	   write = 5;
	   }
	   break;
	   case 2:
	   if( max >=9 ){
	   memcpy(data, data3, 9);
	   write = 9;
	   }
	   break;
	   default:
	   write = 0;
	   break;
   }
   
   choose++;
   return write;
}
