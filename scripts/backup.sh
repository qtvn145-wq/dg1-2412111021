#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

SRC=$1

if [ ! -d "$SRC" ]; then
    echo "Directory not found"
    exit 2
fi

mkdir -p ~/backup

TIME=$(date +%Y%m%d_%H%M%S)

NAME=$(basename "$SRC")

DEST=~/backup/${NAME}_${TIME}.tar.gz

tar -czf "$DEST" "$SRC"

echo "$(date '+%Y-%m-%d %H:%M:%S') -> $DEST" >> logs/backup.log

echo "Backup saved: $DEST"