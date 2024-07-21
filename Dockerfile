#defines the image and tag used
FROM python:3.9-alpine3.13
LABEL maintainer = "scargeo"

#prevent buffering when using docker. allows codes to run on the screen
ENV PYTHONUNBUFFERED 1

#copy the requirements into the docker image.
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
#default directory
WORKDIR /app
#acces to the image container
EXPOSE 8000

ARG DEV=false
# && \ breaks the code into parts
# creating virtual environment for the project to store dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # install postgresql client
    apk add --update --non-cache postgresql-client && \
    # download virtual dependency packages
    apk add ---update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    #condition to install dev dependencies if DEV is true
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # rm -rf /tmp removes the temporary files
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    #add new user to prevent the use of root user
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

#specify paths to run commands from the virtual environment
ENV PATH="/py/bin:$PATH"

USER django-user