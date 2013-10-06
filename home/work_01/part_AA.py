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


def map_rq_yield(function, iterator):
    def rq(current_list):
        if current_list:
            yield function(current_list[0])
            rq(current_list[1:])
    rq(list(iterator))


class test_map_rq_yield(unittest.TestCase):
    def test(self):
        import operator
        import functools

        r = range(0, 11)

        expect = map(functools.partial(operator.pow, 2), r)

        self.assertEqual(r, range(0, 11))

        result = map_rq_yield(functools.partial(operator.pow, 2), r)

        # for i in result:
        #     print i
        #
        # print list(result)

        # self.assertEqual(r, range(0, 11))
        #
        # self.assertEqual(expect, list(result))
        #
        # result = map_rq_yield(functools.partial(operator.pow, 2), xrange(0, 11))
        #
        # self.assertEqual(expect, list(result))


# class time_me():
#     def __init__(self, time_function, result):
#         print time_function, result
#
#     def __call__(self, *args, **kwargs):
#         print self, args, kwargs

def time_me(time_function, result):
    def wrapper(func):
        def wrapped_function(*args, **kwargs):
            result['num_calls'] = result.setdefault('num_calls', 0) + 1
            start = time_function()
            try:
                function_result = func(*args, **kwargs)
            finally:
                result['cum_time'] = result.setdefault('cum_time', 0) + max(time_function() - start, 0)
            return function_result
        return wrapped_function
    return wrapper


class time_me_test(unittest.TestCase):

    def test(self):

        import time
        statistic = {}

        @time_me(time.time, statistic)
        def som_func(x, y):
            time.sleep(1.1)

        som_func(1, 2)
        som_func(1, 2)

        self.assertEqual(statistic['num_calls'], 2)
        self.assertGreater(2.5, statistic['cum_time'])
        self.assertGreater(statistic['cum_time'], 2)


