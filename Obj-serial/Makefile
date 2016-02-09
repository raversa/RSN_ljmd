# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS=-Wall -g -O3 -ffast-math -fomit-frame-pointer -fPIC -Wno-unused-result
LDLIBS=-lm

# list of source files
SRC=force.c utilities.c get_a_line.c output.c velverlet1.c velverlet2.c
VPATH=../src
OBJ=$(SRC:%.c=%.o)

default: ../ljmd-serial.x

clean:
	rm -f *.o ../ljmd-serial.x

../ljmd-serial.x: $(OBJ)
	$(CC) -o $@ $(CFLAGS) ../src/ljmd.c $^ $(LDLIBS)

%.o: %.c
	$(CC) -c $(CFLAGS) $(LDLIBS) $^ -o $@

