#!/bin/bash

protoc --proto_path=proto --python_out=build/gen proto/bakdata/corporate/v1/corporate.proto

# Generates our Schema

protoc --proto_path=proto --python_out=build/gen proto/student/academic/v1/transparency.proto
