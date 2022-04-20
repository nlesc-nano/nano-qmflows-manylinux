set -e

VERSION="$1"

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

    mv eigen-$EIGEN_VERSION/Eigen /usr/include/

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

cleanup () {
    start=$SECONDS
    echo ::group::"Cleanup Eigen $VERSION files"

    rm boost_$BOOST_VERSION_UNDERSCORE.tar.gz

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

download
configure
cleanup
