echo "BUILD STARTS HERE"
echo "ls"
ls

# Runtime data is provided by photochem_clima_data. Creating this directory
# prevents upstream's disabled test suite from downloading and moving a second
# copy across filesystems during CMake configuration.
mkdir -p data

echo "$PYTHON -m pip install . -vv"
$PYTHON -m pip install . -vv
