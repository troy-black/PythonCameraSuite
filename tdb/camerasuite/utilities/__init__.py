import importlib
import pkgutil
from pathlib import Path


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
    except (ImportError, OSError):
        return None


def verify_folder(path: str):
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def verify_file_exists(path: str, filename: str):
    try:
        return Path(f'{path}/{filename}').exists()
    except Exception:
        return False
