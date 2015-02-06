
# ------------------------------------------------------------------------------
# lua-mpi build instructions
# ------------------------------------------------------------------------------
#
# 1. Make sure you have the MPI sources installed.
#
# 2. Create a file called Makefile.in which contains macros like these:
#
#    CC = mpicc
#    LUA_HOME = /path/to/lua-5.2.1
#
#    # Additional compile flags are optional:
#
#    CFLAGS = -Wall -O2
#    LVER = lua-5.2.1 # can be lua-5.1 or other
#
#
# 3. Optionally, you may install local Lua sources by typing `make lua`.
#
#
# 4. Run `make`.
#
# ------------------------------------------------------------------------------

MAKEFILE_IN = Makefile.in
include $(MAKEFILE_IN)

CFLAGS ?= -Wall -shared -fPIC
CURL ?= curl
UNTAR ?= tar -xvf
CD ?= cd
RM ?= rm -f
OS ?= generic
LVER ?= lua-5.2.1

LUA_I ?= -I$(LUA_HOME)/include
LUA_L ?= -L$(LUA_HOME)/lib -llua


default : main MPI.so buffer.so

lua : $(LVER)

$(LVER) :
	$(CURL) http://www.lua.org/ftp/$(LVER).tar.gz -o $(LVER).tar.gz
	$(UNTAR) $(LVER).tar.gz
	$(CD) $(LVER); $(MAKE) $(OS) CC=$(CC); \
		$(MAKE) install INSTALL_TOP=$(PWD)/$(LVER)
	$(RM) $(LVER).tar.gz

mpifuncs.c :
	python readspec.py > $@

lua-mpi.o : lua-mpi.c mpifuncs.c
	$(CC) $(CFLAGS) -c -o $@ $< $(LUA_I)

buffer.o : buffer.c
	$(CC) $(CFLAGS) -c -o $@ $< $(LUA_I)

main.o : main.c
	$(CC) $(CFLAGS) -c -o $@ $< $(LUA_I)

main : main.o lua-mpi.o buffer.o
	$(CC) -o $@ $^ $(LUA_L)

clean :
	$(RM) *.o mpifuncs.c main

MPI.so: lua-mpi.o
	$(CC) $(CFLAGS) -o $@ $< $(LUA_I) $(LUA_L)

buffer.so: buffer.o
	$(CC) $(CFLAGS) -o $@ $< $(LUA_I) $(LUA_L)

# Also remove local Lua sources
realclean : clean
	$(RM) -r $(LVER)
