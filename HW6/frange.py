class Frange:
    def __init__(self, *args, start=0, stop=0, step=1):
        self.start = start
        self.stop = stop
        self.step = step
        if len(args) > 3:
            raise TypeError('The number of arguments cannot exceed 3')
        if len(args) == 3:
            self.start, self.stop, self.step = args
        if len(args) == 2:
            self.start, self.stop = args
        if len(args) == 1:
            self.stop = args[0]

    def __iter__(self):
        return self

    def __next__(self):
        if self.step > 0:
            value = self.start
            self.start += self.step
            if value >= self.stop:
                raise StopIteration
        else:
            value = self.start
            self.start += self.step
            if value <= self.stop:
                raise StopIteration
        return value

assert(list(Frange(5)) == [0, 1, 2, 3, 4])
assert(list(Frange(2, 5)) == [2, 3, 4])
assert(list(Frange(2, 10, 2)) == [2, 4, 6, 8])
assert(list(Frange(10, 2, -2)) == [10, 8, 6, 4])
assert(list(Frange(2, 5.5, 1.5)) == [2, 3.5, 5])
assert(list(Frange(1, 5)) == [1, 2, 3, 4])
assert(list(Frange(0, 5)) == [0, 1, 2, 3, 4])
assert(list(Frange(0, 0)) == [])
assert(list(Frange(100, 0)) == [])

print('SUCCESS!')