from modules.script_callbacks import on_before_process, on_before_ui, on_ui_tabs
from modules.ui_extra_networks import register_page
from src.prompt.callbacks import pbh_before_process
from src.ui.prompt_build_helper_ui import PromptBuildHelperUi
from src.ui.callbacks import editor_ui

on_before_process(pbh_before_process)

on_before_ui(lambda: register_page(PromptBuildHelperUi()))

on_ui_tabs(editor_ui)
