//TODO
// free everything

#include "6.h"
#include "C6base64tohex.h"
#include "solveSingleXOR.h"

double lowest_sum = 1000000;
double sum;

int main(){
	int block_size;
	FILE *fp;
	char buff64[4096];
	char buff_hex[6144];
	char string_a[82];
	char string_b[82];
	long int q;
	int keysize;


	fp = fopen("gistfile1.txt", "r");

	if(fp == NULL)
		exit(1);

	size_t ghi = fread (buff64, 1, 4096, fp);

	// Let us get rid of that shit at the EOF
	buff64[ghi] = 0;

	// Newlines were in file
	removeChar(buff64, '\n');

	base64_to_hex(buff64, buff_hex);


// Get keysize and lowest_sum
	// +=2 because were talking nibbles
	for (block_size = 4; block_size < 81; block_size+=2){
		
		sum = 0;

		for(q=0; q<strlen(buff_hex); q+=(block_size*2)){
			// Put first block_size bytes in string_a 0-3
			strncpy(string_a, &buff_hex[q], block_size);

			// Put next block_size bytes in string_b  4-7
			strncpy(string_b, &buff_hex[q+block_size], block_size);

			sum += hamstrings(string_a, string_b);

			memset(&string_a[0], 0, sizeof(string_a));
			memset(&string_b[0], 0, sizeof(string_b));
		}

		// lets say strlen is 47
		// 6 is block_size
		// 6-6. 6-6. 6-6 6-5. = 47 so we got 1 nibble  
		// 47 mod 6 is 5
		// 6-5 is 1
		// hence, strlen(buff_hex)-(block_size - (strlen(buff_hex)%block_size));
		// 40 mod 8 is zero
		// 8-8 8-8 8-?
		// we need to minus by 8
		// WORKS
		// worked because it was even
		// 47 mod 6 is 5
		// 6-1
		// WORKS
		// worked because it was over
		// 42
		// 5-5 5-5 5-5 5-5 2-
		// 5 - 2
		// 3
		// SHOULD BE 2
		// didn't work because it wasn't over
		// 35
		// 8-8 8-8 3-
		// should be 3 not 5

		// if over
		if(strlen(buff_hex)%(block_size*2) >= block_size)
			sum /= ( strlen(buff_hex)  - (block_size - (strlen(buff_hex)%block_size)) /2);
		else
			sum /= ( (strlen(buff_hex) - (strlen(buff_hex)              %block_size)) /2);
		

		// Keep track of predicted key size so far
		if(sum < lowest_sum){
				keysize = block_size;
				lowest_sum = sum;
		}
		
	}

/*
malloc a two dimensional array of [( strlen(buff_hex) / keysize) + 1][( strlen(buff_hex) / keysize) + 1]
string is "fjdklsarieofjvm"
keysize 3
0369
147..
258..
*/
// Number of rows is keysize and length of rows is (( strlen(buff_hex) / keysize) + 1)

	// We have a hex buff which is 2 chars for meaning
	// We need a 2d array for char[2] so really a 3 dimensional array	
	

	// This will be the x in [keysize][x][2]
	int row_length = ( strlen(buff_hex) / keysize) + 1;

	// This will be the actual 3d arr
	char ***holy_crap = (char ***) malloc(keysize * sizeof(char **));
	

	// I never thought I'd use a 3d array in the field
	int matasano_intern_2014;
	int idk=0;
	for(matasano_intern_2014=0; matasano_intern_2014<keysize; matasano_intern_2014++){
		holy_crap[matasano_intern_2014] = (char **) malloc(row_length * (sizeof(char*)));
		for(idk=0; idk < row_length; idk++){
			holy_crap[matasano_intern_2014][idk] = (char *) calloc(1, sizeof(char)*2);
		}
	}
	
	// initialize the values 
	int column;
	int row;
	int zeroORone;
	int index=0;
	for(column=0; column < row_length; column++)
		for(row=0; row < keysize; row++)
			for(zeroORone = 0; zeroORone < 2; zeroORone++){
				if(index == strlen(buff_hex))
					holy_crap[row][column][zeroORone] = '\0';
				else{
					char seperate = buff_hex[index];
					holy_crap[row][column][zeroORone] = seperate; 
					index++;
				}
			}
		
	

	char *each_row = calloc(row_length*2*sizeof(char)+1, 1);
	int cigital_sucks;
	int matasano_is_awesome;

	char **message = malloc(keysize * sizeof(char*));
	for(cigital_sucks=0; cigital_sucks<keysize; cigital_sucks++)
		message[cigital_sucks] = calloc(row_length*2*sizeof(char)+1, 1);
	

	for(cigital_sucks=0; cigital_sucks<keysize; cigital_sucks++){
		each_row = memset(each_row, 0,sizeof(each_row));

		for(matasano_is_awesome=0; matasano_is_awesome < row_length; matasano_is_awesome++)
			strcat(each_row, holy_crap[cigital_sucks][matasano_is_awesome]);
		
		// Pass array of row_length and have it be filled NEED 2D ARRAY
		find_xor_key_with_print(each_row, message[cigital_sucks]);
	}

 	int rowz;
 	int columnz;
 	for(columnz=0; columnz < row_length; columnz++)
 		for(rowz=0; rowz < keysize; rowz++)
 			if(message[rowz][columnz]!='\0')
 				printf("%c", message[rowz][columnz]);

	return 0;
}

double hamstrings(char *string_a, char *string_b){
	int i;
	int total_dist=0;
	char char_a;
	char char_b;

	for (i = 0; i < strlen(string_b); i++){
		char_a = string_a[i];
		char_b = string_b[i];
		total_dist += hamchars(char_a, char_b);
	}

	return total_dist;
}

int hamchars(char char_a, char char_b){
	int i;
	int ham=0;
	int nib_a[4];
	int nib_b[4];

	// Turn chars into nibbles 
	turn_char_to_nib(nib_a, (int)char_a);
	turn_char_to_nib(nib_b, (int)char_b);

	// Go through bits, if they differ, ham++
	for(i=0; i<4; i++)
		if(nib_a[i] != nib_b[i])
	 		ham++;
	
	return ham;
}

void turn_char_to_nib(int *nib, int char_value){
	int i;
	int bit_value=8;
	
	// Change first hex char to decimal int
	if(       (char_value < 58)  && (47 < char_value) ){
		char_value -=48;
	}else if( (char_value < 103) && (96 < char_value) ){
		char_value -= 87;
	}else if( (char_value < 71) && (64 < char_value) ){
		char_value -= 55;
	}else{
		printf("Invalid input at %d because of char_value %d\n", __LINE__, char_value);
		exit(-1);
	}

	for(i=0; i<4; i++){
		if(char_value >= bit_value){
	 		nib[i]=1;
			char_value -= bit_value;
		}else
			nib[i]=0;
		bit_value /= 2;
	}
}

void removeChar(char *str, char garbage){

    char *src, *dst;
    for(src = dst = str; *src != '\0'; src++){
        *dst = *src;
        if (*dst != garbage) dst++;
    }

    *dst = '\0';
}