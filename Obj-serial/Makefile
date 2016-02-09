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
	rm -f *.mod *.o ../ljmd-serial.x

../ljmd-serial.x: $(OBJ)
	$(CC) -o $@ $(CFLAGS) ../src/ljmd.c $^ $(LDLIBS)

# compilation pattern rule for objects
%.o: %.c
	$(CC) $(CFLAGS) -shared $(LDLIBS) $^ -o $@

ljmd.o: ljmd.c
	$(CC) $(CFLAGS) -shared $(LDLIBS) $< -o $@

utilities.o: utilities.c
	$(CC) $(CFLAGS) -shared $(LDLIBS) $< -o $@

force.o: force.c utilities.o
	$(CC) $(CFLAGS) -shared $(LDLIBS) $< -o $@

