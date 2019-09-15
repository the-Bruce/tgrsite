#!/bin/sh
if ! sassc "$1" "./build/$1" >&2; then
    exit 1
fi
postcss "./build/$1" --no-map --use autoprefixer cssnano -o "$2" >&2