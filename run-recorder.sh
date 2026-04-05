#!/bin/bash

# configuration
PROJECT_FOLDER="/home/<!! INSERT USERNAME HERE !!>/animotion"
OUTPUT_FOLDER="${PROJECT_FOLDER}/output/"
IMAGE_OUTPUT_FOLDER="${OUTPUT_FOLDER}/wait/"
VIDEO_OUTPUT_FOLDER="${OUTPUT_FOLDER}/observe/"

# initialization
LOG_FILE="${OUTPUT_FOLDER}"/$(date --iso-8601="ns").log
source "${PROJECT_FOLDER}/.venv/bin/activate"

# run recorder
recorder \
    --video-output-folder "${VIDEO_OUTPUT_FOLDER}" \
    --image-output-folder "${IMAGE_OUTPUT_FOLDER}" \
    >> "${LOG_FILE}" \
    2>&1



