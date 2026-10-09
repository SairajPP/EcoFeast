from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from ml_service import FoodQualityPredictor
import logging

app = FastAPI(title="EcoFeast ML API")
predictor = FoodQualityPredictor(auto_train=False)

class PredictionRequest(BaseModel):
    storage_time: float
    time_since_cooking: float
    storage_condition: str
    food_type: str
    temperature: Optional[float] = 25.0
    city: Optional[str] = "Mumbai"
    container_type: str
    moisture_type: str
    cooking_method: str
    texture: str
    smell: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        data = request.dict()
        prediction = predictor.predict(data, return_dict=True)
        return prediction
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
