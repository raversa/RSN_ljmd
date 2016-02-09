Step 1. 
The python code io_par.py performs simple unit tests. 
To make it work, it needs a complete library to be in a new directory ../lib/
To obtain the library.so, just do: 

gcc -shared -o library.so *.o

in the directory ../Obj-serial/, and then move to ../lib/

