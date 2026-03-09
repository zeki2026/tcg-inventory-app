from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.gemini_service import gemini_service
from app.dependencies import get_current_user
from app.models.models import User

router = APIRouter()

@router.post("/analyze")
async def analyze_card(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    content = await file.read()
    result = await gemini_service.analyze_card_image(content)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result
