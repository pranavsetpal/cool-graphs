

# This file was *autogenerated* from the file main.sage
from sage.all_cmdline import *   # import sage library

_sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_4 = Integer(4); _sage_const_3 = Integer(3)
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
    if b == _sage_const_0 :
        return a
    return g_gcd(b, g_mod(a, b))

def g_factorization(N):
    primes = list(factor(N))

    R_primes = [(_sage_const_1 , _sage_const_0 )]
    C_primes = []
    for prime, index in primes:
        if prime == _sage_const_2 :
            C_primes.append( (_sage_const_1  + I, index) )

        elif prime % _sage_const_4  == _sage_const_3 :
            R_primes.append( (prime, index) )

        elif prime % _sage_const_4  == _sage_const_1 :
            k = _sage_const_0 
            for i in range(prime):
                if (i**_sage_const_2  % prime) == (-_sage_const_1  % prime):
                    k = i
                    break

            gcd = g_gcd(prime, k + I)
            g_p = gcd if g_mod(N, gcd) == _sage_const_0  else conjugate(gcd)
            C_primes.append( (g_p, index) )

    return R_primes, C_primes


def gen_factor_combs(p, i):
    combs = combinations_with_replacement([ p, conjugate(p) ], i)
    combs = list(combs)[:(i // _sage_const_2 ) + _sage_const_1 ]
    combs = [ prod(comb) for comb in combs ]

    return combs


def findIntegralPoints(r):
    if r == _sage_const_0 :
        return []

    R_primes, C_primes = g_factorization(r)
    coeff = _sage_const_1 
    for p, i in R_primes:
        if i % _sage_const_2  != _sage_const_0 :
            return []
        coeff *= p**(i/_sage_const_2 )

    combs = []
    for p, i in C_primes:
        combs.append( gen_factor_combs(p, i) )

    products = product(*combs)
    products = [ coeff * prod(product) for product in products ]


    points = []
    for p in products:
        points.extend([
            p * _sage_const_1 , conjugate(p) * _sage_const_1 ,
            p *-_sage_const_1 , conjugate(p) *-_sage_const_1 ,
            p * I, conjugate(p) * I,
            p *-I, conjugate(p) *-I,
        ])
    points = tuple(set(points))

    return points


def main():
    r = int(input("Enter radius of circle: "))
    points = findIntegralPoints(r**_sage_const_2 )

    G = Graphics()
    G += circle((_sage_const_0 , _sage_const_0 ), r)
    for p in points:
        p = p.real(), p.imag()
        G += point(p)
        G += text(f'({p[_sage_const_0 ]}, {p[_sage_const_1 ]})', p, color="red")

    G.save('plot.png')

main()

