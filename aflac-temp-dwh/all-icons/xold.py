import importlib
import pkgutil
import sys, inspect

import diagrams
from diagrams import Cluster, Diagram, Edge


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
    # return display_icons(class_list[:-1]) - class_list[length - 1][1](
    #     class_list[length - 1][0]
    # )

    return display_icons(class_list[:-1])


if __name__ == "__main__":
    providers = {}
    modules = get_modules(diagrams)

    for module in modules:
        # Module exception
        # /usr/local/lib/python3.8/site-packages/diagrams/oci/database.py
        # NameError: name 'AutonomousDatabase' is not defined
        if module not in ["diagrams.oci.database"]:
            add_module_to_provider_list(providers, module)

    with Diagram("all_Icons", show="False", outformat="png"):
        for provider in get_provider_list(providers):
            with Cluster(provider):
                for pclassname in get_provider_classes(providers, provider):
                    with Cluster(pclassname):
                        classes = get_classes(
                            importlib.import_module(
                                "diagrams." + provider + "." + pclassname
                            )
                        )
                        display_icons(classes)
