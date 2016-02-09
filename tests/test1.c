#define LIBRARY_PATH ../Obj-serial

#include <dlfcn.h>
#include <stdlib.h>
#include <stdio.h>
#include "../src/_mdsys.h"
#include "../src/utilities.h"

mdsys_t get_me_three_atoms()
{
    mdsys_t sys;

    sys.natoms = 3;          // number of atoms
    sys.mass = 39.948;       // mass in AMU for the Argon
    sys.epsilon = 0.2379;    // epsilon in kcal/mol
    sys.sigma = 3.405;       // sigma in angstrom
    sys.rcut = 8.5;          // rcut in angstrom
    sys.box = 17.1580;       // box length (in angstrom)

    /* allocate memory */
    sys.rx  = (double *) malloc(sys.natoms * sizeof(double));
    sys.ry  = (double *) malloc(sys.natoms * sizeof(double));
    sys.rz  = (double *) malloc(sys.natoms * sizeof(double));
    sys.vx  = (double *) malloc(sys.natoms * sizeof(double));
    sys.vy  = (double *) malloc(sys.natoms * sizeof(double));
    sys.vz  = (double *) malloc(sys.natoms * sizeof(double));
    sys.fx  = (double *) malloc(sys.natoms * sizeof(double));
    sys.fy  = (double *) malloc(sys.natoms * sizeof(double));
    sys.fz  = (double *) malloc(sys.natoms * sizeof(double));

    /* initial velocity */
    sys.vx[0] = -1.5643224621482283e-03;
    sys.vy[0] = 4.8497508563925346e-04;
    sys.vz[0] = -4.3352481732883966e-04;

    sys.vx[1] = 4.1676710257651452e-04;
    sys.vy[1] = 2.2858522230176587e-05;
    sys.vz[1] = -6.1985040462745732e-04;

    sys.vx[2] = -7.5611349562333923e-04;
    sys.vy[2] = 4.0710138209103827e-04;
    sys.vz[2] = -4.6520198934056357e-04;

    /* initial trajectory */
    sys.rx[0] = 6.67103294321331;
    sys.ry[0] = -10.6146871435653;
    sys.rz[0] = 12.6336939877734;

    sys.rx[1] = 6.67103294321331 + 0.25 * sys.rcut;
    sys.ry[1] = -10.6146871435653 + 0.25 * sys.rcut;
    sys.rz[1] = 12.6336939877734 + 0.25 * sys.rcut;

    sys.rx[2] = 6.67103294321331 - 0.3 * sys.rcut;
    sys.ry[2] = -10.6146871435653 - 0.3 * sys.rcut;
    sys.rz[2] = 12.6336939877734 - 0.3 * sys.rcut;

    sys.epot = 0.;

    azzero(sys.fx, sys.natoms);
    azzero(sys.fy, sys.natoms);
    azzero(sys.fz, sys.natoms);

    return sys;
}

int main(int argc, char **argv)
{
    void (*force)(mdsys_t *sys); // pointer to function force
    void *handle; // handle for dynamics objects
    handle = dlopen("../lib-serial/force.so", RTLD_LAZY);

    if (handle)
    {
        mdsys_t sys = get_me_three_atoms();
        force = (void (*)(mdsys_t *sys)) dlsym(handle, "force");
        (*force)(&sys);
        dlclose(handle);

        double expected_x[3] = {-0.23337371610251,0.14024895642290,0.09312475967961};
        double expected_y[3] = {-0.23337371610251,0.14024895642290,0.09312475967961};
        double expected_z[3] = {-0.23337371610251,0.14024895642290,0.09312475967961};

        int i;
        int error = 0;
        for (i=0; i < sys.natoms; i++)
        {
            if (sys.fx[i]-expected_x[i] > 1e-10)
                error = 1;
        }
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
