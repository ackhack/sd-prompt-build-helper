from .lora_def import LoraDef

#Represents a single prompt
class PromptModel:
    #Name of prompt
    name: str
    #The actual prompt
    prompt: str
    #If prompt is used in generation
    active: bool
    #LoRA definitions in different base models
    loras: list[LoraDef]
