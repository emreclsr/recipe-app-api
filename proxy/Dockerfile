# base image of nginx
FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="Emre CALISIR"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

# switch the user to root for set up image
USER root

    # yeni bir klasör oluşturuyor
RUN mkdir -p /vol/static && \
    # setting the permissons for read the contents
    chmod 755 /vol/static && \
    # run.sh'ta envsubst satırının yazabilmesi için bir dosya oluşturuyoruz, user'ın bu dosyaya yazma izni olmalı ki override edebilsin
    touch /etc/nginx/conf.d/default.conf && \
    # change ownership, base image'daki user olan nginx'e veriyoruz
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    # execute permission to run.sh
    chmod +x /run.sh

# bu image için default bir volume tanımlanıyor
VOLUME /vol/static

# switch user to nginx, bu user application'u çalıştırmalı
USER nginx

CMD ["/run.sh"]