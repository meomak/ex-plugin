from base_plugin import BasePlugin
from ui.settings import Header, Switch


__id__ = '$json.id'
__name__ = '$json.name'
__description__ = '$json.description'
__author__ = '$json.author'
__version__ = '$json.version'
__icon__ = '$json.icon'
__app_version__ = '$json.app_version'
__sdk_version__ = '$json.sdk_version'


class Plugin(BasePlugin):
    def create_settings(self):
        return [
            Header(text="Plugin"),
            Switch(
                key="enabled",
                text="Включить плагин",
                default=True,
            ),
        ]

    def on_plugin_load(self):
        self.log("Plugin loaded")