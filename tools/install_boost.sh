set -euo pipefail

VERSION="$1"
VERSION_UNDERSCORE="${VERSION//./_}"
PREFIX="$2"

download () {
    start=$SECONDS
    echo ::group::"Download boost $VERSION"

    curl -Ls https://boostorg.jfrog.io/artifactory/main/release/$VERSION/source/boost_$VERSION_UNDERSCORE.tar.gz -o boost_$VERSION_UNDERSCORE.tar.gz
    tar -xf boost_$VERSION_UNDERSCORE.tar.gz

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

configure () {
    start=$SECONDS
    echo ::group::"Configure Boost $VERSION"

    mv boost_$VERSION_UNDERSCORE/boost "$PREFIX"/include/boost

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

cleanup () {
    start=$SECONDS
    echo ::group::"Cleanup Boost $VERSION files"

    rm boost_$VERSION_UNDERSCORE.tar.gz
    file "$PREFIX"/boost/*

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

download
configure
cleanup
