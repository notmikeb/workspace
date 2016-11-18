#include <stdio.h>
#include "testdata.h"


int main(int argc, char**argv){


printf("getint(3) %d\n", getint(3));

printf("getshort(256) %d\n", getshort(256));
printf("getshort(256*256) %d\n", getshort(256*256));

return 0;
}
