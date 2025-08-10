from modules.processing_class import StableDiffusionProcessing
from ..log_helper import pbh_log_console, pbh_log_prompt
from .prompt_builder import pbh_get_prompt_builder


def pbh_before_process(param: StableDiffusionProcessing):
    prompts = pbh_get_prompt_builder().pbh_generate_prompts()
    if prompts is not None:
        if len(prompts[0]) > 0:
            pbh_log_console("Changing positive prompt to " + prompts[0])
            pbh_log_prompt("Positive: " + prompts[0])
            param.prompt = prompts[0]
        if len(prompts[1]) > 0:
            pbh_log_console("Changing negative prompt to " + prompts[1])
            pbh_log_prompt("Negative: " + prompts[1])
            param.negative_prompt = prompts[1]
    else:
        pbh_log_console("No Prompt found, not changing")
