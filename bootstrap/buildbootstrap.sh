#!/bin/sh
if ! sassc $1 ./build/temp.css >&2; then
    exit 1
fi
postcss ./build/temp.css --no-map --use autoprefixer cssnano -o "$2" >&2