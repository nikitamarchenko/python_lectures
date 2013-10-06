__author__ = 'tpuctah'


def bind(func, *arg_original, **kwargs_original):
    def wrapper(*args, **kwargs):
        return func(*(arg_original + args), **(dict(kwargs.items() + kwargs_original.items())))
    return wrapper

import unittest


class _test(unittest.TestCase):
    def test(self):

        def func(x, y, z, t):
            return x, y, z, t
        f1 = bind(func, 1, 2, t=13)
        self.assertEqual(f1([4]), (1, 2, [4], 13))

