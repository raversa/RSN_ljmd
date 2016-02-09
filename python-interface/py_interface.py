from sys import argv
import numpy as np
from os.path import dirname
from os import chdir
from ctypes import Structure, POINTER, c_double, c_int, cdll

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
		cmdsys.natoms = self.natoms
		cmdsys.nfi = self.nfi
		cmdsys.nsteps = self.nsteps
		cmdsys.dt = self.dt
		cmdsys.mass = self.mass
		cmdsys.epsilon = self.epsilon
		cmdsys.sigma = self.sigma
		cmdsys.box = self.box
		cmdsys.cut = self.rcut
		cmdsys.ekin = self.ekin
		cmdsys.epot = self.epot
		cmdsys.temp = self.temp
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
				("nfi", c_int), 
				("nsteps", c_int),
				("dt", c_double),
				("mass", c_double),
				("epsilon", c_double),
				("sigma", c_double),
				("box", c_double),
				("rcut", c_double),
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
	mdsys = Mdsys(natoms, 0, nsteps, time_step,mass, epsilon, sigma, box_length, rcut, 0, 0, 0, positions, velocities, forces)
		
	# loading all the functions
	force_file = cdll.LoadLibrary("../lib-serial/force.so")
	force = force_file.force
	











