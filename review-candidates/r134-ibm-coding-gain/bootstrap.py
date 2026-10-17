#!/usr/bin/env python3
"""Optional independently seeded multinomial bootstrap, conditioned on each circuit.

This is not an independently verified hardware time-series uncertainty model.
Correlated twirling or chronological drift can widen uncertainty. For those
questions, time-ordered records would be necessary.
"""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import numpy as np
from verify_counts import score, validate
ROOT=Path(__file__).parent


def bootstrap(rec,B=2000,seed=2061016):
    validate(rec)
    rng=np.random.default_rng(seed)
    ct=rec['counts']
    keys={nm:sorted(v) for nm,v in ct.items()}
    Ns={nm:sum(v.values()) for nm,v in ct.items()}
    multin={nm:np.array([ct[nm][k] for k in keys[nm]],dtype=float)/Ns[nm] for nm in keys}
    out=np.empty(B)
    for b in range(B):
        counts={nm:dict(zip(keys[nm],map(int,rng.multinomial(Ns[nm],multin[nm])))) for nm in ct}
        tmp=dict(rec,counts=counts)
        out[b]=score(tmp,validated=False)['gain']
    result={'B':B,'seed':seed,'mean':float(out.mean()),'sd':float(out.std(ddof=1)),
            'percentiles_95':list(map(float,np.quantile(out,[.025,.975])))}
    return result

if __name__=='__main__':
    r=json.loads((ROOT/'raw_counts_and_decoder.json').read_text())
    print(json.dumps({'v2_independent_bootstrap':bootstrap(r)},indent=2))
