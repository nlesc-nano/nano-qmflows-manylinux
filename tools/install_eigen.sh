set -euo pipefail

VERSION="$1"
PREFIX="/usr/local"

download () {
    start=$SECONDS
    echo ::group::"Download Eigen $VERSION"

    curl -s https://gitlab.com/libeigen/eigen/-/archive/$VERSION/eigen-$VERSION.tar.gz -o eigen-$EIGEN_VERSION.tar.gz
    tar -xf eigen-$VERSION.tar.gz

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

configure () {
    start=$SECONDS
    echo ::group::"Configure Eigen $VERSION"

    mv eigen-$EIGEN_VERSION/Eigen "$PREFIX"/Eigen

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

cleanup () {
    start=$SECONDS
    echo ::group::"Cleanup Eigen $VERSION files"

    rm -rf eigen-$EIGEN_VERSION
    rm eigen-$VERSION.tar.gz
    file "$PREFIX"/Eigen/*

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

download
configure
cleanup
