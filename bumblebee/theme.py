import os
import json

class Theme:
    _cycle_index = 0
    _cycle = None
    def __init__(self, name="default"):
        self._data = None
        path = os.path.dirname(os.path.realpath(__file__))
        with open("{}/themes/{}.json".format(path, name)) as f:
            self._data = json.load(f)
        self._defaults = self._data.get("defaults", {})
        self._cycle = self._defaults.get("cycle", [])

        self.reset()

    def _gettheme(self, obj, key):
        module = obj.__module__.split(".")[-1]
        module_theme = self._data.get(module, {})

        value = getattr(obj, key)() if hasattr(obj, key) else None
        value = self._defaults.get(key, value)
        if len(self._cycle) > 0:
            value = self._defaults["cycle"][self._cycle_index].get(key, value)
        value = module_theme.get(key, value)

        if hasattr(obj, "state"):
            state = getattr(obj, "state")()
            state_theme = module_theme.get("states", {}).get(state, {})

            value = state_theme.get(key, value)

        return value

    def reset(self):
        self._cycle_index = 0
        self._previous_background = None
        self._background = None

    def next(self):
        self._cycle_index += 1
        self._previous_background = self._background
        if self._cycle_index >= len(self._cycle):
            self._cycle_index = 0

    def color(self, obj):
        return self._gettheme(obj, "fg")

    def background(self, obj):
        self._background = self._gettheme(obj, "bg")
        return self._background

    def previous_background(self):
        return self._previous_background

    def separator(self, obj):
        return self._gettheme(obj, "separator")

    def default_separators(self, obj):
        return self._gettheme(obj, "default_separators")

    def prefix(self, obj):
        return self._gettheme(obj, "prefix")

    def suffix(self, obj):
        return self._gettheme(obj, "suffix")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4