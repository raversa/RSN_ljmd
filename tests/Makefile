# -*- Makefile -*-
SHELL=/bin/sh
CC=gcc
CFLAGS= -rdynamic 
LDLIBS= -ldl

# list of source files
SRC1 = test1.c
SRC2 = test2.c
SRC3 = test3.c
SRC4 = test4.c
SRC5 = test5.c


VPATH=../Obj-serial/
OBJ1=$(SRC1:%.c=%.o)
OBJ2=$(SRC2:%.c=%.o)
OBJ3=$(SRC3:%.c=%.o)
OBJ4=$(SRC4:%.c=%.o)
OBJ5=$(SRC5:%.c=%.o)

default: test1.x test2.x test3.x test4.x test5.x
	./test1.x
	./test2.x
	./test3.x
	./test4.x
	./test5.x < argon_108.inp

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
	
# linker rule
test4.x: $(OBJ4)
	$(CC) -o $@ $(CFLAGS) $^ $(LDLIBS)

# linker rule
test5.x: $(OBJ5)
	$(CC) -o $@ $(CFLAGS) $^ $(LDLIBS)


# compilation pattern rule for objects
%.o: %.c
	$(CC) -c $(CFLAGS) $<

# dependencies
#ljmd.o: ljmd.c
