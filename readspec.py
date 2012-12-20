
import json
import os


mpi_typenames = [
    'MPI_Aint',
    'MPI_Comm',
    'MPI_Comm_copy_attr_function',
    'MPI_Comm_delete_attr_function',
    #'MPI_Comm_errhandler_function',
    'MPI_Datarep_conversion_function',
    'MPI_Datarep_extent_function',
    'MPI_Datatype',
    'MPI_Errhandler',
    'MPI_File',
    #'MPI_File_errhandler_function',
    'MPI_Grequest_cancel_function',
    'MPI_Grequest_free_function',
    'MPI_Grequest_query_function',
    'MPI_Group',
    'MPI_Info',
    'MPI_Offset',
    'MPI_Op',
    'MPI_Request',
    'MPI_Status',
    'MPI_Type_copy_attr_function',
    'MPI_Type_delete_attr_function',
    'MPI_User_function',
    'MPI_Win',
    'MPI_Win_copy_attr_function',
    'MPI_Win_delete_attr_function', ]
    #'MPI_Win_errhandler_function' ]

mpi_datatypes = [
    'MPI_CHAR',
    'MPI_BYTE',
    'MPI_SHORT',
    'MPI_INT',
    'MPI_LONG',
    'MPI_FLOAT',
    'MPI_DOUBLE',
    'MPI_UNSIGNED_CHAR',
    'MPI_UNSIGNED_SHORT',
    'MPI_UNSIGNED',
    'MPI_UNSIGNED_LONG',
    'MPI_LONG_DOUBLE',
    'MPI_LONG_LONG_INT',
    'MPI_FLOAT_INT',
    'MPI_LONG_INT',
    'MPI_DOUBLE_INT',
    'MPI_SHORT_INT',
    'MPI_2INT',
    'MPI_LONG_DOUBLE_INT',
    'MPI_PACKED',
    'MPI_UB',
    'MPI_LB' ]

mpi_misc = [
    'MPI_ANY_SOURCE',
    'MPI_PROC_NULL',
    'MPI_ROOT',
    'MPI_ANY_TAG',
    'MPI_MAX_PROCESSOR_NAME',
    'MPI_MAX_ERROR_STRING',
    'MPI_MAX_OBJECT_NAME',
    'MPI_UNDEFINED',
    'MPI_CART',
    'MPI_GRAPH',
    'MPI_KEYVAL_INVALID',
]

mpi_skipfuncs = ['MPI_Pcontrol']

mpi_nullobj = {'MPI_Comm': {'NULL': 'MPI_COMM_NULL'},
               'MPI_Op': {'NULL': 'MPI_OP_NULL'},
               'MPI_Group': {'NULL': 'MPI_GROUP_NULL'},
               'MPI_Datatype': {'NULL': 'MPI_DATATYPE_NULL'},
               'MPI_Request': {'NULL': 'MPI_REQUEST_NULL'},
               'MPI_Status': {'NULL': 'NULL'},
               'MPI_Errhandler': {'NULL': 'MPI_ERRHANDLER_NULL'}}


def lua_checkarg(dt, vn, num):
    """ tn: type declaration, vn: variable name, num: arg number """
    if dt.startswith('MPI_') and dt.endswith('*'):
        if dt in mpi_typenames: # metatable name ends in *
            short = dt.replace('MPI_', '')
        else: # metatable name does not end in *
            short = dt.replace('MPI_', '').replace('*', '')
        return """%(dt)s %(vn)s = (%(dt)s) luaL_checkudata(L, %(num)d, "MPI::%(short)s");""" % {
            'dt': dt, 'vn': vn, 'num': num, 'short': short }
    elif dt.startswith('MPI_') and not dt.endswith('*'):
        if dt in mpi_typenames: # metatable name ends in *
            short = dt.replace('MPI_', '')
        else: # metatable name does not end in *
            short = dt.replace('MPI_', '').replace('*', '')
        return """%(dt)s %(vn)s = *((%(dt)s) luaL_checkudata(L, %(num)d, "MPI::%(short)s"));""" % {
            'dt': dt, 'vn': vn, 'num': num, 'short': short }
    else:
        pass#print "unrecognized:", dt
        


class LuaType(object):
    def __init__(self, name, default=0):
        self.name = name
        self.default = default
    def push_new(self):
        noptr_funcs = (
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
        'mname': self.name,
        'default': self.default})

        ptr_funcs = (
"""
static void luampi_push_%(mname)s(lua_State *L, %(name)s arg, int N)
{
  memcpy(lua_newuserdata(L, N*sizeof(%(name)s)), arg, N*sizeof(%(name)s));
  luaL_setmetatable(L, "MPI::%(sname)s");
}
static int _%(mname)s(lua_State *L)
{
  int N = lua_checkinteger(L, 1);
  luampi_push_%(mname)s(L, %(default)s, N);
  return 1;
}""" % {'name': self.name,
        'sname': self.name.replace('MPI_', ''),
        'mname': self.name.replace('*', '_ptr'),
        'default': self.default})

        if '*' in self.name:
            return ptr_funcs
        else:
            return noptr_funcs

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
        arg_list = [ ]
        arg_num = 1
        for t, n in zip(self.arg_types, self.arg_names):
            #ca = lua_checkarg(t, n, arg_num)
            #if ca: print ca
            arg_num += 1

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

      



all_types = set()

luampi_funcs = [ ]
for spec in os.listdir('specs'):
    func = LuaFunction(json.load(open('specs/' + spec)))
    if func.func_name in mpi_skipfuncs: continue
    luampi_funcs.append(func)
    for tname in func.arg_types:
        all_types.add(tname)


#for func in luampi_funcs:
    #func.write()


#print '\n'.join(sorted(all_types))


for tname in mpi_typenames:
    if 'function' in tname: print """ "%s", """ % tname
    #lua_type = LuaType(tname)
    #print lua_type.push_new()

