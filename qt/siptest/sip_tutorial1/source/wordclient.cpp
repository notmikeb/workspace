#include "word.h"
#include "stdio.h"

int main(int argc, char **argv){
  printf("this is main of wordclient.exe\n");
  Word* w1 = new Word("testme");
  w1->reverse();
  return 0;
}