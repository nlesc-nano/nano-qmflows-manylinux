ARG PLATFORM

FROM quay.io/pypa/${PLATFORM}

ENV HIGHFIVE_VERSION=2.4.1
ENV BOOST_VERSION=1.79.0
ENV EIGEN_VERSION=3.4.0
ENV HDF5_VERSION=1.12.2
ENV LIBINT_VERSION=2.7.1
ENV GMP_VERSION=6.2.1
ENV PATH_OLD="${PATH}"
ENV PATH="/workspace/venv/bin/:/opt/python/cp310-cp310/bin/:${PATH}"

COPY . /workspace

RUN python -m venv /workspace/venv
RUN pip install -e /workspace/
RUN python /workspace/tools/install_highfive.py $HIGHFIVE_VERSION --prefix=/usr/local
RUN python /workspace/tools/install_boost.py $BOOST_VERSION --prefix=/usr/local
RUN python /workspace/tools/install_eigen.py $EIGEN_VERSION --prefix=/usr/local
RUN python /workspace/tools/install_gmp.py $GMP_VERSION --prefix=/usr/local
RUN python /workspace/tools/install_hdf5.py $HDF5_VERSION --prefix=/usr/local
RUN python /workspace/tools/install_libint.py $LIBINT_VERSION --prefix=/usr/local

RUN rm -rf /workspace
ENV PATH="${PATH_OLD}"
ENV PATH_OLD=""
