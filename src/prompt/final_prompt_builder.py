from .models.prompt_model import PromptModel
from .models.prompt_category import PromptCategory


class FinalPromptBuilder:

    def __init__(self):
        self.tag_collection: list[str] = []
        self.category_collection: list[str] = []

    def pbh_add_category(self, category: PromptCategory):
        if category.name not in self.category_collection:
            self.category_collection.append(category.name)

    def pbh_add_prompt(self, prompt: PromptModel, base_model: str):
        if not prompt.active:
            return
        self.pbh_add_string(prompt.prompt)
        for lora in prompt.loras:
            if lora.base_model_type == base_model:
                self.pbh_add_string(lora.name)

    def pbh_add_string(self, content: str | None):
        if content is None or len(content) == 0:
            return
        for tag in map(lambda p: p.strip(), content.strip().split(",")):
            self.__pbh_add_single_tag(tag)

    def __pbh_add_single_tag(self, tag: str):
        if tag is None or len(tag) == 0:
            return
        if tag not in self.tag_collection:
            self.tag_collection.append(tag)

    def pbh_get_current_tags(self) -> list[str]:
        return self.tag_collection

    def pbh_get_current_category_names(self) -> list[str]:
        return self.category_collection

    def pbh_get(self) -> str:
        return ", ".join(self.tag_collection)
