import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from itertools import combinations_with_replacement, product
from math import prod


def g_round(z):
    return ( round(z.real()) + round(z.imag())*I )

def g_mod(a, b):
    q = g_round(a / b)
    remainder = a - b*q

    return remainder

def g_gcd(a, b):
    if b == 0:
        return a
    return g_gcd(b, g_mod(a, b))

def g_factorization(N):
    primes = list(factor(N))

    R_primes = [(1, 0)]
    C_primes = []
    for prime, index in primes:
        if prime == 2:
            C_primes.append( (1 + I, index) )

        elif prime % 4 == 3:
            R_primes.append( (prime, index) )

        elif prime % 4 == 1:
            k = 0
            for i in range(prime):
                if (i^2 % prime) == (-1 % prime):
                    k = i
                    break

            gcd = g_gcd(prime, k + I)
            g_p = gcd if g_mod(N, gcd) == 0 else conjugate(gcd)
            C_primes.append( (g_p, index) )

    return R_primes, C_primes


def gen_factor_combs(p, i):
    combs = combinations_with_replacement([ p, conjugate(p) ], i)
    combs = list(combs)[:(i // 2) + 1]
    combs = [ prod(comb) for comb in combs ]

    return combs


def findIntegralPoints(r):
    if r == 0:
        return []

    R_primes, C_primes = g_factorization(r)
    coeff = 1
    for p, i in R_primes:
        if i % 2 != 0:
            return []
        coeff *= p^(i/2)

    combs = []
    for p, i in C_primes:
        combs.append( gen_factor_combs(p, i) )

    products = product(*combs)
    products = [ coeff * prod(product) for product in products ]


    points = []
    for p in products:
        points.extend([
            p * 1, conjugate(p) * 1,
            p *-1, conjugate(p) *-1,
            p * I, conjugate(p) * I,
            p *-I, conjugate(p) *-I,
        ])
    points = tuple(set(points))

    return points


def main():
    r = int(input("Enter radius of circle: "))
    points = findIntegralPoints(r^2)

    G = Graphics()
    G += circle((0, 0), r)
    for p in points:
        p = p.real(), p.imag()
        G += point(p)
        G += text(f'({p[0]}, {p[1]})', p, color="red")

    G.save('plot.png')

main()
