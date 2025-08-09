from .prompt_model import PromptModel
from .category_randomization import CategoryRandomization
from dataclasses import dataclass


# Represents a category containing prompts
@dataclass
class PromptCategory:
    # Name of the category
    name: str
    # If category should be used in generation
    active: bool
    # Randomization properties of category
    randomized: CategoryRandomization
    # If category is positive of negative
    type: str
    # Prompts in this category
    prompts: list[PromptModel]
