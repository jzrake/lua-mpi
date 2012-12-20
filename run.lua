
local MPI = require 'MPI'
local buffer = require 'buffer'

local size = buffer.new_buffer(buffer.sizeof(buffer.int))
local rank = buffer.new_buffer(buffer.sizeof(buffer.int))

MPI.Init()
MPI.Comm_rank(MPI.COMM_WORLD, rank)
MPI.Comm_size(MPI.COMM_WORLD, size)

local comm = MPI.MPI_Comm()
assert(type(comm) == 'userdata')

print(buffer.get_typed(rank, buffer.int, 0))
print(buffer.get_typed(size, buffer.int, 0))

MPI.Finalize()
