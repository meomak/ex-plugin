from _typeshed import Incomplete
from androidx.core.content import ContextCompat as ContextCompat
from base_plugin import BasePlugin
from com.chaquo.python import PyException as PyException
from com.exteragram.messenger.plugins.hooks import PluginsHooks as PluginsHooks
from com.exteragram.messenger.plugins.models import CustomSetting as CustomSetting, DividerSetting as DividerSetting, EditTextSetting as EditTextSetting, HeaderSetting as HeaderSetting, InputSetting as InputSetting, SelectorSetting as SelectorSetting, SwitchSetting as SwitchSetting, TextSetting as TextSetting
from com.exteragram.messenger.plugins.pip import PipController as PipController
from com.exteragram.messenger.plugins.ui import PluginSettingsActivity as PluginSettingsActivity, PluginsActivity as PluginsActivity
from com.exteragram.messenger.plugins.ui.components import InstallPluginBottomSheet as InstallPluginBottomSheet, PluginCellDelegate as PluginCellDelegate, PluginRequirementsView as PluginRequirementsView
from dataclasses import dataclass, field
from de.robv.android.xposed import XposedBridge as XposedBridge
from elyxcore.assets import Assets as Assets, load_data_file as load_data_file
from elyxcore.localization import Strings as Strings
from elyxcore.settings import SettingsController as SettingsController
from elyxcore.utils import gen as gen
from java import dynamic_proxy as dynamic_proxy, jarray as jarray, jbyte as jbyte, jclass as jclass, jfloat as jfloat, jint as jint, jlong as jlong
from org.mvel2 import MVEL as MVEL
from org.telegram.messenger import R as R
from pathlib import Path
from typing import Any
from zipfile import ZipFile, ZipInfo

ELYX_ID: str

def dlog(msg: str) -> None: ...

OnClickListener: Incomplete
Runnable: Incomplete
Callback: Incomplete
Callback2: Incomplete
Callback3: Incomplete
CallbackReturn: Incomplete
ALLOWED_METAINFO: Incomplete
BASE_METAINFO: Incomplete
ENGINE_ID: str

class ArchiveEncryptionError(Exception): ...
class SecurityError(Exception): ...
class ValidationError(Exception): ...

class InvalidPluginError(Exception):
    @classmethod
    def plugin_class_not_found(cls, main_file_path): ...

class RequiredPlugin(Exception):
    plugin_id: Incomplete
    required_version: Incomplete
    link_to_download: Incomplete
    current_version: Incomplete
    def __init__(self, plugin_id, required_version: str | None = None, link_to_download: str | None = None, current_version=None) -> None: ...

class ElyxPlugin:
    instances: dict[str, 'ElyxPlugin']
    instances_by_id: dict[str, 'ElyxPlugin']
    def __new__(cls, dir_path: str | None = None, plzip: ZipFile | None = None, pwd: str | None = None, raise_errors: bool = True): ...
    @classmethod
    def from_archive(cls, plzip: ZipFile): ...
    instance: BasePlugin | None
    plugin_class: type[BasePlugin] | None
    errors: list[tuple[BaseException, str]]
    raise_errors: Incomplete
    dir_path: Incomplete
    plzip: Incomplete
    is_archive: Incomplete
    id: Incomplete
    def __init__(self, dir_path: str | None = None, plzip: ZipFile | None = None, pwd: str | None = None, raise_errors: bool = True) -> None: ...
    @dataclass
    class Structure:
        refmap: dict[str, dict[str, str]] = field(default_factory=dict)
        metainfo: dict[str, Any] = field(default_factory=dict)
        assets: str = ...
        strings: dict[str, dict[str, Any]] = field(default_factory=dict)
        main_file_path: str = ...
        wheels_path: str = ...
        validation_result: Any = ...
    @property
    def validation_result(self): ...
    @property
    def structure(self) -> Structure: ...
    def init(self) -> None: ...
    def get_environment_vars(self) -> dict[str, Any]: ...
    def get_strings(self, files=None): ...
    def load_structure(self): ...
    def validate(self, files: dict[str, ZipInfo | Path]): ...
    def get_file_content(self, f: ZipInfo | Path | None = None, path: str | None = None) -> str: ...
    def get_refmap(self, files: dict[str, ZipInfo | Path]) -> dict[str, dict[str, str]]: ...
    def get_metainfo(self, files: dict[str, ZipInfo | Path] | None = None) -> dict[str, Any]: ...
    def get_validation_result(self): ...
    def is_custom_icon(self): ...
    def get_icon_path(self): ...
