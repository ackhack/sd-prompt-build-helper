import gradio as gr
from .gradio import js
from ..config_manager import pbh_get_config_manager
from ..log_helper import pbh_log_console

def editor_ui():
    with gr.Blocks() as TAGS_EDITOR:
        with gr.Row():
            save_btn = gr.Button("Save", variant="primary", interactive=False)
            load_btn = gr.Button("Load")

        gr.HTML('<div id="pbh-editor"></div>')

        with gr.Row(visible=False):
            tags = gr.Textbox(elem_id="pbh-editor-box")
            real_save_btn = gr.Button("Save Real", elem_id="pbh-editor-btn")

        save_btn.click(fn=None, **js("() => { PbhEditor.save(); }"))
        real_save_btn.click(fn=save, inputs=[tags])
        load_btn.click(fn=load, outputs=[tags]).success(
            fn=lambda: gr.update(interactive=True),
            outputs=[save_btn],
            **js("() => { PbhEditor.load(); }"),
        )

    return [(TAGS_EDITOR, "PBH Editor", "sd-webui-pbh-editor")]


def load() -> str:
    return pbh_get_config_manager().pbh_get_config_as_string()


def save(json_str: str):
    #TODO remove this when ui finished
    pbh_log_console("saving: " + json_str)
    if True:
        return
    pbh_get_config_manager().pbh_save_config_from_string(json_str)
