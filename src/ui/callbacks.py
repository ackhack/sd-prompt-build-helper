import gradio as gr
from .gradio import js
from ..config_manager import pbh_get_config_manager
from ..log_helper import pbh_log_console

def editor_ui():
    with gr.Blocks() as TAGS_EDITOR:
        gr.HTML("""
        <style>
        #pbh-btn-col {
            width: auto !important;
            position: fixed;
            border: 1px solid white;
            display: flex;
            flex-direction: row;
            border-radius: 4px;
        }
        #pbh-editor {
            margin-top: 45px;
        }
        </style>
        """)

        with gr.Row():
            with gr.Column():
                gr.HTML('<div id="pbh-editor"></div>')

            with gr.Column(elem_id="pbh-btn-col"):
                save_btn = gr.Button("Save", variant="primary", interactive=False)
                load_btn = gr.Button("Load", elem_id="pbh-editor-load-btn")


        with gr.Column(visible=False):
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
    pbh_log_console("Loading from backend")
    return pbh_get_config_manager().pbh_get_config_as_string()


def save(json_str: str):
    pbh_log_console("Saving on backend " + str(len(json_str)))
    pbh_get_config_manager().pbh_save_config_from_string(json_str)
