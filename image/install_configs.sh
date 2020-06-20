#!/bin/bash
set -e
source /build/buildconfig
set -x


if [ $# -eq 0 ]; then
    echo "No arguments supplied"
    services=( nginx uwsgi )
else
    services=("${@}")
fi

for service in "${services[@]}"; do
    service_dir=/etc/service/$service
    if [ "$service" == "nginx" ]; then
        rm /etc/nginx/sites-enabled/default
        cp /build/config/nginx /etc/nginx/sites-enabled/
    fi
    mkdir $service_dir
    cp /build/services/$service $service_dir/run
    chmod +x $service_dir/run
done
