#!/bin/bash

echo publishing UDP ports
docker service update --publish-add 12000-13000:12000-13000/udp "$service_name"
docker service inspect super-efficient-key-store | jq -e '.[0].Spec.TaskTemplate.Placement.Constraints | .[] | select(. == "node.hostname==challenges-1")' || \
  docker service update --constraint-add 'node.hostname==challenges-1' "$service_name"
