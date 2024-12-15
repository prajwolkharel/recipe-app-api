# Use Python 3.9 based on Alpine 3.13 as the base image.
# Alpine is a minimal Linux distribution, ideal for creating small, secure containers.
FROM python:3.9-alpine3.13

# Add metadata with the maintainer label for the image.
# This label specifies who maintains the image and can be useful for tracking purposes.
LABEL maintainer = "prajwolkharel"

# Set environment variables for the Python environment:
# - ENV is typically used for custom environment variable definitions.
# - PYTHONUNBUFFERED=1 ensures that Python outputs logs directly to the terminal, which is helpful for debugging.
ENV ENV PYTHONUNBUFFERED=1

# Copy the `requirements.txt` and `requirements.dev.txt` to `/tmp` in the container.
# These are the files that list the application’s dependencies. The 'requirements.dev.txt' is for development dependencies.
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy the entire app directory into `/app` within the container.
# This includes the source code of the application.
COPY ./app /app

# Set the working directory inside the container to `/app`. This is where subsequent commands (like `RUN`, `CMD`, etc.) will be executed.
WORKDIR /app

# Expose port 8000 for the application. This makes the port accessible to other containers or the host machine.
EXPOSE 8000

# Define a build-time argument called DEV, which defaults to "false".
# This can be overridden during the build process to install additional development dependencies if needed.
ARG DEV=false

# The `RUN` instruction installs the necessary dependencies and sets up the environment:
# 1. Create a virtual environment in `/py`. This ensures that dependencies are installed in an isolated environment.
# 2. Upgrade pip to the latest version to avoid issues with outdated versions.
# 3. Install the PostgreSQL client (`postgresql-client`) needed to interact with the database.
# 4. Install build dependencies (`build-base`, `postgresql-dev`, `musl-dev`) required to build some Python packages from source (e.g., psycopg2).
# 5. Install the dependencies from the `requirements.txt` file (production dependencies).
# 6. If the `DEV` argument is set to "true", install the additional development dependencies from `requirements.dev.txt`.
# 7. Clean up the `/tmp` directory to reduce the image size by removing unnecessary files after installation.
# 8. Remove the temporary build dependencies (`.tmp-build-deps`) to keep the image lean and minimize the attack surface.
# 9. Add a non-privileged user `django-user` to improve security by running the app as a non-root user.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Set the PATH environment variable so that Python binaries are found in the `/py/bin` directory.
# This is necessary because the virtual environment is located in `/py`.
ENV PATH="/py/bin:$PATH"

# Switch to a non-privileged user (`django-user`) for running the application to enhance security.
# Running applications as a non-root user is a best practice in container security.
USER django-user
