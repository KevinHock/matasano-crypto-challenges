all: six

six: 6.c 6.h C6base64tohex.h solveSingleXOR.h
	gcc -Wall -Werror -ggdb -o C6base64tohexH C6base64tohex.h
	gcc -Wall -Werror -ggdb -o sixH 6.h
	gcc -Wall -Werror -ggdb -o six 6.c
	gcc -Wall -Werror -ggdb -o ssX solveSingleXOR.h

clean:
	rm -f *~ *.o six sixH C6base64tohexH solveSingleXOR
