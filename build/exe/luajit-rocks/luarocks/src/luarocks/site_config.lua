local site_config = {}

site_config.LUAROCKS_PREFIX=[[/home/vagneron/torch/install/]]
site_config.LUA_INCDIR=[[/home/vagneron/torch/install/include]]
site_config.LUA_LIBDIR=[[/home/vagneron/torch/install/lib]]
site_config.LUA_BINDIR=[[/home/vagneron/torch/install/bin]]
site_config.LUA_INTERPRETER = [[luajit]]
site_config.LUAROCKS_SYSCONFDIR=[[/home/vagneron/torch/install/etc/luarocks]]
site_config.LUAROCKS_ROCKS_TREE=[[/home/vagneron/torch/install/]]
site_config.LUAROCKS_ROCKS_SUBDIR=[[lib/luarocks/rocks]]
site_config.LUA_DIR_SET = true
site_config.LUAROCKS_UNAME_S=[[Linux]]
site_config.LUAROCKS_UNAME_M=[[x86_64]]
site_config.LUAROCKS_DOWNLOADER=[[wget]]
site_config.LUAROCKS_MD5CHECKER=[[md5sum]]

return site_config
