from .prompt_category import PromptCategory
from dataclasses import dataclass, field


#Represents the whole config of the extension
@dataclass
class Config:
    #If the prompt should be overwritten
    active: bool = True
    #Current model in use to filter LoRAs
    base_model:str = ""
    #The categories to use in the final prompt
    categories: list[PromptCategory] = field(default_factory=list)
