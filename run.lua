
local MPI = require 'MPI'
local buffer = require 'buffer'

local size = buffer.new_buffer(buffer.sizeof(buffer.int))
local rank = buffer.new_buffer(buffer.sizeof(buffer.int))

MPI.Init()
MPI.Comm_rank(MPI.COMM_WORLD, rank)
MPI.Comm_size(MPI.COMM_WORLD, size)

local callback_types = {
   "Comm_copy_attr_function",
   "Comm_delete_attr_function",
   "Datarep_conversion_function", 
   "Datarep_extent_function",
   "Grequest_cancel_function",
   "Grequest_free_function",
   "Grequest_query_function",
   "Type_copy_attr_function",
   "Type_delete_attr_function",
   "User_function",
   "Win_copy_attr_function",
   "Win_delete_attr_function",
}
for _,v in ipairs(callback_types) do
   local f = MPI[v]()
   local mt = debug.getregistry()["MPI::"..v]
   assert(debug.getmetatable(f) == mt)
end

local comm = MPI.Comm()
assert(type(comm) == 'userdata')

assert(buffer.get_typed(rank, buffer.int, 0) == 0)
assert(buffer.get_typed(size, buffer.int, 0) == 1)

MPI.Finalize()
print(debug.getinfo(1).source, ": All tests passed")
