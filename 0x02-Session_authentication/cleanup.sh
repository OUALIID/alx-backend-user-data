#!/bin/bash
# Find and remove all __pycache__ directories recursively starting from the current directory
find . -type d -name "__pycache__" -exec rm -r {} +
echo "Cleanup complete"
