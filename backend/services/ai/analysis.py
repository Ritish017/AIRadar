import logging
from typing import Dict, Any, Optional
from backend.services.ai.gemini_provider import gemini_provider
from backend.schemas.content import AnalysisSchema

logger = logging.getLogger(__name__)

class AIAnalysisService:
    """
    Cognitive Analysis Service powered by Google Gemini.
    Deconstructs viral mechanics, hook psychology, key claims, and multi-source verification.
    """

    def __init__(self):
        self.provider = gemini_provider

    async def analyze_content_item(self, item: Dict[str, Any]) -> AnalysisSchema:
        return await self.provider.analyze_content(item)

ai_analysis_service = AIAnalysisService()
