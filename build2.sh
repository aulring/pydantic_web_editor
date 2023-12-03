#!/bin/bash

set -euo pipefail

rm -rf react_editor/build/static/*
rm -rf pydantic_web_editor/src/pydantic_web_editor/static2/*
cd react_editor
npm run build --omit=dev
cd $OLDPWD
cp -r react_editor/build/static/* pydantic_web_editor/src/pydantic_web_editor/static2/
cd pydantic_web_editor
poetry build
cd $OLDPWD