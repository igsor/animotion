#!/bin/bash

# configuration
ENV_FOLDER="~/animotion/.venv/"
OUTPUT_FOLDER="~/animotion/output/"
IMAGE_OUTPUT_FOLDER="${OUTPUT_FOLDER}/wait/"
VIDEO_OUTPUT_FOLDER="${OUTPUT_FOLDER}/observe/"

# initialization
mkdir -p "${OUTPUT_FOLDER}"
LOG_FILE="${OUTPUT_FOLDER}"/$(date --iso-8601="ns").log
source "${ENV_FOLDER}/bin/activate"

# run recorder
recorder \
    --video-output-folder "${VIDEO_OUTPUT_FOLDER}" \
    --image-output-folder "${IMAGE_OUTPUT_FOLDER}" \
    >> "${LOG_FILE}" \
    2>&1



