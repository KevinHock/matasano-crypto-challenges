//TODO GET INPUT
//ASSUMED NO CAPS IN HEX

/*
2. Fixed XOR

Write a function that takes two equal-length buffers and produces
their XOR sum.

The string:

 1c0111001f010100061a024b53535009181c

... after hex decoding, when xor'd against:

 686974207468652062756c6c277320657965

... should produce:

 746865206b696420646f6e277420706c6179
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void xor_sum(int *, int *);
void fill_nib(char, int*);
void print_nib(int *);

int main(){
	printf("Please enter your first string:\n");

	char first_buff[1024];
	scanf("%1023s",first_buff);

	printf("Please enter your second string:\n");
	char second_buff[1024];
	scanf("%1023s",second_buff);	

	int	nib_a[4],nib_b[4];
	int matasano_intern_2014;
	for(matasano_intern_2014=0; matasano_intern_2014<strlen(first_buff); matasano_intern_2014++){
		fill_nib(first_buff[matasano_intern_2014],  nib_a);
		fill_nib(second_buff[matasano_intern_2014], nib_b);
		xor_sum(nib_a, nib_b);
	}
	printf("\n");
}

void xor_sum(int *nib_a, int *nib_b){
	int nib_sum[4];
	int i;

	for(i=0; i<4; i++){
		nib_sum[i] = (nib_a[i] + nib_b[i]) % 2;
	}

	print_nib(nib_sum);
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

//0xCHAR?
void fill_nib(char c_digit, int *nib){
	int value =8;
	int i_digit = (int)c_digit;;
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