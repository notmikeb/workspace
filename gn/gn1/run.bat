gn gen out
ninja -C out -t commands
ninja -C out

echo "out\hello_world.exe from tools\gn\tutorial\hello.c"

echo "\\.gn is the build configure"
echo "it include the \\build\buildconfig.gn"
echo "and then use //build/toolchain:gcc"

echo "build target will use default \\build.gn"
echo "\\build.gn"
echo "this example will deps \\tools\gn\tutorial\build.gn"
echo "and then build a hello_world.exe from hello.c"

out\hello_world.exe
