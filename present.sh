#!/bin/bash

set -eu

if [ $# -ne 1 ]; then
    echo "Usage: $0 <presentation>"
    exit 1
fi

firefox -private-window http://localhost:8000/$1/slides.html
python3 -m http.server 8000
