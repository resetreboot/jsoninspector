#!/bin/bash

SIZES=( 16x16 22x22 24x24 32x32 36x36 48x48 64x64 72x72 96x96 128x128 192x192 256x256 )

# If we can't find the svg, cd into res, we're
# probably being called from the root of
# the source tree
if [ ! -e jsoninspector.svg ]; then
    cd res
fi

for s in "${SIZES[@]}"; do
    echo "Creating $s image from svg" ;
    convert -background none jsoninspector.svg -resize $s jsoninspector$s.png
done
