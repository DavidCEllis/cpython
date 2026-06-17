from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import types
import unittest

from dataclasses import (
    _METHODS,
    _AutoMethod,
    _init_source_maker,

    dataclass,
)


class TestLaziness(unittest.TestCase):
    def test_lazy_methods_in_dict(self):
        # Test that the lazy methods have not been generated
        # eagerly on creation of the dataclass
        @dataclass(frozen=True, order=True)
        class AllMethods:
            a: int

        methods = AllMethods.__dict__[_METHODS]

        for name, method in methods.items():
            self.assertEqual(AllMethods.__dict__[name], method)

    def test_lazy_methods_replaced_in_dict(self):
        # Test that lazy methods are replaced in the class dict
        # by functions after being accessed directly.
        @dataclass(frozen=True, order=True)
        class AllMethods:
            a: int

        methods = AllMethods.__dict__[_METHODS]

        for name, method in methods.items():
            self.assertNotEqual(getattr(AllMethods, name), method)
            self.assertIsInstance(getattr(AllMethods, name), types.FunctionType)


class TestThreading(unittest.TestCase):
    @staticmethod
    def get_slow_init_class():
        def slow_init_maker(name, cls):
            # We need to make __init__ generation slower to guarantee
            # that multiple threads will be trying to call the descriptor
            # __get__ method at the same time.
            time.sleep(0.01)
            return _init_source_maker(name, cls)

        @dataclass(init=False, repr=False, eq=False)
        class SlowInit:
            a: int

        auto_slow_init = _AutoMethod("__init__", slow_init_maker, SlowInit)
        setattr(SlowInit, "__init__", auto_slow_init)

        return SlowInit

    def test_multiple_calls(self):
        # Test retrieving `__init__` from multiple threads simultaneously
        # to trigger the `__get__` call multiple times.
        cls = self.get_slow_init_class()
        get_init = lambda: cls.__init__

        with ThreadPoolExecutor() as pool:
            futures = [pool.submit(get_init) for _ in range(50)]
            results = set()
            for future in as_completed(futures):
                results.add(future.result())

        self.assertEqual(len(results), 1)
