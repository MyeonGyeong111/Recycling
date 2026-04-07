from pydantic import BaseModel

class PredictionResponse(BaseModel):
    category: str
    confidence: float
    message: str

class CategoryInfo(BaseModel):
    category: str
    description: str
    how_to_recycle: str

class LocationRequest(BaseModel):
    latitude: float | None = None
    longitude: float | None = None
    address: str | None = None

class GuidelinesResponse(BaseModel):
    jurisdiction: str
    website_url: str
    contact_number: str | None = None
