#!/bin/bash

mkdir map_python

for i in $(ls -X *.tmx)
do
	echo "$i -> ${i%%.*}.py"
	python converter "$i" doors=^ entities=?*
	cp "${i%%.*}.py" map_python/
	rm "${i%%.*}.py"
done

