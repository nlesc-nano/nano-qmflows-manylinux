FROM quay.io/pypa/manylinux2014_aarch64

ENV HIGHFIVE_VERSION 2.3.1
ENV BOOST_VERSION 1.78.0
ENV EIGEN_VERSION 3.4.0
ENV HDF5_VERSION 1.12.1
ENV LIBINT_VERSION 2.6.0
ENV GMP_VERSION 6.2.1

COPY tools/install_highfive.sh /tmp/install_highfive.sh
COPY tools/install_boost.sh /tmp/install_boost.sh
COPY tools/install_eigen.sh /tmp/install_eigen.sh
COPY tools/install_gmp.sh /tmp/install_gmp.sh
COPY tools/install_hdf5.sh /tmp/install_hdf5.sh
COPY tools/install_libint.sh /tmp/install_libint.sh

RUN bash /tmp/install_highfive.sh $HIGHFIVE_VERSION
RUN bash /tmp/install_boost.sh $BOOST_VERSION
RUN bash /tmp/install_eigen.sh $EIGEN_VERSION
RUN bash /tmp/install_gmp.sh $GMP_VERSION 2
RUN bash /tmp/install_hdf5.sh $HDF5_VERSION 2
RUN bash /tmp/install_libint.sh $LIBINT_VERSION 2
