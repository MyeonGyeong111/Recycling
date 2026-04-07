from fastapi import APIRouter, File, UploadFile, Depends
from app.schemas.recycle import PredictionResponse, CategoryInfo, LocationRequest, GuidelinesResponse
from app.services.recycle_service import RecycleService

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_recycle_category(file: UploadFile = File(...)):
    """
    Simulated MLOps prediction endpoint.
    Takes an image upload and returns a prediction of the recycling category.
    """
    # Read image contents
    contents = await file.read()
    
    # Send to ML service
    result = await RecycleService.predict_image(contents)
    
    return PredictionResponse(**result)

@router.get("/info/{category}", response_model=CategoryInfo)
async def get_recycle_info(category: str):
    """
    Returns information on how to recycle a specific waste category.
    Examples: PLASTIC, PAPER, GLASS, VINYL, CAN, GENERAL
    """
    info = RecycleService.get_category_info(category)
    return CategoryInfo(**info)

@router.post("/guidelines", response_model=GuidelinesResponse)
async def get_local_guidelines(location: LocationRequest):
    """
    Returns the web page and contact number for the relevant local jurisdiction
    based on the provided address or location.
    """
    data = location.model_dump()
    guidance = RecycleService.get_guidelines_for_location(data)
    return GuidelinesResponse(**guidance)
