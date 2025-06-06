# Builder Stage
FROM eclipse-temurin:17-jre-alpine-3.21

ARG LIQUIBASE_VERSION=4.28.0
ARG LB_SHA256=97dd07eaca0406a09e1ae19b407eea42a7e944c7f4571922bffce71b43b75ce8

# Create setup user
RUN addgroup -g 1000 setup && \
    adduser -D -u 1000 -G setup -s /bin/sh setup && \
    chown setup:setup /home/setup

# Create directory for Liquibase
RUN mkdir /liquibase && chown setup /liquibase

# Install PostgreSQL client
RUN apk update && \
    apk add --no-cache \
    bash \
    curl \
    postgresql-client \
    wget

# Download and install Liquibase
WORKDIR /liquibase

RUN wget -q -O liquibase-${LIQUIBASE_VERSION}.tar.gz "https://github.com/liquibase/liquibase/releases/download/v${LIQUIBASE_VERSION}/liquibase-${LIQUIBASE_VERSION}.tar.gz" && \
    echo "$LB_SHA256 *liquibase-${LIQUIBASE_VERSION}.tar.gz" | sha256sum -c - && \
    tar -xzf liquibase-${LIQUIBASE_VERSION}.tar.gz && \
    rm liquibase-${LIQUIBASE_VERSION}.tar.gz && \
    ln -s /liquibase/liquibase /usr/local/bin/liquibase && \
    liquibase --version

# Set LIQUIBASE_HOME environment variable
ENV LIQUIBASE_HOME=/liquibase

# Copy main script to the image
COPY ./run-setup.sh /run-setup.sh

RUN chmod +x /run-setup.sh

# Set user and group
USER setup:setup

WORKDIR /

ENTRYPOINT ["/run-setup.sh"]
