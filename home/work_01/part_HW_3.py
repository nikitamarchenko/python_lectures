__author__ = 'tpuctah'


def check_me(function):

    if not len(function.__doc__):
        raise TypeError("Function doc string is missing")

    import inspect

    argspec = inspect.getargspec(function)

    if argspec.varargs:
        raise TypeError('Forbidden type {}'.format(argspec.varargs))

    if argspec.keywords:
        raise TypeError('Forbidden type {}'.format(argspec.keywords))

    arg = [x.strip()[7:].split(': ') for x in function.__doc__.split('\n') if x.strip().startswith('@param ')]

    if len(arg) != len(argspec.args):
        msg = \
            'Invalid function params count. Function {} get {} argumets but in docstring {}'\
                .format(function.__name__, len(argspec.args), len(arg))
        raise TypeError(msg)

    for i, a in enumerate(zip(arg, argspec.args)):
        if a[0][0] != a[1]:
            raise TypeError("Invalid argument name {} in {} position".format(a[0], i))

    def wrapper(*args):
        for a in zip(arg, args):
            if type(a[1]).__name__ != a[0][1]:
                raise TypeError('Argument type error: "{}" must be {}'.format(*a[0]))
        return function(*args)
    return wrapper

import unittest


class _test(unittest.TestCase):
    def test_varargs(self):
        def func():
            @check_me
            def my_func(*args):
                """
            @param x: int
            @param y: str
            """
                pass

        self.assertRaises(TypeError, func)

    def test_keywords(self):
        def func():
            @check_me
            def my_func(**kwargs):
                """
            @param x: int
            @param y: str
            """
                pass

        self.assertRaises(TypeError, func)

    def test_arg_position(self):
        def func():
            @check_me
            def my_func(y, x):
                """
            @param x: int
            @param y: str
            """
                pass

        self.assertRaises(TypeError, func)

    def test_01(self):

        @check_me
        def my_func(x, y):
            """
            @param x: int
            @param y: str
            """
            return str(x) + y

        self.assertRaises(TypeError, my_func, 1, 2)
        self.assertEqual(my_func(2, "3"), "23")
