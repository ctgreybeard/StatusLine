# coding=utf-8
from __future__ import absolute_import

import flask

import octoprint.plugin

class StatusLinePlugin(octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.SimpleApiPlugin,
                       octoprint.plugin.OctoPrintPlugin
                       ):

    def __init__(self):
        self.fan = "--"
        self.lcd = ""

    # OctoPrintPlugin hook

    def hook_m117(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        if gcode:
            should_send = False
            if gcode == "M117":
                self._logger.debug("Sent M117 command: {0}".format(cmd))
                self.lcd = cmd[5:]
                should_send = True
            elif gcode == "M107":
                self.fan = "00"
                should_send = True
            elif gcode == "M106":
                cmda = cmd.split()
                for a in cmda:
                    if a[0] == 'S':
                        self.fan = a[1:]
                        should_send = True
            if should_send:
                self._plugin_manager.send_plugin_message(self._identifier, dict(status_lcd=self.lcd, status_fan=self.fan))

    # AssetPlugin

    def get_assets(self):
        return {
            "js": ["js/status_line.js"]
        }

    # TemplatePlugin

    def get_template_configs(self):
        return [
            dict(type="sidebar", name="Status line", icon="print")
        ]

    # SimpleApiPlugin

    def on_api_get(self, request):
        return flask.jsonify(dict(
            status_lcd=self.lcd,
            status_fan=self.fan,
        ))

__plugin_name__ = "Status Line"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = StatusLinePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.protocol.gcode.sent": __plugin_implementation__.hook_m117
    }

