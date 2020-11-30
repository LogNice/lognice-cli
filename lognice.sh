#! /bin/bash
export $(grep -v '^#' src/.env | xargs)
docker run --rm -v $(pwd):/usr/src/app/$VOLUME lognice_cli "$@"
