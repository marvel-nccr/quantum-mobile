F90 = gfortran

#Add next two lines for parallel postw90. Choose the correct name of the mpi f90 wrapper
COMMS  = mpi 
MPIF90 = mpif90.openmpi

FCOPTS = -O3 -ffpe-summary=none
LDOPTS =

#=======================
# System LAPACK and BLAS
# e.g. use
#   sudo apt-get install libblas-dev liblapack-dev
# on Ubuntu
#=======================
LIBS = -llapack -lblas





