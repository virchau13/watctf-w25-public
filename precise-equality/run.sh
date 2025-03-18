#!/bin/sh
export FLAG="$(cat flag.txt)"
cd /app
exec ./precise-equality
