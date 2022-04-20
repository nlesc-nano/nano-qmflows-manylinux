set -euo pipefail

VERSION="$1"
PREFIX="/usr/local"

download () {
    start=$SECONDS
    echo ::group::"Download HighFive $VERSION"

    curl -Ls https://github.com/BlueBrain/HighFive/archive/refs/tags/v$VERSION.tar.gz -o highfive-$VERSION.tar.gz
    tar -xf highfive-$VERSION.tar.gz

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

configure () {
    start=$SECONDS
    echo ::group::"Configure HighFive $VERSION"

    mv HighFive-$VERSION/include/* "$PREFIX"/

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

cleanup () {
    start=$SECONDS
    echo ::group::"Cleanup HighFive $VERSION files"

    rm highfive-$VERSION.tar.gz
    rm -rf HighFive-$VERSION
    file "$PREFIX"/*

    echo ::endgroup::
    printf "%71.71s\n" "✓ $(($SECONDS - $start))s"
}

download
configure
cleanup
