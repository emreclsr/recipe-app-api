#!/bin/sh

# eğer bir komut crash olursa diğerine devam etme hata ver ve çık
set -e

python manage.py wait_for_db
# tüm statik dosyaları static files directory'e koyacak
python manage.py collectstatic --noinput
python manage.py migrate

# uwsgi django app klasörü altındaki wsgi.py'a ulaşacak
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi