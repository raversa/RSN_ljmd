# -*- Makefile -*-
SHELL=/bin/sh
CC=mpicc
MPICC=mpicc
CFLAGS=-Wall -g -O3 -ffast-math -fomit-frame-pointer -Wno-unused-result
LDLIBS=-lm

# list of source files
SRC=ljmd.c force.c utilities.c get_a_line.c output.c velverlet1.c velverlet2.c
VPATH=../src-parallel
OBJ=$(SRC:%.c=%.o)

default: ../ljmd-parallel.x

clean:
	rm -f *.mod *.o ../ljmd-parallel.x

../ljmd-parallel.x: $(OBJ)
	$(MPICC) -o $@ $(CFLAGS) $^ $(LDLIBS)

# compilation pattern rule for objects
%.o: %.c
	$(CC) -c $(CFLAGS) -fPIC $(LDLIBS) $^

ljmd.o: ljmd.c
