import os.path

from .final_prompt_builder import FinalPromptBuilder
from modules.processing_class import StableDiffusionProcessing
from ..util import pbh_get_gallery_folder


class ImageInfo:
    def __init__(self, prompt_builder: FinalPromptBuilder, prompt_type: str, param: StableDiffusionProcessing):
        self.prompt_builder = prompt_builder
        self.prompt_type = prompt_type
        self.param = param


class GallerySaver:
    infos: list[ImageInfo] = []

    def pbh_add_prompt(self, prompt_builder: FinalPromptBuilder, prompt_type: str, param: StableDiffusionProcessing):
        self.infos.append(ImageInfo(prompt_builder, prompt_type, param))

    def pbh_add_image(self, image: str, param: StableDiffusionProcessing):
        infos: list[ImageInfo] = [i for i in self.infos if i.param == param]
        for info in infos:
            self.infos.remove(info)
            # only save positive prompts
            if info.prompt_type == "positive":
                self.__save_info_with_image(info, image)

    def __save_info_with_image(self, info: ImageInfo, image: str):
        gallery = pbh_get_gallery_folder()

        prompt_gallery = gallery + "/prompts/"

        for prompt in info.prompt_builder.pbh_get_current_prompts():
            path = prompt_gallery + prompt
            if not os.path.isdir(path):
                os.makedirs(path)
            file = path + "/" + os.path.basename(image)
            if not os.path.isfile(file):
                os.link(image, path + "/" + os.path.basename(image))

        category_gallery = gallery + "/categories/"

        for category in info.prompt_builder.pbh_get_current_category_names():
            path = category_gallery + category
            if not os.path.isdir(path):
                os.makedirs(path)
            file = path + "/" + os.path.basename(image)
            if not os.path.isfile(file):
                os.link(image, path + "/" + os.path.basename(image))


instance = GallerySaver()


def pbh_get_gallery_saver() -> GallerySaver:
    return instance
