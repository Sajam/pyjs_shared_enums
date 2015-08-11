from enum import Enum

# Test comment

var_test = 0


def test_func():
    return 'foo'


class NumbersEnum(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4


class TestClass(object):
    foo = 'bar'

    class FoosEnum(Enum):
        FOO = 'foo'
        BAR = 'bar'
        BAZ = 'baz'

    def baz(self):
        return self.foo


if __name__ == '__main__':
    for i in xrange(1, 5, 1):
        print '{} iteration!'.format(i)
