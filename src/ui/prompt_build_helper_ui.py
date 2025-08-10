from modules.ui_extra_networks import ExtraNetworksPage


class PromptBuildHelperUi(ExtraNetworksPage):
    def __init__(self):
        super().__init__("PBH")


    def refresh(self):
        pass

    def list_items(self):
        raise NotImplementedError

    def create_item(self, name: str, index: int = -1, *arg, **kwarg):
        pass