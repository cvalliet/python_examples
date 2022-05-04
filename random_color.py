#!/usr/bin/env python3

import numpy as np

def random_color():
    return list(np.random.choice(range(256), size=3))


if __name__ == '__main__':
    r, g, b = random_color()
    print('#%02x%02x%02x' % (r, g, b))

