#!/usr/bin/env bash
set -e

cmake --build ./build
./build/sensor_processing_test
./build/sensor_processing