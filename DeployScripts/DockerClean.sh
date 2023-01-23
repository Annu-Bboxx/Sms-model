#!/bin/bash
printf "\n>>> Deleting stopped containers\n\n"
for c in $(docker ps -a -q); do
    docker rm $c
done

printf "\n>>> Deleting untagged images\n\n"
for i in $(docker images -q -f dangling=true); do
    docker rmi $i
done