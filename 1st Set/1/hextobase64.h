#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//TODO iteration and index the same?
//assumed no caps in hex
//

void print_bib(int *);
void hex_to_base64(char *);
void h2b64_fill_bib(int *, int *, int *, int);
void h2b64_fill_nib(char, int *);

void hex_to_base64(char *input){
	int nib_a[4], nib_b[4];
    int bib[6];
	int index=0;
    int iteration=0;
    int i;
    
	// Patterns repeat
	// 0	  1      0      1
	// AAAABB BBCCCC DDDDEE EEFFFF
	// AAAABB BBAAAA AAAABB BBAAAA

    for (i = 0; i < /*64*/strlen(input)-(strlen(input)/3); i++){
  	  h2b64_fill_nib(input[index++], nib_a);

  	  //We keep b every other time
  	  if(iteration%2!=1)
  		  h2b64_fill_nib(input[index++], nib_b);
      

  	  //How we fill depends on A and B pattern
  	  h2b64_fill_bib(bib, nib_a, nib_b, iteration++%2);

  	  print_bib(bib);
  	  fflush(NULL);
    }
}

void print_bib(int *bib){
   	//                             10        20        30        40        50        60
   	//                    1234567890123456789012345678901234567890123456789012345678901234
   	char mime_standard[]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
 	
 	int value=32;
 	int b64_index=0;
	int i;

	for(i=0; i<6; i++){
		if(bib[i])
			b64_index+=value;
		value/=2;
	}

	printf("%c", mime_standard[b64_index]);
	
	fflush(NULL);
}

void h2b64_fill_bib(int *bib, int *nib_a, int *nib_b, int a_not_first){
	if(a_not_first){
		bib[0] = nib_b[2];
		bib[1] = nib_b[3];
		bib[2] = nib_a[0];
		bib[3] = nib_a[1];
		bib[4] = nib_a[2];
		bib[5] = nib_a[3];
	}else{
		bib[0] = nib_a[0];
		bib[1] = nib_a[1];
		bib[2] = nib_a[2];
		bib[3] = nib_a[3];
		bib[4] = nib_b[0];
		bib[5] = nib_b[1];
	}
}

//0xCHAR?
void h2b64_fill_nib(char c_digit, int *nib){
	int value =8;
	int i_digit = (int) c_digit;
	int i=0;
    
	// Change hex char to decimal int
	if(      i_digit < 58  && i_digit > 47){
		i_digit-=48;
	}else if(i_digit < 103 && i_digit > 96){
		i_digit -= 87;
	}else{
		printf("Invalid input\n");
		exit(-1);
	}

	// Fill nibble
	for(i=0; i<4; i++){
		if(i_digit >=value){
			nib[i]=1;
			i_digit-=value;
		}else{
			nib[i]=0;
		}
		value/=2;
	}
}