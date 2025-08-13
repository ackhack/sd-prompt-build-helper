from modules.shared import opts
from .util import pbh_get_gallery_folder
import os

#adding our gallery folder to browser_folders to show the extension gallery in the gallery tab
folder = str(os.path.abspath(pbh_get_gallery_folder()))
if not folder in opts.browser_folders:
    opts.browser_folders += str(os.path.abspath(pbh_get_gallery_folder())) + ','
