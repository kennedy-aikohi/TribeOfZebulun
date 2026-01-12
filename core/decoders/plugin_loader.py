import os
import importlib
import plugins


def load_plugins():
    instances = []
    base = os.path.dirname(plugins.__file__)

    for f in os.listdir(base):
        if f.endswith(".py") and f not in ("__init__.py", "base_plugin.py"):
            mod = importlib.import_module(f"plugins.{f[:-3]}")
            for obj in mod.__dict__.values():
                if hasattr(obj, "detect"):
                    instances.append(obj())
    return instances
