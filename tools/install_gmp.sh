set -e

VERSION="$1"
N_PROC="$2"
PREFIX="/usr/local"

download () {
    start=$SECONDS
    echo ::group::"Download GMP $VERSION"

    curl -Ls https://gmplib.org/download/gmp/gmp-$VERSION.tar.xz -o gmp-$VERSION.tar.xz
    tar -xf gmp-$VERSION.tar.xz

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

configure () {
    start=$SECONDS
    echo ::group::"Configure GMP $VERSION"

    mkdir -p "$PREFIX"
    pushd gmp-$VERSION
    ./configure --prefix="$PREFIX" --enable-cxx

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

build () {
    start=$SECONDS
    echo ::group::"Build GMP $VERSION"

    make -j $N_PROC
    make install
    popd

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

cleanup () {
    start=$SECONDS
    echo ::group::"Cleanup GMP $VERSION files"

    rm gmp-$VERSION.tar.xz
    rm -rf gmp-$VERSION
    file "$PREFIX"/

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

download
configure
build
cleanup
