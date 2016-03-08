#include "5.h"

int main(){
	int matasano_intern_2014;
 
	for(matasano_intern_2014=0; matasano_intern_2014 < strlen(quote); matasano_intern_2014++)
		take_char(quote[matasano_intern_2014], matasano_intern_2014);

	printf("\n");

	return 0;
}

void take_char(char current_char, int letter){
	int nib_a[4], nib_b[4];

	// Three letters in ICE
	letter %= 3;

	// Make current_char two nibbles
	fill_nibs(nib_a, nib_b, current_char);

	// XOR both nibbles
	xor_nibs(nib_a, nib_b, letter);

	// Print results
	print_nib(nib_a);
	print_nib(nib_b);
}

void print_nib(int *nib){
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

void xor_nibs(int *nib_a, int *nib_b, int letter){
	if(letter==0){
		// I = x49
		// 0100 1001

		nib_a[1] = (nib_a[1] == 1) ? 0 : 1;

		nib_b[0] = (nib_b[0] == 1) ? 0 : 1;
		nib_b[3] = (nib_b[3] == 1) ? 0 : 1;

	}else if(letter==1){
		// C = x43
		// 0100 0011

		nib_a[1] = (nib_a[1] == 1) ? 0 : 1;

		nib_b[2] = (nib_b[2] == 1) ? 0 : 1;
		nib_b[3] = (nib_b[3] == 1) ? 0 : 1;

	}else{/*letter==2*/
		// E = x45
		// 0100 0101

		nib_a[1] = (nib_a[1] == 1) ? 0 : 1;

		nib_b[1] = (nib_b[1] == 1) ? 0 : 1;
		nib_b[3] = (nib_b[3] == 1) ? 0 : 1;

	}
}

void fill_nibs(int *nib_a, int *nib_b, char current_char){
	int i;
	int bit_value=128;
	int char_as_int = (int) current_char;

	// Fill first nibble
	for(i=0; i<4; i++){
		if(char_as_int >= bit_value){
	 		nib_a[i]=1;
			char_as_int -= bit_value;
		}else
			nib_a[i]=0;
		
		bit_value /= 2;
	}

	// Fill second nibble
	for(i=0; i<4; i++){
		if(char_as_int >= bit_value){
	 		nib_b[i]=1;
			char_as_int -= bit_value;
		}else
			nib_b[i]=0;
		
		bit_value /= 2;
	}
}