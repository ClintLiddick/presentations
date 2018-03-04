#!/bin/bash

pids=()
for i in {1..7}; do
    ./client.py &
    pids[${i}]=$!
done

trap 'kill ${pids[*]}' SIGINT
wait ${pids[*]}
