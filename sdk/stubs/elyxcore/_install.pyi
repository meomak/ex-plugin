from _typeshed import Incomplete
from elyxcore._plugin import ArchiveEncryptionError as ArchiveEncryptionError, ElyxPlugin as ElyxPlugin, RequiredPlugin as RequiredPlugin, ValidationError as ValidationError
from elyxcore.localization import strings as strings
from elyxcore.utils import gen as gen, gen2 as gen2, resize_image as resize_image

OnClickListener: Incomplete
Runnable: Incomplete
Callback: Incomplete

class InstallAlert:
    @classmethod
    def show_password_dialog(cls, lib, fragment, params): ...
    @classmethod
    def show(cls, lib, fragment, plugin: ElyxPlugin, params): ...
