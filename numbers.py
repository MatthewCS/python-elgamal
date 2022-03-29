import random


def prime_bitlen(bitlen, mr_trials=10):

    found = False
    n = -1

    while not found:

        # n = random prime candidate of bitlen bits
        n = random.randrange((2 ** (bitlen - 1)) + 1, (2 ** bitlen) - 1)

        # find valid d for miller-rabin test
        d = n - 1

        while d % 2 == 0:
            d //= 2

        # use miller rabin test using multi-threading

        found = True

        for _ in range(0, mr_trials):

            if not miller_rabin(n, d):

                found = False
                break

    return n


def miller_rabin(n, d):

    if n == 2:          return True
    if n < 3:           return False
    if n % 2 == 0:      return False

    # random number in [2 .. n - 2]
    rand = random.randrange(3, n - 2)

    x = pow(rand, d, n)

    if x in (1, n - 1):  return True

    # keep squaring x & doubling d until:
    # A. d doesn't reach n - 1
    # B. x^2 (mod n) is not 1 (composite) or n - 1 (prime)
    while(d != n - 1):

        x = pow(x, 2, n)
        d *= 2

        if x == 1:
            return False

        if x == n - 1:
            return True

    return False



def gcd(x, y):

    if x < y:

        return gcd(y, x)

    if x % y == 0:

        return y

    return gcd(y, x % y)
