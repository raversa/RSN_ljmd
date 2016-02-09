The functions need to be compiled without the option -c so we can perform the single tests. 
To mantain the proper build-up of the final executable, we added the dependencies in the Makefile. 

To be able to run the executable, once in the directory Obj-serial: 

export LD_LIBRARY_PATH=`pwd`

To compile the tests: 

gcc -rdynamic test1.c -ldl
