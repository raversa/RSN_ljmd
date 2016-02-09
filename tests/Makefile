# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS= -rdynamic 
LDLIBS= -ldl

# list of source files
SRC1 = test1.c
SRC2 = test2.c
#SRC_b=first_vel.c sec_vel.c others.c force.c test_b.c
#SRC_c=others.c test_c.c
#SRC_d=inout.c test_d.c


VPATH=../Obj-serial/
OBJ1=$(SRC1:%.c=%.o)
OBJ2=$(SRC2:%.c=%.o)

default: test1.x test2.x
	./test1.x
	./test2.x

clean:
	rm -f *.mod *.o *.x

# linker rule
test1.x: $(OBJ1)
	$(CC) -o $@ $(CFLAGS) $^ $(VPATH)utilities.o $(LDLIBS)

# linker rule
test2.x: $(OBJ2)
	$(CC) -o $@ $(CFLAGS) $^ $(VPATH)force.o $(VPATH)utilities.o $(LDLIBS)


# compilation pattern rule for objects
%.o: %.c
	$(CC) -c $(CFLAGS) $<

# dependencies
#ljmd.o: ljmd.c
