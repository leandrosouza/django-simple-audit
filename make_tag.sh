#!/bin/bash

VERSION=$(grep "version = " setup.py  | cut -d "=" -f2 | cut -d "'" -f2)

echo "VERSION: ${VERSION}"

if ! git tag | grep $VERSION | grep -v grep > /dev/null;
then
    echo "TAG ${VERSION} does not exists!"
    git tag ${VERSION}
    git push --tags
    git push
else
    echo "TAG ${VERSION} already exists!"
fi