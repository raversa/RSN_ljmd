from sys import argv
import numpy as np
from os.path import dirname
from os import chdir
from ctypes import Structure, POINTER, c_double, c_int, RTLD_GLOBAL, CDLL, pointer

class Mdsys(object):
    def __init__(self, natoms, nfi, nsteps, dt, mass, epsilon, sigma, box, rcut,
                 ekin, epot, temp, r, v, f):
    
        # Create the not-so-friendly object that should be passed
        # to the C functions
        rx = r[0].ctypes.data_as(POINTER(c_double))
        ry = r[1].ctypes.data_as(POINTER(c_double))
        rz = r[2].ctypes.data_as(POINTER(c_double))
        vx = v[0].ctypes.data_as(POINTER(c_double))
        vy = v[1].ctypes.data_as(POINTER(c_double))
        vz = v[2].ctypes.data_as(POINTER(c_double))
        fx = f[0].ctypes.data_as(POINTER(c_double))
        fy = f[1].ctypes.data_as(POINTER(c_double))
        fz = f[2].ctypes.data_as(POINTER(c_double))
        
        self._cmdsys= C_Mdsys(c_int(natoms),
                              c_int(nfi),
                              c_int(nsteps),
                              c_double(dt),
                              c_double(mass),
                              c_double(epsilon),
                              c_double(sigma),
                              c_double(box),
                              c_double(rcut),
                              c_double(ekin),
                              c_double(epot),
                              c_double(temp),
                              rx,
                              ry,
                              rz,
                              vx,
                              vy,
                              vz,
                              fx,
                              fy,
                              fz)
     
        self.r = r
        self.v = v
        self.f = f

    @property
    def natoms(self):
        return self._cmdsys.natoms
    @natoms.setter
    def natoms(self, value):
        self._cmdsys.natoms = c_int(value)

    @property
    def nfi(self):
        return self._cmdsys.nfi
    @nfi.setter
    def nfi(self, value):
        self._cmdsys.nfi = c_int(value)

    @property
    def nsteps(self):
        return self._cmdsys.nsteps
    @nsteps.setter
    def nsteps(self, value):
        self._cmdsys.nsteps = c_int(value)

    @property
    def dt(self):
        return self._cmdsys.dt
    @dt.setter
    def dt(self, value):
        self._cmdsys.dt = c_double(value)

    @property
    def mass(self):
        return self._cmdsys.mass
    @mass.setter
    def mass(self, value):
        self._cmdsys.mass = c_double(value)

    @property
    def epsilon(self):
        return self._cmdsys.epsilon
    @epsilon.setter
    def epsilon(self, value):
        self._cmdsys.epsilon = c_double(value)

    @property
    def sigma(self):
        return self._cmdsys.sigma
    @sigma.setter
    def sigma(self, value):
        self._cmdsys.sigma = c_double(value)

    @property
    def box(self):
        return self._cmdsys.box
    @box.setter
    def box(self, value):
        self._cmdsys.box = c_double(value)

    @property
    def rcut(self):
        return self._cmdsys.rcut
    @rcut.setter
    def rcut(self, value):
        self._cmdsys.rcut = c_double(value)

    @property
    def ekin(self):
        return self._cmdsys.ekin
    @ekin.setter
    def ekin(self, value):
        self._cmdsys.ekin = c_double(value)

    @property
    def epot(self):
        return self._cmdsys.epot
    @epot.setter
    def epot(self, value):
        self._cmdsys.epot = c_double(value)

    @property
    def temp(self):
        return self._cmdsys.temp
    @temp.setter
    def temp(self, value):
        self._cmdsys.temp = c_double(value)

    def as_ctype(self):
        return self._cmdsys


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
    mdsys = Mdsys(natoms, 0, nsteps, time_step, mass, epsilon, sigma, box_length, rcut, 0, 0, 0, positions, velocities, forces)
        
    # loading all the functions
    utilities_file = CDLL("../lib-serial/utilities.so", mode = RTLD_GLOBAL)
    azzero = lambda x: utilities_file.azzero(pointer(x))
    ekin = lambda x: utilities_file.ekin(pointer(x))
    force_file = CDLL("../lib-serial/force.so", mode = RTLD_GLOBAL)
    force = lambda x: force_file.force(pointer(x))
    velverlet1_file = CDLL("../lib-serial/velverlet1.so", mode = RTLD_GLOBAL)
    velverlet1 = lambda x: velverlet1_file.velverlet1(pointer(x))
    velverlet2_file = CDLL("../lib-serial/velverlet2.so", mode = RTLD_GLOBAL)
    velverlet2 = lambda x: velverlet2_file.velverlet2(pointer(x))
    
    ekin(mdsys.as_ctype())
    force(mdsys.as_ctype())

    print("Starting simulation...")
    print("Ekin: {:<20} Epot: {:<20} Etot: {:<20}".format(mdsys.ekin, mdsys.epot, mdsys.ekin + mdsys.epot))

    # main MD loop
    for mdsys.nfi in range(mdsys.nsteps):
        #propagate system and recompute energies
        velverlet1(mdsys.as_ctype())
        velverlet2(mdsys.as_ctype())
        ekin(mdsys.as_ctype())

    print("Simulation done")
    print("Ekin: {:<20} Epot: {:<20} Etot: {:<20}".format(mdsys.ekin, mdsys.epot, mdsys.ekin + mdsys.epot))







