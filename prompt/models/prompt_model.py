from .lora_def import LoraDef
from dataclasses import dataclass, field


# Represents a single prompt
@dataclass
class PromptModel:
    # Name of prompt
    name: str
    # The actual prompt
    prompt: str
    # If prompt is used in generation
    active: bool
    # LoRA definitions in different base models
    loras: list[LoraDef] = field(default_factory=list)
    # When randomized, how likely it is that this is used
    weight: int = 1
