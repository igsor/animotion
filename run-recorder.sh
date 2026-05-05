#!/bin/bash

# configuration
PROJECT_FOLDER="/home/<!! INSERT USERNAME HERE !!>/animotion"
OUTPUT_ROOT="${PROJECT_FOLDER}/output/"

# initialization
source "${PROJECT_FOLDER}/.venv/bin/activate"
OUTPUT_FOLDER=$(output_tree "${OUTPUT_ROOT}")
mkdir -p "${OUTPUT_FOLDER}" 2>/dev/null

# define output folder structure
IMAGE_OUTPUT_FOLDER="${OUTPUT_FOLDER}/wait/"
VIDEO_OUTPUT_FOLDER="${OUTPUT_FOLDER}/observe/"
LOG_FILE="${OUTPUT_FOLDER}"/$(date --iso-8601="ns").log

# run recorder
recorder \
    --video-output-folder "${VIDEO_OUTPUT_FOLDER}" \
    --image-output-folder "${IMAGE_OUTPUT_FOLDER}" \
    >> "${LOG_FILE}" \
    2>&1



