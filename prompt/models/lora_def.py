#Represents a LoRA string with the base model it belongs to
class LoraDef:
    #Name of the LoRA to use, e.g. <lora:akane-kurokawa-s1s2-illustriousxl-lora-nochekaiser:1.0>
    name: str
    #Name of the base model the LoRA is base on, is user inputted
    base_model_type: str
