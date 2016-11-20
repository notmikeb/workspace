#include <string.h>
#include <stdio.h>
#include "word.h"

char temp[128];

Word::Word(const char *w){
  int i;
  int length = strlen(w);
  this->the_word = new char(length+1);
  for(i = 0; i< length; i++){
     this->the_word[i] = w[i];
     printf("%d\n", w[i]);
  }
  this->the_word[length] = 0;
}

char *Word::reverse() const {

int i;
for ( i = 0; i < sizeof(temp); i++){
  temp[i] = 0;
}
for( i =0; this->the_word != 0  && this->the_word[i] != 0 ; i++){
  temp[i] = this->the_word[i];
}
return (char *)this->the_word;
}