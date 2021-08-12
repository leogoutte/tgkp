# if you don't have -DINTELMKL in the f90 flags, please remove all sparse related files below
# like sparse.o, landau_level_sparse.o, lanczos_sparse.o
obj =  module.o eigen.o readinput.o gen_hk.o \
       ek_bulk.o main.o

# compiler
#f90  = gfortran  -cpp 
#fcheck =   -ffree-line-length-0 -g -Wextra  -Wconversion -fimplicit-none -fbacktrace -ffree-line-length-0 -fcheck=all -ffpe-trap=zero,overflow,underflow -finit-real=nan
#flag = -O3 ${fcheck} #-nogen-interface #  -warn all 

# export DYLD_LIBRARY_PATH=/opt/intel/oneapi/mkl/2021.2.0/lib/:$DYLD_LIBRARY_PATH

f90  = gfortran -cpp -static-libgfortran
FLAGS =  -O3 #-nogen-interface  
flag = ${FLAGS}  # -check all -traceback -pg

# blas and lapack libraries
#libs = -L/opt/intel/oneapi/mkl/2021.2.0/lib/ \
		-lmkl_intel_lp64 -lmkl_sequential \
		-lmkl_core     
# libs = -L/usr/local/lib/ -llapack
libs = /usr/local/lib/libblas.a /usr/local/lib/liblapack.a
#libs = /Users/leogoutte/Documents/lapack-3.10.0/liblapack.a

 
main :  $(obj)
	$(f90) $(obj) -o tg_kpgen $(libs) 
#cp tg_kpgen  ../../bin

.SUFFIXES: .o .f90

.f90.o :
	$(f90) -c $(flag) $(includes) $*.f90

clean :
	rm -f *.o *.mod *~ tg_kpgen
