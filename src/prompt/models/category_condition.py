from dataclasses import dataclass, field


# Represents a category containing prompts
@dataclass
class CategoryCondition:
    #If condition is active
    active: bool = False
    # If true, all tags and categories need to be present, otherwise only one, so a or condition
    and_condition: bool = True
    # Negates the condition
    negative: bool = False
    # Single tags to look for
    tags: list[str] = field(default_factory=list)
    # Category names to look for
    categories: list[str] = field(default_factory=list)
