#define LIBRARY_PATH ../Obj-serial

#include <dlfcn.h>
#include <stdlib.h>
#include <stdio.h>
#include "../src/_mdsys.h"

int main(int argc, char **argv)
{
    int nprint, i;

    mdsys_t sys;

    int (*func_to_be_tested)(FILE *fp, char *buf); // pointer to function
    void *handle; // handle for dynamics objects
    handle = dlopen("../lib-serial/get_a_line.so", RTLD_LAZY);

    if (handle)
    {
        func_to_be_tested = (int (*)(FILE *fp, char *buf)) dlsym(handle, "get_a_line");

        char line[200];

        if(func_to_be_tested(stdin,line)) return 1;
        sys.natoms=atoi(line);
        if(func_to_be_tested(stdin,line)) return 1;
        sys.mass=atof(line);
        if(func_to_be_tested(stdin,line)) return 1;
        sys.epsilon=atof(line);
        if(func_to_be_tested(stdin,line)) return 1;
        sys.sigma=atof(line);
        if(func_to_be_tested(stdin,line)) return 1;
        sys.rcut=atof(line);
        if(func_to_be_tested(stdin,line)) return 1;
        sys.box=atof(line);
        if(func_to_be_tested(stdin,line)) return 1;
        sys.nsteps=atoi(line);
        if(func_to_be_tested(stdin,line)) return 1;
        sys.dt=atof(line);
        if(func_to_be_tested(stdin,line)) return 1;
        nprint=atoi(line);
        
        int error = 0;

        if (sys.natoms != 108)
            error = 1;
        if (sys.mass != 39.948)
            error = 1;
        if (sys.epsilon != 0.2379)
            error = 1;
        if (sys.sigma != 3.405)
            error = 1;
        if (sys.rcut != 8.5)
            error = 1;
            
        if (error == 0)
            printf("test passed\n");
        else
            printf("test failed\n");

    }
    else
    {
        return 1;
    }

    return 0;
}
