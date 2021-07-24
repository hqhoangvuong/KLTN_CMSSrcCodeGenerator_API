#!/bin/bash
echo "Publishing package at $1"
cd /root/swagger-codegen/out/$1
npm install
npm run build
npm publish dist --access=public
echo "Done"
