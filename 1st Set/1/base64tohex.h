#include <string.h>
#include <stdio.h>
#include <stdlib.h>

void base64_to_hex(char *);
void fill_nib(int *, int *, int *, int);
void print_nib(int *);
void fill_bib(char, int *);

void base64_to_hex(char input[]){
	int bib_a[6], bib_b[6];
	int nib[4];
	int index=0;
    int iteration=0;
	int i;

  	// Patterns repeat
	// 03	4501 25	  03   4501 25   03   4501 25      
	// AAAA AABB BBBB CCCC CCDD DDDD EEEE EEFF FFFF
	// AAAA AABB BBBB AAAA AABB BBBB AAAA AABB BBBB
	
  	for (i = 0; i < strlen(input)+(strlen(input)/2); i++){
  		
  		//Every fourth time we replace A and B
  		if(iteration%3==0 || iteration==0){
  			fill_bib(input[index++], bib_a);

  			fill_bib(input[index++], bib_b);
  		}

  		//Three ways (03, 4501, 25) to fill nib 
  		fill_nib(nib, bib_a, bib_b, iteration++%3);

  		print_nib(nib);
  		fflush(NULL);
  	}
}

void fill_nib(int *nib, int *bib_a, int *bib_b, int pattern){
	if(pattern==0){
		//03
		nib[0]=bib_a[0];
		nib[1]=bib_a[1];
		nib[2]=bib_a[2];
		nib[3]=bib_a[3];
	}else if(pattern==1){
		//4501
		nib[0] = bib_a[4];
		nib[1] = bib_a[5];
		nib[2] = bib_b[0];
		nib[3] = bib_b[1];
	}else{
		//25
		nib[0] = bib_b[2];
		nib[1] = bib_b[3];
		nib[2] = bib_b[4];
		nib[3] = bib_b[5];
	}
}

void print_nib(int *nib){
	//lynda.com ajax
	int value=8;
 	int answer=0;
	int i;

	for(i=0; i<4; i++){
		if(nib[i])
			answer+=value;
		value/=2;
	}

	printf("%x", answer);
}

void fill_bib(char c_b64, int *bib){
	int value =32;
	int b64_index=-1;
	int i=0;
    
	// Change base64 char to decimal int
	// indexOf mime standard
   	//                              10        20        30        40        50        60
   	//                     1234567890123456789012345678901234567890123456789012345678901234
   	char mime_standard[]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	int indexOf;

	for(indexOf=0; indexOf < strlen(mime_standard); indexOf++){
		if(mime_standard[indexOf]==c_b64){
			b64_index=indexOf;
			break;
		}
	}
	if(b64_index==-1){
		printf("Invalid input\n");
		exit(-1);
	}

	// Fill bibble
	for(i=0; i<6; i++){
		if(b64_index >= value){
			bib[i]=1;
			b64_index-= value;
		}else{
			bib[i]=0;
		}
		value/=2;
	}
}

