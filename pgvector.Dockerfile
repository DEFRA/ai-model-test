# Use a specific version of the Postgres image
FROM postgres:16.6-alpine3.21 AS pg-builder

RUN apk add git
RUN apk add build-base
RUN apk add clang clang15
RUN apk add llvm19-dev llvm19
WORKDIR /home
RUN git clone --branch v0.6.1 https://github.com/pgvector/pgvector.git
WORKDIR /home/pgvector
RUN make
RUN make install

FROM postgres:16.6-alpine3.21
COPY --from=pg-builder /usr/local/lib/postgresql/bitcode/vector.index.bc /usr/local/lib/postgresql/bitcode/vector.index.bc
COPY --from=pg-builder /usr/local/lib/postgresql/vector.so /usr/local/lib/postgresql/vector.so
COPY --from=pg-builder /usr/local/share/postgresql/extension /usr/local/share/postgresql/extension