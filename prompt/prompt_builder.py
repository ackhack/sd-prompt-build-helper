from .config_manager import pbh_get_config_manager, ConfigManager
from .models.config import Config
from .models.prompt_model import PromptModel
from .final_prompt_builder import FinalPromptBuilder
from random import randint, choices


class PromptBuilder:

    def __init__(self):
        self.config_manger: ConfigManager = pbh_get_config_manager()

    # Generate a prompts using the current config
    def pbh_generate_prompts(self):
        config = self.config_manger.pbh_get_config()
        if config is None or not config.active:
            return None
        return (self.__pbh_generate_prompt_from_config(config, "positive"),
                self.__pbh_generate_prompt_from_config(config, "negative"))

    def __pbh_generate_prompt_from_config(self, config: Config, type: str) -> str:
        final_prompt = FinalPromptBuilder()

        for category in config.categories:
            if category.type != type or not category.active:
                continue

            if not category.randomized.randomized:
                # Simple go through all prompts that are active
                for prompt in category.prompts:
                    final_prompt.pbh_add_prompt(prompt, config.base_model)
            else:
                # Calc the amount of prompt models to use
                max_mdl = category.randomized.max_prompts
                if max_mdl < 1:
                    max_mdl = len(category.prompts)
                min_mdl = category.randomized.min_prompts
                if min_mdl < 0:
                    min_mdl = 0
                if min_mdl > max_mdl:
                    min_mdl = max_mdl
                n_mdl = randint(min_mdl, max_mdl)

                # Get all active prompts and if there are more prompts then we need we randomly pick some of them
                active_prompts = self.__get_random_prompts_from_list([p for p in category.prompts if p.active], n_mdl)

                # Add them to final prompt
                for prompt in active_prompts:
                    final_prompt.pbh_add_prompt(prompt, config.base_model)

        return final_prompt.pbh_get()

    def __get_random_prompts_from_list(self, prompts: list[PromptModel], count: int) -> list[PromptModel]:
        if count >= len(prompts):
            return prompts

        res: list[PromptModel] = []
        while count > 0:
            weights = list(map(lambda p: p.weight, prompts))
            index = choices(range(len(weights)), weights=weights, k=1)[0]
            res.append(prompts[index])
            prompts.remove(prompts[index])
            count -= 1
        return res


instance = PromptBuilder()


def pbh_get_prompt_builder() -> PromptBuilder:
    return instance
