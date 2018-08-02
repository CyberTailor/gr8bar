#!/usr/bin/env python3

import os
import sys
import threading
import time
import types

from PyQt5 import QtCore, QtWidgets

try:
    from modules import sound, network, linux, gallium_os
    import ui
    import tools
except ModuleNotFoundError:
    from gr8bar.modules import sound, network, linux, gallium_os
    from gr8bar import ui
    from gr8bar import tools


sys.path.append(os.path.dirname(sys.argv[1]))
cfg = __import__(os.path.basename(sys.argv[1].replace('.py', '')))

app = QtWidgets.QApplication([])

window = QtWidgets.QWidget()
window.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint |
                      QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool |
                      QtCore.Qt.X11BypassWindowManagerHint)

bounds = cfg.bounds()
window.move(bounds['x'], bounds['y'])
window.setFixedSize(bounds['w'] if 'w' in bounds else bounds['width'],
                    bounds['h'] if 'h' in bounds else bounds['height'])

window_layout = ui.hbox_layout(window)

properties = {}

modules = types.SimpleNamespace(sound=sound, network=network, linux=linux,
                                gallium_os=gallium_os)

data = types.SimpleNamespace(app=app, panel=window, layout=window_layout,
                             ui=ui, os=os, tools=tools, props=properties,
                             modules=modules)


def render():
    '''
    Renders the bar from the given configuration file
    '''
    ui.clear_layout(window_layout)
    cfg.config(data)

    window.ensurePolished()

    bg = window.palette().color(window.backgroundRole())
    if bg == QtCore.Qt.transparent:
        window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        window.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)


def run_updater(updater, tools, modules, properties):
    '''
    Runs an updater with the fed tools and properties
    :param updater: The updater to run
    :param tools: The tools api wrapper
    :param properties: The properties that the updater maintains
    '''
    while True:
        updater[0](tools, modules, properties)
        time.sleep(updater[1])


def main():
    updaters = cfg.init_prop_updaters()
    for updater in updaters:
        threading.Thread(target=run_updater,
                         args=(updater, tools, modules, properties,)).start()
    timer = QtCore.QTimer()
    timer.timeout.connect(render)
    timer.start(cfg.render_loop_delay())
    render()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
