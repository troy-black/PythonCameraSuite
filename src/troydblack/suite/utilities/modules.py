import importlib
import pkgutil


def import_submodules(package: str, recursive=True) -> dict:
    module = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(module.__path__):
        full_name = module.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results
