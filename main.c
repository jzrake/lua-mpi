
#include <mpi.h>
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"

#include "mpifuncs.c"

static int _MPI_Init(lua_State *L)
{
  int ret = MPI_Init(0, MPI_ARGVS_NULL);
  lua_pushnumber(L, ret);
  return 1;
}
static int _MPI_Finalize(lua_State *L)
{
  int ret = MPI_Finalize();
  lua_pushnumber(L, ret);
  return 1;
}
static int _MPI_Comm_size(lua_State *L)
{
  MPI_Comm comm = *((MPI_Comm*) luaL_checkudata(L, 1, "MPI::Comm"));
  int *size = (int*) lua_touserdata(L, 2); luaL_checktype(L, 2, LUA_TUSERDATA);
  int ret = MPI_Comm_size(comm, size);
  lua_pushnumber(L, ret);
  return 1;
}
static int _MPI_Comm_rank(lua_State *L)
{
  MPI_Comm comm = *((MPI_Comm*) luaL_checkudata(L, 1, "MPI::Comm"));
  int *rank = (int*) lua_touserdata(L, 2); luaL_checktype(L, 2, LUA_TUSERDATA);
  int ret = MPI_Comm_rank(comm, rank);
  lua_pushnumber(L, ret);
  return 1;
}

static void register_constants(lua_State *L)
{
  luampi_push_MPI_Comm(L, MPI_COMM_WORLD); lua_setfield(L, -2, "COMM_WORLD");
  lua_pushnumber(L, MPI_SUCCESS); lua_setfield(L, -2, "MPI_SUCCESS");
}

int luaopen_buffer(lua_State *L);
int luaopen_mpi(lua_State *L)
{
  luaL_Reg mpi_types[] = {
    {"MPI_Aint", _MPI_Aint},
    {"MPI_Comm", _MPI_Comm},
    {"MPI_Comm_copy_attr_function_ptr", _MPI_Comm_copy_attr_function_ptr},
    {"MPI_Comm_delete_attr_function_ptr", _MPI_Comm_delete_attr_function_ptr},
    {"MPI_Datarep_conversion_function_ptr", _MPI_Datarep_conversion_function_ptr},
    {"MPI_Datarep_extent_function_ptr", _MPI_Datarep_extent_function_ptr},
    {"MPI_Datatype", _MPI_Datatype},
    {"MPI_Errhandler", _MPI_Errhandler},
    {"MPI_File", _MPI_File},
    {"MPI_Grequest_cancel_function_ptr", _MPI_Grequest_cancel_function_ptr},
    {"MPI_Grequest_free_function_ptr", _MPI_Grequest_free_function_ptr},
    {"MPI_Grequest_query_function_ptr", _MPI_Grequest_query_function_ptr},
    {"MPI_Group", _MPI_Group},
    {"MPI_Info", _MPI_Info},
    {"MPI_Offset", _MPI_Offset},
    {"MPI_Op", _MPI_Op},
    {"MPI_Request", _MPI_Request},
    {"MPI_Status_ptr", _MPI_Status_ptr},
    {"MPI_Type_copy_attr_function_ptr", _MPI_Type_copy_attr_function_ptr},
    {"MPI_Type_delete_attr_function_ptr", _MPI_Type_delete_attr_function_ptr},
    {"MPI_User_function_ptr", _MPI_User_function_ptr},
    {"MPI_Win", _MPI_Win},
    {"MPI_Win_copy_attr_function_ptr", _MPI_Win_copy_attr_function_ptr},
    {"MPI_Win_delete_attr_function_ptr", _MPI_Win_delete_attr_function_ptr},

    {"Comm_rank", _MPI_Comm_rank},
    {"Comm_size", _MPI_Comm_size},
    {"Init", _MPI_Init},
    {"Finalize", _MPI_Finalize},
    {NULL, NULL}};

  luaL_newmetatable(L, "MPI::Aint"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Comm"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Comm_copy_attr_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Comm_delete_attr_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Comm_errhandler_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Datarep_conversion_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Datarep_extent_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Datatype"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Errhandler"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::File"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::File_errhandler_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Grequest_cancel_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Grequest_free_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Grequest_query_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Group"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Info"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Offset"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Op"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Request"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Status*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Type_copy_attr_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Type_delete_attr_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::User_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Win"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Win_copy_attr_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Win_delete_attr_function*"); lua_pop(L, 1);
  luaL_newmetatable(L, "MPI::Win_errhandler_function*"); lua_pop(L, 1);

  lua_newtable(L);
  luaL_setfuncs(L, mpi_types, 0);
  register_constants(L);
  return 1;
}


int main(int argc, char **argv)
{
  int n;
  lua_State *L = luaL_newstate();
  luaL_openlibs(L);
  luaL_requiref(L, "MPI", luaopen_mpi, 0); lua_pop(L, 1);
  luaL_requiref(L, "buffer", luaopen_buffer, 0); lua_pop(L, 1);
 
  // Create the global `arg` table
  // ---------------------------------------------------------------------------
  lua_newtable(L);
  for (n=0; n<argc; ++n) {
    lua_pushstring(L, argv[n]);
    lua_rawseti(L, -2, n);
  }
  lua_setglobal(L, "arg");


  // Run the script
  // ---------------------------------------------------------------------------
  if (argc == 1) {
    printf("usage: main script.lua [arg1=val1 arg2=val2]\n");
  }
  else {
    if (luaL_dofile(L, argv[1])) {
      printf("%s\n", lua_tostring(L, -1));
    }
  }

  lua_close(L);
  return 0;
}
