set -euo pipefail

VERSION="$1"
PREFIX="$2"
N_PROC="$3"

download () {
    start=$SECONDS
    echo ::group::"Download Libint $VERSION"

    curl -Ls https://github.com/evaleev/libint/archive/refs/tags/v$VERSION.tar.gz -o libint-$VERSION.tar.gz
    tar -xf libint-$VERSION.tar.gz

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

configure () {
    start=$SECONDS
    echo ::group::"Configure Libint $VERSION"

    mkdir -p "$PREFIX"
    mkdir build
    pushd libint-$VERSION
    chmod u+rx autogen.sh
    ./autogen.sh
    popd
    pushd build
    if [[ "$OSTYPE" == "darwin"* ]]; then
        ../libint-$VERSION/configure --prefix="$PREFIX" --libdir="/usr/local/lib" --enable-shared=yes CXXFLAGS='-std=c++11'
    else
        ../libint-$VERSION/configure --prefix="$PREFIX" --enable-shared=yes
    fi
    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

build () {
    start=$SECONDS
    echo ::group::"Build Libint $VERSION"

    make -j $N_PROC
    make install
    popd

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

cleanup () {
    start=$SECONDS
    echo ::group::"Cleanup Libint $VERSION files"

    rm libint-$VERSION.tar.gz
    rm -rf libint-$VERSION
    rm -rf build
    file "$PREFIX"/*

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

download
configure
build
cleanup
