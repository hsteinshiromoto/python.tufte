# ---
# Build arguments
# ---
ARG DOCKER_PARENT_IMAGE
FROM $DOCKER_PARENT_IMAGE

# NB: Arguments should come after FROM otherwise they're deleted
ARG BUILD_DATE

# Silence debconf
ARG DEBIAN_FRONTEND=noninteractive

ARG PROJECT_NAME
ARG PYTHON_VERSION=3.9.7

# ---
# Enviroment variables
# ---
ENV BUILD_DATE=$BUILD_DATE
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
ENV TZ Australia/Sydney
ENV SHELL=/bin/bash
ENV PYTHON_VERSION=$PYTHON_VERSION
ENV HOME=/home/$PROJECT_NAME

RUN mkdir -p $HOME
WORKDIR $HOME

COPY . $HOME

# ---
# Get poetry
# ---
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:$HOME/.poetry/bin"
ENV PATH="${PATH}:$HOME/.local/bin"

# RUN poetry config virtualenvs.create false \
#     && poetry install --no-interaction --no-ansi

ENV PATH="${PATH}:$HOME/.local/bin"
# Need for Pytest
ENV PATH="${PATH}:${PYENV_ROOT}/versions/$PYTHON_VERSION/bin"

# N.B.: Keep the order 1. entrypoint, 2. cmd

# N.B.: Keep the order entrypoint than cmd
# ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Keep the container running
CMD tail -f /dev/null