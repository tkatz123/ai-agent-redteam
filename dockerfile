# Use Python 3.11 slim as a lightweight base
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps: build tools (for any wheels), make (for your Makefile), and certs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential make curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip/setuptools/wheel first
RUN python -m pip install --upgrade pip setuptools wheel

# Copy project metadata first for better layer caching
# (If you also have README.md or LICENSE referenced by pyproject, copy them too)
COPY pyproject.toml ./

# Copy the rest of your source (src/, scripts/, poisoned_site/, Makefile, etc.)
# so we can do an editable install (or a standard install) from the project root
COPY . .

# Install your project and all dependencies from pyproject.toml
# If your pyproject uses setuptools or hatch/poetry-core, this will work.
# For dev/editable installs, you can switch to: pip install -e .
RUN pip install .

# Default env for strict runs (you can override at `docker run`)
ENV CONSENT_MODE=always

# Default command: run the short demo and build the static dashboard
# Assumes you have `demo` and `dashboard` targets in your Makefile
CMD ["/bin/bash", "-lc", "make demo && make dashboard && ls -la data/dashboard && echo 'Dashboard ready at data/dashboard/index.html'"]
