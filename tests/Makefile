# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS= -rdynamic 
LDLIBS= -ldl

# list of source files
SRC1 = test1.c
SRC2 = test2.c
SRC3 = test3.c


VPATH=../Obj-serial/
OBJ1=$(SRC1:%.c=%.o)
OBJ2=$(SRC2:%.c=%.o)
OBJ3=$(SRC3:%.c=%.o)

default: test1.x test2.x test3.x
	./test1.x
	./test2.x
	./test3.x

clean:
	rm -f *.mod *.o *.x

# linker rule
test1.x: $(OBJ1)
	$(CC) -o $@ $(CFLAGS) $^ $(VPATH)utilities.o $(LDLIBS)

# linker rule
test2.x: $(OBJ2)
	$(CC) -o $@ $(CFLAGS) $^ $(VPATH)force.o $(VPATH)utilities.o $(LDLIBS)
	
# linker rule
test3.x: $(OBJ3)
	$(CC) -o $@ $(CFLAGS) $^ $(VPATH)force.o $(VPATH)utilities.o $(LDLIBS)


# compilation pattern rule for objects
%.o: %.c
	$(CC) -c $(CFLAGS) $<

# dependencies
#ljmd.o: ljmd.c
