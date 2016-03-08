//Made ' ' count in my letter frequency to make "Ieeacdm*GI-y*fcao*k*zedn*el*hkied" incorrect

//Must be even number of chars in the string
//Must only be lower case in hex string 
//
/*
3. Single-character XOR Cipher

The hex encoded string:

      1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt
the message.


Write code to do this for you.
How?
Devise some method for "scoring" a piece of English plaintext.
(Character frequency is a good metric.)
Evaluate each output and choose the one with the best score.
Tune your algorithm until this works.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int  get_byte_value(int *);
int  xor_and_get_value(int *, int *);
void fill_byte_by_nibs(int *, char, char);
void fill_byte_by_value(int *, int);

//Assume most frequent letters will appear more than less frequent letters
int main(){
	int value;
	char buff[1024];
	int byte[8];
	int key_byte[8];
	int byte_index;
	int letter_index;
	int sum=0;
	int best_sum=0;
	char letter;
	int key;
	int best_key;
	char best_char_key;
	char chars[27] = "e taoinshrdlcumwfgypbvkjxqz";
	int  freqs[27] = {13, 10, 9, 8, 7, 7, 7, 6, 6, 6, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0};
	//				  e  t  a  o  i  n  s  h  r  d  l  c  u  m  w  f  g  y  p  b  v  k  j  x  q  z
	//				  13 9  8  7  7  7  6  6  6  4  4  3  3  3  2  2  2  2  2  1  1  1  0  0  0  0 

	printf("Please enter your hex encoded string:\n");
	scanf("%1023s",buff);

	printf("\nstrlen is %zu\n\n", strlen(buff));

	//Loop Keys
	for(key=0; key<128; key++){

		//if(/*key == 82 ||*/ key == 114 || key == 94 || key == 126 || key == 88 || key == 120){
		//	key++;
		//}

		//Loop Bytes
		for (byte_index = 0; byte_index < strlen(buff); byte_index+=2){

			// Turn two chars into byte
			fill_byte_by_nibs(byte, buff[byte_index], buff[byte_index+1]);
			
			//Turn key into byte
			fill_byte_by_value(key_byte, key);

			// Get decimal value of the xor sum
			value = xor_and_get_value(byte, key_byte);
			

			// Add to the sum
			if( ( (64<value) && (91>value) ) || ( (96<value) && (123>value) ) || (value==32)){
				if( (value > 64) && (91 > value) )
					value+=32;
				
				letter = (char) value;
				
				for(letter_index=0; letter_index<27; letter_index++)
					if(letter == chars[letter_index])
						sum+=freqs[letter_index];
			}
		}

		// Save Key
		if(sum > best_sum){
			best_sum = sum;
			best_key = key;
		}

		sum = 0;
	}

	best_char_key = (char)best_key;
	printf("The key is '%c'\nWith a score of %d\nThe decrypted message is:\n", best_char_key, best_sum);

	// Decrypt the message
	// 1. Turn best_key into byte
	fill_byte_by_value(key_byte, best_key);

	// 2. Loop Bytes and print them
	for (byte_index = 0; byte_index < strlen(buff); byte_index+=2){

		fill_byte_by_nibs(byte, buff[byte_index], buff[byte_index+1]);

		value = xor_and_get_value(byte, key_byte);

		printf("%c", (char)value);
	}

	printf("\n");

	printf("Chicago intern 2014\n");
	return 0;
}

void fill_byte_by_nibs(int *byte, char char_a, char char_b){
	int value =8;
	int char_value_a = (int) char_a;
	int char_value_b = (int) char_b;
	int i=0;
    
	// Change first hex char to decimal int
	if(       (char_value_a < 58)  && (47 < char_value_a) ){
		char_value_a -=48;
	}else if( (char_value_a < 103) && (96 < char_value_a) ){
		char_value_a -= 87;
	}else{
		printf("Invalid input\n");
		exit(-1);
	}

	// Change second hex char to decimal int
	if(       (char_value_b < 58)  && (47 < char_value_b) ){
		char_value_b -=48;
	}else if( (char_value_b < 103) && (96 < char_value_b) ){
		char_value_b -= 87;
	}else{
		printf("Invalid input\n");
		exit(-1);
	}

	// Fill most significant nibble
	for(i=0; i<4; i++){
		if(char_value_a >=value){
			byte[i]=1;
			char_value_a-=value;
		}else{
			byte[i]=0;
		}
		value/=2;
	}

	value = 8;

	// Fill least significant nibble
	for (;i<8; i++){
		if( char_value_b >= value){
			byte[i]=1;
			char_value_b -= value;
		}else{
			byte[i]=0;
		}
		value/=2;
	}
}

void fill_byte_by_value(int *byte, int value){
	int i;
	int bit_value=128;

	// Fill byte
	for(i=0; i<8; i++){
		if(value >= bit_value){
			byte[i]=1;
			value -= bit_value;
		}else{
			byte[i]=0;
		}
		bit_value /= 2;
	}
}

int xor_and_get_value(int *byte_a, int *byte_b){
	int final_byte[8];
	int i;

	for(i=0; i<8; i++)
		final_byte[i] = (byte_a[i] + byte_b[i]) % 2;
	
	return get_byte_value(final_byte);
}

int get_byte_value(int *byte){
	int bit_value = 128;
	int value=0;
	int i;

	for(i=0; i<8; i++){
		if(byte[i])
			value+=bit_value;
		bit_value/=2;
	}

	return value;
}