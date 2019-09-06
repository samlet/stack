from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import importlib
import inspect
import logging
import pkgutil
import warnings

import six
from sagas.util.reflect_util import all_subclasses

logger = logging.getLogger(__name__)

class ClassFinder(object):
    def __init__(self, base_cls):
        self.actions = {}
        self.base_cls=base_cls

    def _import_submodules(self, package, recursive=True):
        """ Import all submodules of a module, recursively, including
        subpackages

        :param package: package (name or actual module)
        :type package: str | module
        :rtype: dict[str, types.ModuleType]
        """
        if isinstance(package, six.string_types):
            package = importlib.import_module(package)
        if not getattr(package, "__path__", None):
            return

        results = {}
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + "." + name
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                self._import_submodules(full_name)

    def register_package(self, package):
        try:
            self._import_submodules(package)
        except ImportError:
            logger.exception("Failed to register package '{}'.".format(package))

        actions = all_subclasses(self.base_cls)
        return actions


if __name__ == '__main__':
    from sagas.nlu.ruleset import RuleSets
    executor = ClassFinder(RuleSets)
    actions=executor.register_package("sagas.aifuncs")
    for action in actions:
        print(action)

