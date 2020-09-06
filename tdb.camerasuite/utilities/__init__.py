import importlib
import pkgutil


def import_submodules(package: str, recursive=True) -> dict:
    module = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(module.__path__):
        fullname = module.__name__ + '.' + name
        results[fullname] = import_module(fullname)
        if recursive and is_pkg:
            results.update(import_submodules(fullname))
    return results


def import_module(fullname: str):
    try:
        return importlib.import_module(fullname)
    except ImportError:
        return None
