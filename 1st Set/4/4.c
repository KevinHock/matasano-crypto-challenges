/*
4. Detect single-character XOR

One of the 60-character strings at:

  https://gist.github.com/3132713

has been encrypted by single-character XOR.
Find it. 
(Your code from #3 should help.)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "4.h"

int main(){
	char string[61];
	char best_string[61];
	int i;
	char curr_char;
	FILE *matasano_intern_2014_chicago;

	int sum;
	int best_sum=0;

	matasano_intern_2014_chicago=fopen("gistfile1.txt", "r");

	if(matasano_intern_2014_chicago==NULL)
		exit(1);

	i=0;

	while(1){
		while( (i < 60) && (curr_char != 10 || curr_char!= 13)){
			curr_char = (char) fgetc(matasano_intern_2014_chicago);

			//
			if(curr_char==EOF)
				goto done; 
			//
		
			string[i] = curr_char;
			i++;
		}
		
		fflush(NULL);
		
		string[60] = '\0';


		sum = find_xor_key(string);

		// Save the best
		if(sum > best_sum){
			best_sum=sum;

			strncpy(best_string, string, 60);

			best_string[60]=(char)0;
		}

		

		curr_char = (char) fgetc(matasano_intern_2014_chicago);
		
		while(curr_char == 10 || curr_char== 13)
			curr_char = (char) fgetc(matasano_intern_2014_chicago);

		string[0]=curr_char;
		
		if(curr_char==EOF)
			goto done; 
		
		
		i=1;
	}

	done:

	printf("Best_string is %s\n", best_string);
	find_xor_key_with_print(best_string);

	// Close file
	fclose(matasano_intern_2014_chicago);

	return 0;
}


