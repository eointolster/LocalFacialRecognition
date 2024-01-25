FROM postgres:16

# Set the locale
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

# Install pgvector
RUN apt-get update -y && apt-get install -y --fix-missing \
    build-essential \
    git \
    postgresql-server-dev-all \
 && git clone https://github.com/ankane/pgvector.git \
 && cd pgvector \
 && make \
 && make install

# Set up default database and user (customize as needed)
ENV POSTGRES_DB facial_recognition
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD timney

# Expose the PostgreSQL port
EXPOSE 5432

# Set the default command for the container to run PostgreSQL
CMD ["postgres"]
