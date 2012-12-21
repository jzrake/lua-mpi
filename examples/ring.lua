
local MPI = require 'MPI'
local buffer = require 'buffer'

local sizeb = buffer.new_buffer(buffer.sizeof(buffer.int))
local rankb = buffer.new_buffer(buffer.sizeof(buffer.int))

MPI.Init()
MPI.Comm_rank(MPI.COMM_WORLD, rankb)
MPI.Comm_size(MPI.COMM_WORLD, sizeb)

local size = buffer.get_typed(sizeb, buffer.int, 0)
local rank = buffer.get_typed(rankb, buffer.int, 0)

local function ring()
   if rank == 0 then
      local message = buffer.new_buffer("here is the message")
      MPI.Send(message, #message, MPI.BYTE, rank + 1, 0, MPI.COMM_WORLD)
   else
      local num_recvb = buffer.new_buffer(buffer.sizeof(buffer.int))
      local status = MPI.Status()
      MPI.Probe(rank - 1, 0, MPI.COMM_WORLD, status)
      MPI.Get_count(status, MPI.BYTE, num_recvb)
      local num_recv = buffer.get_typed(num_recvb, buffer.int, 0)
      local message = buffer.new_buffer(num_recv)
      MPI.Recv(message, #message, MPI.BYTE, rank - 1, 0, MPI.COMM_WORLD, status)
      if rank ~= size - 1 then
	 MPI.Send(message, #message, MPI.BYTE, rank + 1, 0, MPI.COMM_WORLD)
      end
      print(string.format("rank %d got the message: %s", rank, message))
   end
end

if size == 1 then
   print('Example needs MPI size to be greater than 1')
else
   ring()
end

MPI.Finalize()
