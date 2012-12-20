
import json
import os


class LuaType(object):
    def __init__(self, name, default=0):
        self.name = name
        self.default = default
    def push_new(self):
        funcs = (
"""
static void luampi_push_%(mname)s(lua_State *L, %(name)s arg)
{
  *((%(name)s*) lua_newuserdata(L, sizeof(%(name)s))) = arg;
  luaL_setmetatable(L, "MPI::%(sname)s");
}
static int _%(mname)s(lua_State *L)
{
  luampi_push_%(mname)s(L, %(default)s);
  return 1;
}""" % {'name': self.name,
        'sname': self.name.replace('MPI_', ''),
        'mname': self.name.replace('*', '_ptr'),
        'default': self.default})
        print funcs,

    def newmetatable(self):
        print """  luaL_newmetatable(L, "MPI::%s"); lua_pop(L, 1);""" % self.name[4:]

    def setfuncs_list(self):
        print """    {"%(mname)s", _%(mname)s},""" % {
            'mname': self.name.replace('*', '_ptr')}


class LuaFunction(object):
    def __init__(self, spec):
        self.arg_names = [a['name'] for a in spec['args']]
        self.arg_types = [a['type'] for a in spec['args']]
        self.func_name = spec['name']
        self.ret_type = spec['retVal']

    def write(self):
        func = (
            """
static int h5lua_%(func_name)s(lua_State *L)
{
  %(lua_args)s
  %(ret_type)s res = %(func_name)s(%(arg_list)s);
  %(ret_statement)s
  return 1;
}""" % { 'func_name': self.func_name,
         'lua_args': '',
         'ret_type': self.ret_type,
         'arg_list': '',
         'ret_statement': '' })
        print func,


type_names = [
    'MPI_Aint',
    'MPI_Comm',
    'MPI_Comm_copy_attr_function*',
    'MPI_Comm_delete_attr_function*',
    #'MPI_Comm_errhandler_function*',
    'MPI_Datarep_conversion_function*',
    'MPI_Datarep_extent_function*',
    'MPI_Datatype',
    'MPI_Errhandler',
    'MPI_File',
    #'MPI_File_errhandler_function*',
    'MPI_Grequest_cancel_function*',
    'MPI_Grequest_free_function*',
    'MPI_Grequest_query_function*',
    'MPI_Group',
    'MPI_Info',
    'MPI_Offset',
    'MPI_Op',
    'MPI_Request',
    'MPI_Status*',
    'MPI_Type_copy_attr_function*',
    'MPI_Type_delete_attr_function*',
    'MPI_User_function*',
    'MPI_Win',
    'MPI_Win_copy_attr_function*',
    'MPI_Win_delete_attr_function*', ]
    #'MPI_Win_errhandler_function*' ]


descr = {'MPI_Comm': {'NULL': 'MPI_COMM_NULL'},
         'MPI_Op': {'NULL': 'MPI_OP_NULL'},
         'MPI_Group': {'NULL': 'MPI_GROUP_NULL'},
         'MPI_Datatype': {'NULL': 'MPI_DATATYPE_NULL'},
         'MPI_Request': {'NULL': 'MPI_REQUEST_NULL'},
         'MPI_Errhandler': {'NULL': 'MPI_ERRHANDLER_NULL'}}


for tname in type_names:
    lua_type = LuaType(tname, default=descr.get(tname, {'NULL':0})['NULL'])
    #lua_type.newmetatable()
    lua_type.push_new()
    #lua_type.setfuncs_list()


#for line in open('specs/constants.txt'):
#    print line.strip()+';\n',
