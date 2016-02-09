/*
 * simple lennard-jones potential MD code with velocity verlet.
 * units: Length=Angstrom, Mass=amu; Energy=kcal
 *
 * MPI c version.
 */

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <math.h>
#include <mpi.h>


#include "constants.h"
#include "utilities.h"
#include "get_a_line.h"
#include "output.h"
#include "force.h"
#include "velverlet1.h"
#include "velverlet2.h"


void assigned_data(int natoms, int num_proc, int me, int *start_num, int *local_part)
/*
 * This function calculate how many particles should be elaborated
 * in a process if that process has rank 'me', there are 'num_proc'
 * processes and there are 'natoms' particles in the simulation
 */
{
    int first_num;
    int to_be_stored = natoms / num_proc;
    int r = natoms % num_proc;

    if(me<r)
    {
        ++to_be_stored;
        first_num = to_be_stored * me;
    } else {
        first_num = to_be_stored * me + r;
    }

    *start_num = first_num;
    *local_part = to_be_stored;
}


/* main */
int main(int argc, char **argv)
{
    int nprint, i;
    int me, n_proc;
    char restfile[BLEN], trajfile[BLEN], ergfile[BLEN], line[BLEN];
    FILE *fp,*traj,*erg;
    mdsys_t sys;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &me);
    MPI_Comm_size(MPI_COMM_WORLD, &n_proc);

    if (me==0) {

        printf("Running with %d processes.\n\n",n_proc);

        /* read input file */
        if(get_a_line(stdin,line)) return 1;
        sys.natoms=atoi(line);
        if(get_a_line(stdin,line)) return 1;
        sys.mass=atof(line);
        if(get_a_line(stdin,line)) return 1;
        sys.epsilon=atof(line);
        if(get_a_line(stdin,line)) return 1;
        sys.sigma=atof(line);
        if(get_a_line(stdin,line)) return 1;
        sys.rcut=atof(line);
        if(get_a_line(stdin,line)) return 1;
        sys.box=atof(line);
        if(get_a_line(stdin,restfile)) return 1;
        if(get_a_line(stdin,trajfile)) return 1;
        if(get_a_line(stdin,ergfile)) return 1;
        if(get_a_line(stdin,line)) return 1;
        sys.nsteps=atoi(line);
        if(get_a_line(stdin,line)) return 1;
        sys.dt=atof(line);
        if(get_a_line(stdin,line)) return 1;
        nprint=atoi(line);
    }

    /* Broadcast the information required for initialize the system
       among all the nodes */
    MPI_Bcast(&(sys.natoms), sizeof(int), MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&(sys.nsteps), sizeof(int), MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&(sys.mass), sizeof(double), MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&(sys.epsilon), sizeof(double), MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&(sys.sigma), sizeof(double), MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&(sys.rcut), sizeof(double), MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&(sys.box), sizeof(double), MPI_DOUBLE, 0, MPI_COMM_WORLD);

    /* allocate memory */
    sys.rx=(double *)malloc(sys.natoms*sizeof(double));
    sys.ry=(double *)malloc(sys.natoms*sizeof(double));
    sys.rz=(double *)malloc(sys.natoms*sizeof(double));
    sys.vx=(double *)malloc(sys.natoms*sizeof(double));
    sys.vy=(double *)malloc(sys.natoms*sizeof(double));
    sys.vz=(double *)malloc(sys.natoms*sizeof(double));
    sys.fx=(double *)malloc(sys.natoms*sizeof(double));
    sys.fy=(double *)malloc(sys.natoms*sizeof(double));
    sys.fz=(double *)malloc(sys.natoms*sizeof(double));

    azzero(sys.fx, sys.natoms);
    azzero(sys.fy, sys.natoms);
    azzero(sys.fz, sys.natoms);


    if (me==0) {
        /* read restart */
        fp=fopen(restfile,"r");
        if(fp) {
            for (i=0; i<sys.natoms; ++i) {
                fscanf(fp,"%lf%lf%lf",sys.rx+i, sys.ry+i, sys.rz+i);
            }
            for (i=0; i<sys.natoms; ++i) {
                fscanf(fp,"%lf%lf%lf",sys.vx+i, sys.vy+i, sys.vz+i);
            }
            fclose(fp);
        } else {
            perror("cannot read restart file");
            return 3;
        }
    }

    /* Broadcast the initial data */
    MPI_Bcast(sys.rx, sys.natoms * sizeof(int), MPI_INT, 0, MPI_COMM_WORLD );
    MPI_Bcast(sys.ry, sys.natoms * sizeof(int), MPI_INT, 0, MPI_COMM_WORLD );
    MPI_Bcast(sys.rz, sys.natoms * sizeof(int), MPI_INT, 0, MPI_COMM_WORLD );
    MPI_Bcast(sys.vx, sys.natoms * sizeof(int), MPI_INT, 0, MPI_COMM_WORLD );
    MPI_Bcast(sys.vy, sys.natoms * sizeof(int), MPI_INT, 0, MPI_COMM_WORLD );
    MPI_Bcast(sys.vz, sys.natoms * sizeof(int), MPI_INT, 0, MPI_COMM_WORLD );

    /* initialize forces and energies.*/
    sys.nfi=0;
    force(&sys);
    ekin(&sys);

    if (me==0){
        erg=fopen(ergfile,"w");
        traj=fopen(trajfile,"w");

        printf("Starting simulation with %d atoms for %d steps.\n", sys.natoms, sys.nsteps);
        printf("     NFI            TEMP            EKIN                 EPOT              ETOT\n");
        output(&sys, erg, traj);
    }

    /**************************************************/
    /* main MD loop */
    for(sys.nfi=1; sys.nfi <= sys.nsteps; ++sys.nfi) {

        /* write output, if requested */
        if ((sys.nfi % nprint) == 0)
            output(&sys, erg, traj);

        /* propagate system and recompute energies */
        velverlet1(&sys);
        velverlet2(&sys);
        ekin(&sys);
    }
    /**************************************************/

    /* clean up: close files, free memory */
    printf("Simulation Done.\n");
    fclose(erg);
    fclose(traj);

    free(sys.rx);
    free(sys.ry);
    free(sys.rz);
    free(sys.vx);
    free(sys.vy);
    free(sys.vz);
    free(sys.fx);
    free(sys.fy);
    free(sys.fz);

    return 0;
}
