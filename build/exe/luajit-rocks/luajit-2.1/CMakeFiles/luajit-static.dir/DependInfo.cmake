# The set of languages for which implicit dependencies are needed:
SET(CMAKE_DEPENDS_LANGUAGES
  "ASM"
  "C"
  )
# The set of files for implicit dependencies of each language:
SET(CMAKE_DEPENDS_CHECK_ASM
  "/home/vagneron/torch/build/exe/luajit-rocks/luajit-2.1/lj_vm.S" "/home/vagneron/torch/build/exe/luajit-rocks/luajit-2.1/CMakeFiles/luajit-static.dir/lj_vm.S.o"
  )
SET(CMAKE_ASM_COMPILER_ID "GNU")
SET(CMAKE_DEPENDS_CHECK_C
  "/home/vagneron/torch/exe/luajit-rocks/luajit-2.1/src/ljamalg.c" "/home/vagneron/torch/build/exe/luajit-rocks/luajit-2.1/CMakeFiles/luajit-static.dir/src/ljamalg.c.o"
  )
SET(CMAKE_C_COMPILER_ID "GNU")

# Preprocessor definitions for this target.
SET(CMAKE_TARGET_DEFINITIONS
  "LUAJIT_CPU_SSE2"
  "LUAJIT_ENABLE_LUA52COMPAT"
  "LUA_MULTILIB=\"lib\""
  "LUA_ROOT=\"/home/vagneron/torch/install\""
  "LUA_USE_READLINE"
  "_FILE_OFFSET_BITS=64"
  "_LARGEFILE_SOURCE"
  )

# Targets to which this target links.
SET(CMAKE_TARGET_LINKED_INFO_FILES
  )

# The include file search paths:
SET(CMAKE_C_TARGET_INCLUDE_PATH
  "../exe/luajit-rocks/luajit-2.1/src"
  "../exe/luajit-rocks/luajit-2.1/dynasm"
  "exe/luajit-rocks/luajit-2.1"
  )
SET(CMAKE_CXX_TARGET_INCLUDE_PATH ${CMAKE_C_TARGET_INCLUDE_PATH})
SET(CMAKE_Fortran_TARGET_INCLUDE_PATH ${CMAKE_C_TARGET_INCLUDE_PATH})
SET(CMAKE_ASM_TARGET_INCLUDE_PATH ${CMAKE_C_TARGET_INCLUDE_PATH})
