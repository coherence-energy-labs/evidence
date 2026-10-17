#!/usr/bin/env python3
"""Independent, stdlib-only verification of the explicit 2-use flagged-channel code.

This checks the exact 2-use fidelity, threshold and finite-dimensional parameter
bounds.  It DOES NOT verify the unpublished PPT-channel-to-flagged-channel
reduction; that is a separate theorem obligation. A proof of that reduction is
needed before claiming the full PPT x erasure result.
"""
from __future__ import annotations
from fractions import Fraction as Q
from math import isqrt


def sqrt_bounds(d: int, places: int = 48) -> tuple[Q, Q]:
    if type(d) is not int or d < 2 or type(places) is not int or places < 5:
        raise ValueError('invalid parameter')
    scale = 10 ** places
    lo_num = isqrt(d * scale * scale)
    lower = Q(lo_num, scale)
    upper = Q(lo_num + (0 if lo_num * lo_num == d * scale * scale else 1), scale)
    assert lower * lower <= d <= upper * upper
    return lower, upper


def p_bounds(d: int) -> tuple[Q,Q]:
    a,b=sqrt_bounds(d)
    return 1/(1+b), 1/(1+a)


def two_use_branch_fidelities(p: Q) -> dict[str,Q]:
    """Constructive decoding of |++>,|--> for two flagged uses.

    Flag 00: inverse isometry, ideal F=1.
    Flag 01/10: Z readout parity induces a correctable logical phase;
    Bernoulli bit-flip p makes it fail with probability p.
    Flag 11: both Z readouts form a binary X-basis measurement of the
    logical qubit with parity-flip rate 2p(1-p).  Measure-and-prepare,
    with the full discarded reference retained in the fidelity definition.
    """
    if p < 0 or p > 1:
        raise ValueError('p must be in [0,1]')
    return {'00': Q(1), '01': 1-p, '10': 1-p,
            '11': Q(1,2)-p*(1-p)}


def fidelity(p: Q) -> Q:
    branches=two_use_branch_fidelities(p)
    return sum(branches.values(),Q(0))/4


def fidelity_poly(p: Q) -> Q:
    return (7-6*p+2*p*p)/8


def bound_for_d(d: int) -> tuple[Q,Q]:
    p_lo,p_hi=p_bounds(d)
    # d >= 2 gives p < 1/2 and F'(p)= (4p-6)/8 < 0
    return fidelity(p_hi), fidelity(p_lo)


def test():
    from itertools import product
    for numerator,denominator in product(range(0,11),[10,20]):
        p=Q(numerator,denominator)
        assert fidelity(p) == fidelity_poly(p)
    for d in range(2,125):
        lo,hi=bound_for_d(d)
        assert lo<=hi and hi-lo<Q(1,10**40)
        assert (lo>Q(3,4)) == (d>=22)
        if d>=23:
            previous=bound_for_d(d-1)[1]
            assert lo>previous
    assert fidelity(Q(1,7))==Q(303,392)   # d=36
    assert fidelity(Q(1,9))==Q(515,648)   # d=64
    for d in [19,20,21,22,32,36,64,256,1024]:
        lo,hi=bound_for_d(d)
        print(f'd={d:<4} exact-rational F bounds: '
              f'[{float(lo):.15f},{float(hi):.15f}], '
              f'margin >= {float(lo-Q(3,4)):+.15f}')
    print('PASS: exact-rational closed-form construction, threshold and controls')

if __name__=='__main__':
    test()
