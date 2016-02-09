from sys import argv
import numpy as np
from os.path import dirname
from os import chdir
from ctypes import Structure, POINTER, c_double, c_int, RTLD_GLOBAL, CDLL

class Mdsys(object):
	def __init__(self, natoms, nfi, nsteps, dt, mass, epsilon, sigma, box, rcut, ekin, epot, temp, r, v, f):
		self.natoms = natoms
		self.nfi = nfi
		self.nsteps= nsteps
		self.dt = dt
		self.mass = mass
		self.epsilon = epsilon
		self.sigma = sigma
		self.box = box
		self.rcut = rcut
		self.ekin = ekin
		self.epot = epot
		self.temp = temp
		self.r = r
		self.v = v
		self.f = f

	def as_ctype(self):
		cmdsys= C_Mdsys()
		cmdsys.natoms = c_int(self.natoms)
		cmdsys.nfi = c_int(self.nfi)
		cmdsys.nsteps = c_int(self.nsteps)
		cmdsys.dt = c_double(self.dt)
		cmdsys.mass = c_double(self.mass)
		cmdsys.epsilon = c_double(self.epsilon)
		cmdsys.sigma = c_double(self.sigma)
		cmdsys.box = c_double(self.box)
		cmdsys.cut = c_double(self.rcut)
		cmdsys.ekin = c_double(self.ekin)
		cmdsys.epot = c_double(self.epot)
		cmdsys.temp = c_double(self.temp)
		rx = self.r[0]
		cmdsys.rx = rx.ctypes.data_as(POINTER(c_double))
		ry = self.r[1]
		cmdsys.ry = ry.ctypes.data_as(POINTER(c_double))
		rz = self.r[2]
		cmdsys.rz = rz.ctypes.data_as(POINTER(c_double))
		vx = self.v[0]
		cmdsys.vx = vx.ctypes.data_as(POINTER(c_double))
		vy = self.v[1]
		cmdsys.vy = vy.ctypes.data_as(POINTER(c_double))
		vz = self.v[2]
		cmdsys.vz = vz.ctypes.data_as(POINTER(c_double))
		fx = self.f[0]
		cmdsys.fx = fx.ctypes.data_as(POINTER(c_double))
		fy = self.f[1]
		cmdsys.fy = fy.ctypes.data_as(POINTER(c_double))
		fz = self.f[2]
		cmdsys.fz = fz.ctypes.data_as(POINTER(c_double))
		return cmdsys


class C_Mdsys(Structure):
	_fields_ = [("natoms", c_int),  
				("mass", c_double),
				("epsilon", c_double),
				("sigma", c_double),
				("rcut", c_double),
				("box", c_double),
				("nsteps", c_int),
				("dt", c_double),
				("nfi", c_int),
				("ekin", c_double),
				("epot", c_double),
				("temp", c_double),
				("rx", POINTER(c_double)),
				("ry", POINTER(c_double)),
				("rz", POINTER(c_double)),
				("vx", POINTER(c_double)),
				("vy", POINTER(c_double)),
				("vz", POINTER(c_double)),
				("fx", POINTER(c_double)),
				("fy", POINTER(c_double)),
				("fz", POINTER(c_double)),]


if __name__ == '__main__' :
	#read input file
	input_filename = argv[1]
	input_dir = dirname(input_filename)
	chdir(input_dir)
	with open(input_filename, 'r') as f:
		input_instruction = f.readlines()
	first_word = [a.split()[0] for a in input_instruction]

	natoms = int(first_word[0])
	mass = float(first_word[1])
	epsilon = float(first_word[2])
	sigma = float(first_word[3])
	rcut = float(first_word[4])
	box_length = float(first_word[5])
	restart_file = first_word[6]
	trajectory_file = first_word[7]
	energies_file = first_word[8]
	nsteps = int(first_word[9])
	time_step = float(first_word[10])
	output_frequency = int(first_word[11])

	#read restart file
	particles = np.fromfile(restart_file, sep = ' ')
	positions = particles[:3*natoms]
	velocities = particles[3*natoms:]
	positions = positions.reshape(natoms,3)
	velocities = velocities.reshape(natoms,3)

	positions = np.ascontiguousarray(positions.T)
	velocities = np.ascontiguousarray(velocities.T)

	forces = np.zeros([3,natoms])


	# mdsys = object of the Mdsys class
	mdsys = Mdsys(natoms, 0, nsteps, time_step, mass, epsilon, sigma, box_length, rcut, 0, 0, 0, positions, velocities, forces)
		
	# loading all the functions
	utilities_file = CDLL("../lib-serial/utilities.so", mode = RTLD_GLOBAL)
	azzero = utilities_file.azzero
	ekin = utilities_file.ekin
	force_file = CDLL("../lib-serial/force.so", mode = RTLD_GLOBAL)
	force = force_file.force
	
	azzero(mdsys.r[0].ctypes.data_as(POINTER(c_double)), 108)
	print(mdsys.r)

	ekin(mdsys.as_ctype())

	











