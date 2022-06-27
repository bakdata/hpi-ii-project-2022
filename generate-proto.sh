#!/bin/bash

# RB
protoc --proto_path=./proto --python_out=. proto/bakdata/rb/announcement/v1/announcement.proto \
 proto/bakdata/rb/person/v1/person.proto \
 proto/bakdata/rb/corporate/v1/corporate.proto


# BaFin
protoc --proto_path=./proto --python_out=. proto/bakdata/bafin/trade/v1/trade.proto \
 proto/bakdata/bafin/person/v1/person.proto \
 proto/bakdata/bafin/corporate/v1/corporate.proto

# Error
protoc --proto_path=./proto --python_out=. proto/bakdata/common/error/v1/crawl_error.proto
