from _typeshed import Incomplete
from androidx.core.content import ContextCompat as ContextCompat
from com.chaquo.python import PyException as PyException
from com.exteragram.messenger.plugins import Plugin as Plugin, PluginsController as PluginsController
from com.exteragram.messenger.plugins.hooks import PluginsHooks as PluginsHooks
from com.exteragram.messenger.plugins.models import CustomSetting as CustomSetting, DividerSetting as DividerSetting, EditTextSetting as EditTextSetting, HeaderSetting as HeaderSetting, InputSetting as InputSetting, SelectorSetting as SelectorSetting, SwitchSetting as SwitchSetting, TextSetting as TextSetting
from com.exteragram.messenger.plugins.pip import PipController as PipController
from com.exteragram.messenger.plugins.ui import PluginSettingsActivity as PluginSettingsActivity, PluginsActivity as PluginsActivity
from com.exteragram.messenger.plugins.ui.components import InstallPluginBottomSheet as InstallPluginBottomSheet, PluginCellDelegate as PluginCellDelegate, PluginRequirementsView as PluginRequirementsView
from de.robv.android.xposed import XposedBridge as XposedBridge
from elyxcore.utils import LazyDict as LazyDict, gen as gen
from java import dynamic_proxy as dynamic_proxy, jarray as jarray, jbyte as jbyte, jclass as jclass, jfloat as jfloat, jint as jint, jlong as jlong
from org.mvel2 import MVEL as MVEL
from org.telegram.messenger import R as R
from typing import Any, overload

ELYX_ID: str

def dlog(msg: str) -> None: ...

OnClickListener: Incomplete
Runnable: Incomplete
Callback: Incomplete
Callback2: Incomplete
Callback3: Incomplete
CallbackReturn: Incomplete

class Strings(LazyDict):
    all_strings: Incomplete
    def __init__(self, all_strings: dict[str, dict]) -> None: ...
    @staticmethod
    def get_current_language(): ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, value) -> None: ...
    @overload
    def get(self, key: str) -> Any: ...
    @overload
    def get(self, key: str, default) -> Any: ...
    def get_with_locale(self, key: str, default=None, locale: str = None) -> Any: ...
    def __call__(self, key: str, *args, default: str | None = None, locale: str = None, **kwargs): ...
    @staticmethod
    def pluralization_string(number: int, words: list[str]) -> str: ...
    def pluralize(self, number: int, key: str) -> str: ...

strings: Incomplete
