#!/usr/bin/env python3
"""Independent finite-matrix checks of a proposed PPT channel family.

The construction is restated from its mathematical definition, not from the
private ONE_Q implementation. Finite numerical tests are evidence against
indexing mistakes, not a proof for all shield dimensions.
"""
from __future__ import annotations
import numpy as np
import math


def fourier(d: int):
    a=np.arange(d)
    return np.exp(2j*np.pi*np.outer(a,a)/d)


def channel_choi(d: int, weight: float):
    h=fourier(d)
    dd=d*d
    sw=np.zeros((dd,dd),complex)
    for a in range(d):
        for b in range(d):
            sw[a*d+b,b*d+a]=1
    # twist of the maximally mixed shield, diagonal phases + SWAP
    phase=np.diag(h.reshape(-1))
    twist0=phase@sw
    # twist of the correlated shield, Fourier on span{|aa>}
    twist1=np.eye(dd,dtype=complex)
    positions=[a*d+a for a in range(d)]
    twist1[np.ix_(positions,positions)]=h/math.sqrt(d)
    eye=np.eye(dd,dtype=complex)
    sigma0=eye/dd
    sigma1=np.zeros((dd,dd),complex)
    sigma1[positions,positions]=1/d
    # order key_R,key_B,shield_R,shield_B => finally input_R,output_B
    out=np.zeros((4*dd,4*dd),complex)
    for sector,pr,shield,twist in [(0,1-weight,sigma0,twist0),
                                   (1,weight,sigma1,twist1)]:
        for a in range(2):
            for b in range(2):
                key=np.zeros((4,4),complex)
                left=2*a+(a^sector);right=2*b+(b^sector)
                key[left,right]=pr/2
                ua=eye if a==0 else twist
                ub=eye if b==0 else twist
                out+=np.kron(key, ua@shield@ub.conj().T)
    return out.reshape(2,2,d,d,2,2,d,d).transpose(0,2,1,3,4,6,5,7).reshape(4*dd,4*dd)


def diagnostics(d,weight):
    rho=channel_choi(d,weight)
    D=2*d
    tr_out=rho.reshape(D,D,D,D).trace(axis1=1,axis2=3)
    pt=rho.reshape(D,D,D,D).transpose(0,3,2,1).reshape(D*D,D*D)
    return {'choi_psd_min':float(np.linalg.eigvalsh(rho)[0]),
            'ppt_min':float(np.linalg.eigvalsh(pt)[0]),
            'tp_deviation':float(np.max(np.abs(tr_out-np.eye(D)/D))),
            'trace_deviation':float(abs(np.trace(rho)-1))}


def main():
    for d in (2,3,4,5):
        p=1/(1+math.sqrt(d));v=diagnostics(d,p);bad=diagnostics(d,.96*p)
        print('d=',d,'at PPT boundary',v,'off boundary',bad)
        assert v['choi_psd_min'] > -1e-12 and v['ppt_min'] > -1e-12
        assert v['tp_deviation'] < 2e-12 and v['trace_deviation']<2e-12
        assert bad['ppt_min'] < -1e-6
    print('PASS: finite matrices; NOT a general-dimension proof')

if __name__=='__main__':main()
