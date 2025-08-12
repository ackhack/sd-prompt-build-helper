from ..config_manager import pbh_get_config_manager, ConfigManager
from .models.config import Config
from .models.prompt_model import PromptModel
from .models.prompt_category import PromptCategory
from .models.category_condition import CategoryCondition
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

    def __pbh_generate_prompt_from_config(self, config: Config, prompt_type: str) -> str:
        final_prompt = FinalPromptBuilder()

        for category in config.categories:
            if category.type != prompt_type or not category.active or not self.__is_category_included_by_conditions(
                    category.conditions, final_prompt):
                continue

            final_prompt.pbh_add_category(category)

            if not category.randomized.active:
                # Simple go through all prompts that are active
                for prompt in category.prompts:
                    final_prompt.pbh_add_prompt(prompt, config.base_model)
            else:
                # Calc the amount of prompt models to use
                n_mdl = self.__get_number_of_prompt_models_to_add(category)

                # Get all active prompts and if there are more prompts then we need we randomly pick some of them
                active_prompts = self.__get_random_prompts_from_list([p for p in category.prompts if p.active], n_mdl)

                # Add them to final prompt
                for prompt in active_prompts:
                    final_prompt.pbh_add_prompt(prompt, config.base_model)

        return final_prompt.pbh_get()

    def __is_category_included_by_conditions(self, condition: CategoryCondition, final: FinalPromptBuilder) -> bool:
        if not condition.active:
            return True

        if len(condition.tags) == 0 and len(condition.categories) == 0:
            return True

        added_tags = final.pbh_get_current_tags()
        added_categories = final.pbh_get_current_category_names()

        # or condition, just look if any are present and then return depending on negative condition
        if not condition.and_condition:
            for search_tag in condition.tags:
                if search_tag in added_tags:
                    return not condition.negative
            for search_category in condition.categories:
                if search_category in added_categories:
                    return not condition.negative
            return condition.negative
        # and condition, look if any is not present
        else:
            for search_tag in condition.tags:
                if search_tag not in added_tags:
                    return condition.negative
            for search_category in condition.categories:
                if search_category not in added_categories:
                    return condition.negative
            return not condition.negative

    def __get_number_of_prompt_models_to_add(self, category: PromptCategory) -> int:
        max_mdl = category.randomized.max_prompts
        if max_mdl < 1:
            max_mdl = len(category.prompts)
        min_mdl = category.randomized.min_prompts
        if min_mdl < 0:
            min_mdl = 0
        if min_mdl > max_mdl:
            min_mdl = max_mdl
        n_mdl = randint(min_mdl, max_mdl)
        return n_mdl

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
