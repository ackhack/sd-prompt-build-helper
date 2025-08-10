from modules.script_callbacks import on_before_process, on_ui_tabs
from src.prompt.callbacks import pbh_before_process
from src.ui.callbacks import editor_ui

on_before_process(pbh_before_process)

on_ui_tabs(editor_ui)
