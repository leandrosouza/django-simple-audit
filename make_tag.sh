#!/bin/bash

VERSION=$(grep "version = " setup.py  | cut -d "=" -f2 | cut -d "'" -f2)

echo $VERSION

if ! git tag | grep $VERSION | grep -v grep;
then
    echo "TAG ${VERSION} does not exists!"
    git tag ${VERSION}
    git push --tags
    git push
fi