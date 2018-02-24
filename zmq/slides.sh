#!/bin/bash

pandoc -i slides.md -t revealjs -s --self-contained -o slides.html
