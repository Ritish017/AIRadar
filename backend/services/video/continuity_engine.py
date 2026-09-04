"""
Continuity Engine (V3.3):
Maintains unified cross-shot state across Characters, Environments, Objects, Camera Grammar, Color, and Narrative Progression.
Injects concise, high-priority continuity tokens into each shot prompt without creating prompt bloat.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import uuid


class CharacterState(BaseModel):
    identity_name: str
    age_range: str
    attire: str  # e.g. "Charcoal technical blazer over clean crewneck"
    hair_and_features: str  # e.g. "Dark cropped hair, rectangular acetate eyeglasses"
    accessories: str = "None"
    current_posture: str = "Standing upright at workstation"
    emotional_state: str = "Intense analytical focus"
    facial_reference_token: str = "REF-CHAR-01"


class EnvironmentState(BaseModel):
    location_name: str
    architectural_style: str  # e.g. "Minimalist subterranean research facility"
    time_of_day: str = "Night (Interior Controlled)"
    lighting_scheme: str  # e.g. "4500K neutral diffused key light, cool cyan rim"
    primary_landmarks: List[str] = Field(default_factory=list)
    atmosphere: str = "Clean, low particulate, clear visibility"


class ObjectState(BaseModel):
    object_id: str
    name: str
    current_location: str
    physical_state: str  # e.g. "Active glowing optical link, closed chassis"
    persistent_color: str


class ContinuityMasterState(BaseModel):
    state_id: str
    project_title: str
    color_palette_lock: str  # e.g. "Matte slate #0f172a, crisp white #ffffff, electric cyan #06b6d4"
    camera_visual_grammar: str  # e.g. "Controlled documentary dolly, orthogonal framing"
    characters: Dict[str, CharacterState] = Field(default_factory=dict)
    environment: EnvironmentState
    persistent_objects: Dict[str, ObjectState] = Field(default_factory=dict)
    narrative_history: List[str] = Field(default_factory=list)
    current_scene_index: int = 1


class ContinuityInjectionPayload(BaseModel):
    shot_number: int
    concise_character_anchor: Optional[str] = None
    concise_environment_anchor: str
    concise_color_anchor: str
    prior_state_anchor: Optional[str] = None
    continuity_instruction: str


class ContinuityEngine:
    """
    Orchestrates cross-shot coherence without prompt bloat.
    """

    def initialize_state(
        self,
        title: str,
        topic: str,
        has_character: bool = False,
        character_name: Optional[str] = None,
        style_preset: str = "TECH_DOCUMENTARY"
    ) -> ContinuityMasterState:
        state_id = f"cont_{uuid.uuid4().hex[:8]}"

        char_name = character_name or "Lead AI Architect"
        characters = {}
        if has_character:
            characters[char_name] = CharacterState(
                identity_name=char_name,
                age_range="32-38 years",
                attire="Dark charcoal tailored technical blazer, matte black crewneck shirt",
                hair_and_features="Short cropped dark hair, rectangular acetate eyeglasses, neutral expression",
                accessories="Matte silver wristwatch",
                current_posture="Positioned beside computing terminal",
                emotional_state="Measured analytical authority",
                facial_reference_token=f"REF-{char_name.replace(' ', '_').upper()}"
            )

        env = EnvironmentState(
            location_name="Advanced Neural Computing Center",
            architectural_style="Modern subterranean clean facility with dark brushed carbon surfaces and glass partitions",
            time_of_day="Continuous studio illumination",
            lighting_scheme="Diffused 4500K soft overhead key light, subtle cyan edge separation",
            primary_landmarks=["Wall-sized multi-metric display panel", "Liquid-cooled compute blade rack"],
            atmosphere="Crisp particulate-free cleanroom air"
        )

        objects = {
            "compute_rack": ObjectState(
                object_id="OBJ-01",
                name="Liquid-Cooled Compute Rack",
                current_location="Left third of laboratory space",
                physical_state="Active status LEDs, clean plumbing lines",
                persistent_color="Matte obsidian black"
            )
        }

        return ContinuityMasterState(
            state_id=state_id,
            project_title=title,
            color_palette_lock="Primary: #0B0F17, Accent: #06B6D4, Surface: #1E293B, Text: #F8FAFC",
            camera_visual_grammar="Smooth mechanical dollies and locked planar views; zero random handheld shake",
            characters=characters,
            environment=env,
            persistent_objects=objects,
            narrative_history=["Project initialized"],
            current_scene_index=1
        )

    def generate_shot_continuity_anchor(
        self,
        state: ContinuityMasterState,
        shot_number: int,
        requires_character: bool = False,
        requires_specific_object: Optional[str] = None
    ) -> ContinuityInjectionPayload:
        char_anchor = None
        if requires_character and state.characters:
            char = list(state.characters.values())[0]
            char_anchor = f"LOCKED CHARACTER: {char.identity_name} ({char.hair_and_features}, wearing {char.attire}). Maintain identical facial geometry."

        env_anchor = f"LOCKED ENVIRONMENT: {state.environment.location_name} ({state.environment.lighting_scheme})."
        color_anchor = f"PALETTE LOCK: {state.color_palette_lock}."

        prior_narrative = state.narrative_history[-1] if state.narrative_history else "Opening shot"
        prior_anchor = f"CONTINUITY FROM PRIOR SHOT: Preserves spatial position and state from '{prior_narrative}'."

        combined_instruction = f"CONTINUITY CONSTRAINTS: {char_anchor + ' ' if char_anchor else ''}{env_anchor} {color_anchor} {prior_anchor}"

        return ContinuityInjectionPayload(
            shot_number=shot_number,
            concise_character_anchor=char_anchor,
            concise_environment_anchor=env_anchor,
            concise_color_anchor=color_anchor,
            prior_state_anchor=prior_anchor,
            continuity_instruction=combined_instruction.strip()
        )

    def advance_narrative(self, state: ContinuityMasterState, action_completed: str) -> None:
        state.narrative_history.append(action_completed)
        state.current_scene_index += 1


continuity_engine = ContinuityEngine()
