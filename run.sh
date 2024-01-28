ENV_NAME="product_recommendation_api"

source activate ${ENV_NAME}


echo "Starting FastAPI Uvicorn Server"
uvicorn main:app --reload