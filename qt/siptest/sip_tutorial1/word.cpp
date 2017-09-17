#include "word.h"
#include "stdio.h"

Word::Word(const char *w){
printf("a new word object '%s'\n", w);
the_word = new char[20]();
int len = 0;
for(int i = 0; i< 20 ; i++){
    the_word[i] = 0;
}
for(int i = 0; i< 19 && w[i]!=0; i++){
    the_word[i] = w[i];
    len++;
}
printf("len:%d", len);
}

char *Word::reverse() const{
printf("reverse a word\n");
printf("reverse:'%s'", the_word);
return 0;
}

Word::~Word(){
printf("destroy a word");
delete[] the_word;    
}
