ARG PLATFORM
ARG HIGHFIVE_VERSION
ARG BOOST_VERSION
ARG EIGEN_VERSION
ARG HDF5_VERSION
ARG LIBINT_VERSION
ARG GMP_VERSION

FROM quay.io/pypa/${PLATFORM}

ENV HIGHFIVE_VERSION=${HIGHFIVE_VERSION}
ENV BOOST_VERSION=${BOOST_VERSION}
ENV EIGEN_VERSION=${EIGEN_VERSION}
ENV HDF5_VERSION=${HDF5_VERSION}
ENV LIBINT_VERSION=${LIBINT_VERSION}
ENV GMP_VERSION=${GMP_VERSION}
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
RUN cp -r /workspace/licenses /usr/local/licenses

RUN rm -rf /workspace
ENV PATH="${PATH_OLD}"
ENV PATH_OLD=""
