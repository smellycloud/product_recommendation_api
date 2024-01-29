#!/bin/bash
REQUIREMENTS_FILE="requirements.txt"

ENV_NAME="product_recommendation_api"


conda create --name ${ENV_NAME} --yes --quiet

# Activate the new conda environment
source activate ${ENV_NAME}

if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -r $REQUIREMENTS_FILE
else
    echo "The file $REQUIREMENTS_FILE does not exist."
fi

# Install remaining packages
pip install uvicorn duckduckgo-search