/*
1. Convert hex to base64 and back.

The string:

  49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

should produce:

  SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t

Now use this code everywhere for the rest of the exercises. Here's a
simple rule of thumb:

  Always operate on raw bytes, never on encoded strings. Only use hex
  and base64 for pretty-printing.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hextobase64.h"
#include "base64toHex.h"

int main(){
  int decision;
  char matasano_intern_2014[1024];
  
  printf("Please enter:\n1 for base64 to hex\n2 for hex to base64\n");
  scanf("%d",&decision);

  if(decision==1){
    printf("Please enter your base64 string\n");
  }else if(decision==2){
    printf("Please enter your hex string\n");
  }else{
    printf("Wrong input\n");
    return -1;
  }
  scanf("%1023s",matasano_intern_2014);

  if(decision==1){
    base64_to_hex(matasano_intern_2014);
  }else if(decision==2){
    hex_to_base64(matasano_intern_2014);
  }

  printf("\n");
  return 0;
}