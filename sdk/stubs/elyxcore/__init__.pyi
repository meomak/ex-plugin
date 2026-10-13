from _typeshed import Incomplete
from elyxcore.assets import Asset as Asset, AssetNotFoundException as AssetNotFoundException, Assets as Assets, AssetsDirNotFoundException as AssetsDirNotFoundException
from elyxcore.localization import Strings as Strings
from elyxcore.settings import SettingsController as SettingsController
from elyxcore.utils import LazyDict as LazyDict, gen as gen, gen2 as gen2, mvel_execute as mvel_execute
from typing import Any

__all__ = ['Asset', 'AssetNotFoundException', 'Assets', 'AssetsDirNotFoundException', 'Strings', 'SettingsController', 'LazyDict', 'gen', 'gen2', 'mvel_execute', 'OnClickListener', 'Runnable', 'Callback', 'Callback2', 'Callback3', 'CallbackReturn', 'get_environment', 'import_module']

OnClickListener: Incomplete
Runnable: Incomplete
Callback: Incomplete
Callback2: Incomplete
Callback3: Incomplete
CallbackReturn: Incomplete

def get_environment() -> dict[str, Any]: ...
def import_module(name: str, package: str | None = None): ...
