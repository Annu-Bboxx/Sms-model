#!/bin/bash

set -e


#HOST_NAME=$(connection_param host)
#PORT=$(connection_param port)
#DATABASE_NAME=$(connection_param dbname)
#USERNAME=$(connection_param username)
#PASSWORD=$(connection_param password)

#rm /tmp/file.txt

docker run -v /Users/annukajla/Documents/sms_modelling:/app/data/predictions sms_modelling:latest -ngu "togo" -target "local"
#	--env HOST_NAME=$HOST_NAME \
#	--env PORT=$PORT \
#	--env DATABASE_NAME=$DATABASE_NAME \
#	--env USERNAME=$USERNAME \
#	--env PASSWORD=$PASSWORD \

#	  -ngu $1 \
#	  -target $2
