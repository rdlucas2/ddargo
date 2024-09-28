#!/bin/sh

# Ensure the output directory exists
mkdir -p /app/out

# Run pytest with coverage and output results to /app/out
pytest --cov=./ --cov-report=xml:/app/out/coverage.xml --junitxml=/app/out/tests.xml

sed -i 's|<source>/app|<source>.|g' /app/out/coverage.xml
