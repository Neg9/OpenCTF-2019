#!/bin/sh
# Be sure to have jq and yq installed

# curl https://172.17.0.3:4443 -k --cipher CAMELLIA128-SHA

CIPHER="CAMELLIA128-SHA"
FLAG=$(<challenge.yaml yq -r .flags[].flag)

tmp_image_id=$(docker build . | awk '/Successfully built / {print $3}')

if [ -z "${tmp_image_id}" ]; then
	exit 1
fi

tmp_container_id=$(docker run -d "${tmp_image_id}")

service_uri=https://$(docker inspect "${tmp_container_id}" | jq -r '(.[].NetworkSettings.IPAddress) + ":" + (.[].NetworkSettings.Ports | to_entries[].key | split("/")[0])')

docker run -it "alpine:2.6" \
	"sh" "-c" \
	"apk update >/dev/null 2>&1 \
	&& apk add openssl curl >/dev/null 2>&1 \
	&& curl --verbose --insecure --cipher \"${CIPHER}\" \"${service_uri}\" \
	| grep -qF \"${FLAG}\""

# If grep found the flag, exit clean, otherwise, exit dirty
if [ 0 -eq $? ]; then
	echo "PASS: Found correct flag via HTTPS request with curl"
	exit 0
else
	echo "FAIL: Did not find correct flag via HTTPS request with curl"
	exit 1
fi
