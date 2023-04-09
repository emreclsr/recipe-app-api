#!/bin/sh

set -e

# environment substitute
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g "deamon off;"