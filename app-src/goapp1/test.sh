#!/bin/sh

go test -v -json ./... > /app/out/tests.json && \
go test -coverprofile=/app/out/coverage.out ./...
