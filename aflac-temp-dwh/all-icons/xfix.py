import importlib
import pkgutil
import inspect

import diagrams
from diagrams import Cluster, Diagram, Edge


class fragile(object):
    class Break(Exception):
        """Break out of the with statement"""

    def __init__(self, value):
        self.value = value

    def __enter__(self):
        return self.value.__enter__()

    def __exit__(self, etype, value, traceback):
        error = self.value.__exit__(etype, value, traceback)
        if etype == self.Break:
            return True
        return error


def get_modules(mod) -> list:
    path_list = []
    spec_list = []

    for importer, mod_name, is_package in pkgutil.walk_packages(mod.__path__):
        import_path = f"{mod.__name__}.{mod_name}"

        if is_package:
            spec = pkgutil._get_spec(importer, mod_name)

            importlib._bootstrap._load(spec)
            spec_list.append(spec)
        else:
            path_list.append(import_path)

        # if not is_package:
        #     path_list.append(import_path)

    return path_list


def get_classes(mod):
    class_list = []

    for (
        name,
        obj,
    ) in inspect.getmembers(mod.inspect.isclass):
        if not name.startswith("_"):
            class_list.append([name, obj])

    return class_list


def add_module_to_providers_list(providers, mod):
    (diagram, provider, pclass) = mod.split(".")

    if provider not in providers:
        providers[provider] = [pclass]
    else:
        providers[provider].append(pclass)


def get_providers_list(providers):
    return providers.keys()


def get_providers_classes(providers, provider):
    return providers[provider]


def display_icons(class_list):
    _length = len(class_list)

    if _length < 1:
        return

    if _length == 1:
        return class_list[0][1](class_list[0][0])

    return display_icons(class_list[:-1]) - class_list[_length - 1][1](
        class_list[_length - 1][0]
    )


def print_image(providers, provider):
    with fragile(Diagram(provider, show=False, outformat="png")):
        for pclassname in get_providers_classes(providers, provider):
            with Cluster(pclassname):
                classes = get_classes(
                    importlib.import_module("diagrams." + provider + "." + pclassname)
                )
                display_icons(classes)

        raise fragile.Break


def main():
    providers = dict()
    modules = get_modules(diagrams)

    for module in modules:
        if module not in ["diagrams.oci.database"]:
            add_module_to_providers_list(providers, module)

    for provider in get_providers_list(providers):
        print_image(providers, provider)


if "__main__" == __name__:
    main()
