import math
import random

import classical
from quantum import quantum

def shor(n):
    if classical.is_prime(n):
        raise Exception("{} must be a composite number".format(n))

    if classical.is_prime_power(n):
        raise Exception("{} cannot be a power of a prime".format(n))

    found = False
    while not found:
        x = random.randint(2, n-1)
        gcd = math.gcd(x, n)

        if gcd != 1:
            found = True
            print("Lucky find!!")
            return [gcd, n // gcd]

        r = get_order(x, n)

        if r % 2 == 0:
            y = classical.power_mod(x, r // 2, n)
            d1, d2 = math.gcd(y+1, n), math.gcd(y-1, n)

            if n % d1 == True:
                found = True
                return [d1, n // d1]

            if n % d2 == True:
                found = True
                return [d2, n // d2]

def get_order(x, n):
    t = math.floor(2 * math.log2(n)) + 1
    n_states = 2**t

    print("-------------------->\nget_order: x={}, n={}".format(x, n))

    r = 1
    while x != 1 and r < n:
        m = quantum(x, n, n_states)

        while m == 0:
            print("[F] : MEASURED : 0")
            m = quantum(x, n, n_states)

        print("[T] : MEASURED : {}".format(m))
        convergents = classical.get_convergents(m, n_states)

        d = 1
        for c in convergents:
            if c.denominator < n:
                d = c.denominator

        x = classical.power_mod(x, d, n)
        r *= d

    print("Estimated r: {}".format(r))
    return r
