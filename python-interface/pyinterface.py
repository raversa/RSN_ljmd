import numpy as np
import ctypes as ct
import sys as sys
import fileinput as fi


class mdsys_t(ct.Structure):
	_fields_ = [("natoms", ct.c_int),
		    ("mass", ct.c_double),
		    ("epsilon", ct.c_double),
		    ("sigma", ct.c_double),
		    ("rcut", ct.c_double),
		    ("box", ct.c_double),
		    ("nsteps", ct.c_int),
		    ("dt", ct.c_double),
		    ("nfi", ct.c_int),
		    ("rx", ct.c_double),
		    ("ry", ct.c_double),
		    ("rz", ct.c_double),
		    ("vx", ct.c_double),
		    ("vy", ct.c_double),
		    ("vz", ct.c_double),
		    ("fx", ct.c_double),
		    ("fy", ct.c_double),
		    ("fz", ct.c_double)]





inp_var = []
for line in fi.input():
	inp_var.append(line.split()[0])


sys = mdsys_t()

sys.natoms = int(inp_var[0])
sys.mass = float(inp_var[1])
sys.epsilon = float(inp_var[2])
sys.sigma = float(inp_var[3])
sys.rcut = float(inp_var[4])
sys.box = float(inp_var[5])
sys.nsteps = int(inp_var[9])
sys.dt = float(inp_var[10])
sys.nfi = int("0")

restfile = inp_var[6]
trajfile = inp_var[7]
ergfile = inp_var[8]





print sys.natoms
print sys.mass
print sys.epsilon
print sys.sigma
print sys.rcut
print sys.box
print sys.nsteps
print sys.dt
print "sys.nfi", sys.nfi
print restfile, type(restfile)
print trajfile, type(trajfile)
print ergfile, type(ergfile)






