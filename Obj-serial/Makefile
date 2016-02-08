# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS=-Wall -g -O3 -ffast-math -fomit-frame-pointer -fPIC -shared -Wno-unused-result
LDLIBS=-lm

# list of source files
SRC=ljmd.c force.c utilities.c get_a_line.c output.c velverlet1.c velverlet2.c
VPATH=../src
OBJ=$(SRC:%.c=%.o)

default: ../ljmd-serial.x

clean:
	rm -f *.mod *.o ../ljmd-serial.x

../ljmd-serial.x: $(OBJ)
	$(CC) -o $@ $(CFLAGS) $^ $(LDLIBS)

# compilation pattern rule for objects
%.o: %.c
	$(CC) -c $(CFLAGS) $(LDLIBS) $^

ljmd.o: ljmd.c
