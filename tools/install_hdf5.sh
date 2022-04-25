set -euo pipefail

VERSION="$1"
VERSION_SHORT="${HDF5_VERSION%.*}"
PREFIX="$2"
N_PROC="$3"

download () {
    start=$SECONDS
    echo ::group::"Download HDF5 $VERSION"

    curl -s https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-$VERSION_SHORT/hdf5-$HDF5_VERSION/src/hdf5-$HDF5_VERSION.tar.gz -o hdf5-$HDF5_VERSION.tar.gz
    tar -xzvf hdf5-$VERSION.tar.gz

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

configure () {
    start=$SECONDS
    echo ::group::"Configure HDF5 $VERSION"

    mkdir -p "$PREFIX"
    pushd hdf5-$VERSION
    chmod u+rx autogen.sh
    if [[ "$OSTYPE" == "darwin"* ]]; then
        ./configure --prefix="$PREFIX" --enable-build-mode=production --libdir="/usr/local/lib"
    else
        ./configure --prefix="$PREFIX" --enable-build-mode=production
    fi

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

build () {
    start=$SECONDS
    echo ::group::"Build HDF5 $VERSION"

    make -j $N_PROC
    make install
    popd

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

cleanup () {
    start=$SECONDS
    echo ::group::"Cleanup HDF5 $VERSION files"

    rm hdf5-$VERSION.tar.gz
    rm -rf hdf5-$VERSION
    file "$PREFIX"/*

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

download
configure
build
cleanup
