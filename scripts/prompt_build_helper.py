from modules.script_callbacks import on_before_process, on_ui_tabs, on_image_saved
from src.prompt.callbacks import pbh_before_process, pbh_on_image_saved
from src.ui.callbacks import editor_ui

on_before_process(pbh_before_process)
on_image_saved(pbh_on_image_saved)
on_ui_tabs(editor_ui)
