ARG platform
FROM quay.io/pypa/${platform}

ARG highfive_version
ARG boost_version
ARG eigen_version
ARG hdf5_version
ARG libint_version
ARG gmp_version

ENV HIGHFIVE_VERSION=${highfive_version}
ENV BOOST_VERSION=${boost_version}
ENV EIGEN_VERSION=${eigen_version}
ENV HDF5_VERSION=${hdf5_version}
ENV LIBINT_VERSION=${libint_version}
ENV GMP_VERSION=${gmp_version}
ENV PATH_OLD="${PATH}"
ENV PATH="/workspace/venv/bin/:/opt/python/cp310-cp310/bin/:/opt/python/cp39-cp39/bin/:/opt/python/cp38-cp38/bin/:/opt/python/cp37-cp37/bin/:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

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
