from .prompt_model import PromptModel
from .category_randomization import CategoryRandomization
from .category_condition import CategoryCondition
from dataclasses import dataclass, field


# Represents a category containing prompts
@dataclass
class PromptCategory:
    # Condition if category should be added or not
    conditions: CategoryCondition = field(default_factory=CategoryCondition)
    # Randomization properties of category
    randomized: CategoryRandomization = field(default_factory=CategoryRandomization)
    # Name of the category
    name: str = ""
    # If category is positive of negative
    type: str = ""
    # Prompts in this category
    prompts: list[PromptModel] = field(default_factory=list)
    # If category should be used in generation
    active: bool = True
