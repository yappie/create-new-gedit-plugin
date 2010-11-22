from __future__ import with_statement
import os
import pipes

plugins_dir = os.path.expanduser("~/.gnome2/gedit/plugins/")

main_file = """
import gedit

class {ModuleName}WindowHelper:
    def __init__(self, plugin, window):
        print "Plugin created for", window
        self._window = window
        self._plugin = plugin

    def deactivate(self):
        print "Plugin stopped for", self._window
        self._window = None
        self._plugin = None

    def update_ui(self):
        # Called whenever the window has been updated (active tab
        # changed, etc.)
        print "Plugin update for", self._window

class {ModuleName}Plugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        self._instances[window] = {ModuleName}WindowHelper(self, window)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        self._instances[window].update_ui()
""".strip()

manifest_file = """
[Gedit Plugin]
Loader=python
Module={module_name_lowercase}
IAge=2
Name={module_name}
Description=A Python plugin example
Authors={author}
Copyright={author}
Website=http://www.gedit.org
""".strip()

module = raw_input('New Module Name [Ctrl+C to abort]:').strip()
author = raw_input('Author Name <and@your.email>:').strip()

module_name_lowercase = module.lower().replace(' ','_')

manifest_file = manifest_file \
    .replace('{author}', author) \
    .replace('{module_name}', module) \
    .replace('{module_name_lowercase}', module_name_lowercase) \

main_file = main_file \
    .replace('{ModuleName}', module.title().replace(' ',''))



plugin_dir = os.path.join(plugins_dir, module_name_lowercase)
if not os.path.exists(plugin_dir):
    os.mkdir(plugin_dir)

fn1 = os.path.join(plugin_dir, '%s.gedit-plugin' % module_name_lowercase)
assert not os.path.exists(fn1), \
            "File '%s' already exists, won't overwrite plugin" % fn1
with open(fn1, 'w') as f:
    f.write(manifest_file)

fn2 = os.path.join(plugin_dir, '%s.py' % module_name_lowercase)
assert not os.path.exists(fn2), \
            "File '%s' already exists, won't overwrite plugin" % fn2
with open(fn2, 'w') as f:
    f.write(main_file)

os.system('gedit %s %s &' % (pipes.quote(fn1), pipes.quote(fn2)))    

