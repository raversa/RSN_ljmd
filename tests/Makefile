# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS= -rdynamic 
LDLIBS= -ldl

# list of source files
SRC1 = test1.c
#SRC_b=first_vel.c sec_vel.c others.c force.c test_b.c
#SRC_c=others.c test_c.c
#SRC_d=inout.c test_d.c


VPATH=../Obj-serial/
OBJ_a=$(SRC1:%.c=%.o)
#OBJ_b=$(SRC_b:%.c=%.o)
#OBJ_c=$(SRC_c:%.c=%.o)
#OBJ_d=$(SRC_d:%.c=%.o)

default: test1.x
	./test1.x

clean:
	rm -f *.mod *.o *.x

# linker rule
test1.x: $(OBJ_a)
	$(CC) -o $@ $(CFLAGS) $^ $(VPATH)utilities.o $(LDLIBS)


# compilation pattern rule for objects
%.o: %.c
	$(CC) -c $(CFLAGS) $<

# dependencies
#ljmd.o: ljmd.c
