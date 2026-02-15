import google.generativeai as genai
from app.config import get_settings
from PIL import Image
import io

settings = get_settings()

class GeminiService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro-vision')
        else:
            self.model = None

    async def analyze_card_image(self, image_bytes: bytes):
        if not self.model:
            return {"error": "Gemini AI not configured"}

        try:
            image = Image.open(io.BytesIO(image_bytes))
            prompt = "Analyze this trading card. Extract the Card Name, Set, and estimate the condition (Grade). Return as JSON."
            response = self.model.generate_content([prompt, image])
            return {"analysis": response.text}
        except Exception as e:
            return {"error": f"Failed to analyze image: {str(e)}"}

gemini_service = GeminiService()
