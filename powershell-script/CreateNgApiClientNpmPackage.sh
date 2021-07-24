#!/bin/bash
echo "Creating API client for file $1"

cd /root/swagger-codegen
./run-in-docker.sh generate -i ./user_api_swagger/$1 -l typescript-angular -o /gen/out/api-client-$2 --additional-properties npmName=@hqhoangvuong/api-client-$2,snapshot=true,ngVersion=5.0.0
echo "Done."
