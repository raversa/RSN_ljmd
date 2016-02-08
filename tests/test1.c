#define LIBRARY_PATH ../Obj-serial

#include <dlfcn.h>
#include <stdio.h>
#include "../src/_mdsys.h"

int main(int argc, char **argv)
{
	void (*force)(mdsys_t *sys); // pointer to function force
	void *handle; // handle for dynamics objects
	handle = dlopen("../Obj-serial/force.o", RTLD_LAZY);

	if (handle)
	{
		printf("ok!! \n");
		dlclose(handle);
	}
	return 0;
}
