FILE(REMOVE_RECURSE
  "lj_vm.S"
  "lj_ffdef.h"
  "lj_bcdef.h"
  "lj_libdef.h"
  "lj_recdef.h"
  "lj_folddef.h"
  "vmdef.lua"
  "CMakeFiles/libluajit.dir/src/ljamalg.c.o"
  "CMakeFiles/libluajit.dir/lj_vm.S.o"
  "libluajit.pdb"
  "libluajit.so"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang ASM C)
  INCLUDE(CMakeFiles/libluajit.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
