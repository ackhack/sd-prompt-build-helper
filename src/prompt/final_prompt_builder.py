from .models.prompt_model import PromptModel
from .models.prompt_category import PromptCategory
from ..log_helper import pbh_log_debug

class FinalPromptBuilder:

    def __init__(self):
        self.tag_collection: list[str] = []
        self.prompt_collection: list[str] = []
        self.category_collection: list[str] = []

    def pbh_add_category(self, category: PromptCategory):
        if category.name not in self.category_collection:
            self.category_collection.append(category.name)

    def pbh_add_prompt(self, prompt: PromptModel, base_model: str):
        pbh_log_debug("Try adding " + prompt.name)
        if not prompt.active:
            pbh_log_debug(prompt.name + ": Not active")
            return
        self.prompt_collection.append(prompt.name)
        self.__pbh_add_string(prompt.prompt)
        for lora in prompt.loras:
            pbh_log_debug(prompt.name + ": Checking LoRA for " + lora.base_model_type)
            if lora.base_model_type == base_model:
                self.__pbh_add_string(lora.name)

    def __pbh_add_string(self, content: str | None):
        if content is None or len(content) == 0:
            return
        pbh_log_debug("Adding string " + content)
        for tag in map(lambda p: p.strip(), content.strip().split(",")):
            self.__pbh_add_single_tag(tag)

    def __pbh_add_single_tag(self, tag: str):
        if tag is None or len(tag) == 0:
            return
        if tag not in self.tag_collection:
            pbh_log_debug("Adding tag " + tag)
            self.tag_collection.append(tag)

    def pbh_get_current_tags(self) -> list[str]:
        return self.tag_collection

    def pbh_get_current_prompts(self) -> list[str]:
        return self.prompt_collection

    def pbh_get_current_category_names(self) -> list[str]:
        return self.category_collection

    def pbh_get(self) -> str:
        res = ", ".join(self.tag_collection)
        pbh_log_debug("Completed prompt: " + res)
        return res
