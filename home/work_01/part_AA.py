__author__ = 'nmarchenko'

import unittest


# def map_rq(function, iterator):
#     result = []
#     i = iter(iterator)
#     try:
#         def rq(arg):
#             result.append(function(arg))
#             rq(next(i))
#
#         rq(next(i))
#     except StopIteration:
#         pass
#
#     return result

def map_rq(function, iter):
    result = []
    def rq(current_list):
        if current_list:
            result.append(function(current_list[0]))
            rq(current_list[1:])
    rq(list(iter))
    return result


class test_map_rq(unittest.TestCase):
    def test(self):
        import operator
        import functools

        r = range(0, 11)

        expect = map(functools.partial(operator.pow, 2), r)

        self.assertEqual(r, range(0, 11))

        result = map_rq(functools.partial(operator.pow, 2), r)

        self.assertEqual(r, range(0, 11))

        self.assertEqual(expect, result)

        result = map_rq(functools.partial(operator.pow, 2), xrange(0, 11))

        self.assertEqual(expect, result)


def map_yield(function, iterator):
    for i in iterator:
        yield function(i)


class test_map_yield(unittest.TestCase):
    def test(self):
        import operator
        import functools

        r = range(0, 11)

        expect = map(functools.partial(operator.pow, 2), r)

        self.assertEqual(r, range(0, 11))

        result = map_yield(functools.partial(operator.pow, 2), r)

        self.assertEqual(r, range(0, 11))

        self.assertEqual(expect, list(result))

        result = map_yield(functools.partial(operator.pow, 2), xrange(0, 11))

        self.assertEqual(expect, list(result))