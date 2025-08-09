from .models.prompt_model import PromptModel


class FinalPromptBuilder:
    prompt = ""

    def pbh_add_prompt(self, prompt: PromptModel, base_model: str):
        if not prompt.active:
            return
        self.pbh_add_string(prompt.prompt)
        if hasattr(prompt, "loras"):
            for lora in prompt.loras:
                if lora.base_model_type == base_model:
                    self.pbh_add_string(lora.name)

    def pbh_add_string(self, content: str | None):
        if content is None:
            return
        content = content.strip()
        if not content.endswith(","):
            content += ","
        self.prompt += content

    def pbh_get(self) -> str:
        return ", ".join(map(lambda p: p.strip(), self.prompt.split(",")))
