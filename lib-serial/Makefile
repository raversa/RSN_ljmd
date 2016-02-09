# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS=-Wall -g -O3 -ffast-math -fomit-frame-pointer -fPIC -shared -Wno-unused-result
LDLIBS=-lm

# list of source files
SRC=force.c utilities.c get_a_line.c output.c velverlet1.c velverlet2.c
VPATH=../src
SRDLIB=$(SRC:%.c=%.so)

default: all

clean:
	rm -f *.so

all: $(SRDLIB)

force.so: force.c utilities.so
	$(CC) $(CFLAGS) -shared $(LDLIBS) $< -o $@

%.so: %.c
	$(CC) $(CFLAGS) -shared $(LDLIBS) $^ -o $@


