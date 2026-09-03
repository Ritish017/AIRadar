import logging
from typing import List, Dict, Any, Optional
from backend.services.ai.gemini_provider import gemini_provider
from backend.schemas.content import GeneratedVariantSchema

logger = logging.getLogger(__name__)

class AIPostGenerator:
    """
    Original Post Synthesizer powered by Google Gemini.
    Generates original, high-signal X posts across 6 formats while enforcing originality safeguards.
    """

    def __init__(self):
        self.provider = gemini_provider

    async def generate_variants(
        self,
        item: Dict[str, Any],
        analysis: Optional[Dict[str, Any]] = None,
        tone: str = "technical",
        length: str = "medium",
        voice_profile: Optional[Dict[str, Any]] = None,
        angle: Optional[str] = None,
        hook_strategy: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        sharpen: bool = True
    ) -> List[GeneratedVariantSchema]:
        return await self.provider.generate_variants(
            item=item,
            analysis=analysis,
            tone=tone,
            length=length,
            voice_profile=voice_profile,
            angle=angle,
            hook_strategy=hook_strategy,
            custom_instructions=custom_instructions,
            sharpen=sharpen
        )

ai_post_generator = AIPostGenerator()
