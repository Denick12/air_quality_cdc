FROM apache/airflow:2.7.2

# Switch to root for system deps
USER root

# Install OS-level dependencies (needed for psycopg2, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements into /tmp with airflow user ownership
COPY --chown=airflow:root requirements.txt /tmp/requirements.txt

# Switch to airflow user
USER airflow

# Install Python packages and clean up
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt
