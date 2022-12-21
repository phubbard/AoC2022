#!/bin/bash

echo "Generating..."
python3 15.py
echo "Building..."
gcc master_15.c -O2 -o master_15.exe
echo "Running..."
./master_15.exe
echo "Done, no errors."



