FROM python:3.9-alpine3.13
LABEL maintainer="Emre CALISIR"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# DEV parametresi false verildi yani sadece Dockerfile çalışırsa production'daymış gibi olacak ama
# development sırasında docker-compose'da bu parametre true olacağından burası true olacaktır.
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # add dependecies for psycopg2 (postgresql adapter)
    apk add --update --no-cache postgresql-client jpeg-dev &&\
    # kurulum tamamlandıktan sonra ihtiyacımız olmayan paketleri tmp-build-deps olarak grupluyoruz
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    # if DEV true requirements.dev.txt'yi yükle
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    # artık ihtiyacımız olmayan paketleri siliyoruz
    apk del .tmp-build-deps &&\
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    # media ve static dosyalar için klasör açıyoruz
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    # açılan klasörlerin sahipliğini değiştirme
    chown -R djnago-user:djnago-user /vol && \
    chmod -R 755 /vol

# root user'ı kullanmak istemediğimiz için yeni bir user oluşturuyoruz.

ENV PATH="/py/bin:$PATH"

USER django-user