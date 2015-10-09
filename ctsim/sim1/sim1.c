#include <stdio.h>
#include "sim1_dll.h"

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