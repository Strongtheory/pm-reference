import importlib
import inspect
import pkgutil
import os

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


def get_modules(module):
    path_list = []
    spec_list = []
    for importer, modname, ispkg in pkgutil.walk_packages(module.__path__):
        import_path = f"{module.__name__}.{modname}"
        if ispkg:
            spec = pkgutil._get_spec(importer, modname)
            importlib._bootstrap._load(spec)
            spec_list.append(spec)
        else:
            path_list.append(import_path)
    return path_list


def get_classes(module):
    class_list = []
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if not name.startswith("_"):
            class_list.append([name, obj])
    return class_list


def add_module_to_provider_list(providers, module):
    # eg diagrams.azure.database
    # add "database" to array linked to key "azure"
    (diagram, provider, pclass) = module.split(".")
    if provider not in providers:
        providers[provider] = [pclass]
    else:
        providers[provider].append(pclass)


def get_provider_list(providers):
    return providers.keys()


def get_provider_classes(providers, provider):
    return providers[provider]


def display_icons(class_list):
    if len(class_list) < 1:
        return
    if len(class_list) == 1:
        return class_list[0][1](class_list[0][0])
    length = len(class_list)
    return (
        display_icons(class_list[:-1])
        - Edge(penwidth="0", minlen="2")
        - class_list[length - 1][1](class_list[length - 1][0])
    )


def print_image(provider, pclassName):
    with fragile(
        Diagram(
            f"{provider}-{pclassName}",
            show=False,
            outformat="png",
            filename=f"{provider}/{pclassName}",
        )
    ):
        with Cluster(pclassName):
            classes = get_classes(
                importlib.import_module("diagrams." + provider + "." + pclassName)
            )
            display_icons(classes)

        raise fragile.Break


def check_local_directory(name):
    return os.path.isdir(name)


def create_dir(name):
    try:
        os.mkdir(name)
    except OSError as err:
        print(err)


def main():
    providers = dict()
    modules = get_modules(diagrams)

    for module in modules:
        if module not in ["diagrams.oci.database"]:
            add_module_to_provider_list(providers, module)

    for provider in get_provider_list(providers):
        print(provider)
        if not check_local_directory(provider):
            create_dir(provider)

        for pclassName in get_provider_classes(providers, provider):
            print(pclassName)
            print_image(provider, pclassName)

        print("\n")


if __name__ == "__main__":
    main()
