#!/bin/bash

set -euo pipefail

rm -rf pydantic_web_editor/src/pydantic_web_editor/static/*
cd pydantic_web_editor_webpack
npm run build --omit=dev
cd $OLDPWD
cp -r pydantic_web_editor_webpack/statics/* pydantic_web_editor/src/pydantic_web_editor/static/
cd pydantic_web_editor
poetry build
cd $OLDPWD