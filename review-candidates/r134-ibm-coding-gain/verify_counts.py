#!/usr/bin/env python3
"""Independent STD-LIB ONLY re-scorer of a historical IBM Kingston n=1/n=2 experiment.

Inputs: unpostselected 22 circuit count dictionaries and frozen decoder-effect
matrices. This rederives every branch from raw counts rather than trusting the
producer's persisted analysis. It does not authenticate IBM's external job API,
compiled machine instructions, or the original preregistration timestamp.
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
P=math.sqrt(2.0)-1.0
JOBS={'db6pvrkvf2bc73d1k8ug': ([149,148,147], '51558904c64cde18547619069635d5b93758b829'),
      'db6q46cvf2bc73d1kek0': ([148,149,150], '80a68eed646d99cc476d270298d0a43527a0d0ca')}
REQUIRED=(['n1_f0_'+x for x in ('XX','YY','ZZ')] + ['n1_f1_ZZ'] +
          ['n2_f00_'+x for x in ('XX','YY','ZZ')] +
          ['n2_'+arm+'_x'+str(flip)+'_'+b for arm in ('f10','f01') for flip in (0,1) for b in ('XX','YY','ZZ')] +
          ['n2_f11_'+b for b in 'XYZ'])


def validate(rec):
    if rec.get('schema')!='oneq-public-hw-gain/1' or rec.get('backend')!='ibm_kingston':
        raise ValueError('incorrect raw record schema or backend')
    data=rec.get('counts',{})
    if set(data)!=set(REQUIRED) or rec.get('shots') !=4000:
        raise ValueError('missing, extra, or mismatched circuit/shot plan')
    job=rec.get('job')
    if job not in JOBS:
        raise ValueError('unexpected immutable source job')
    layout,blob=JOBS[job]
    if rec.get('layout')!=layout or rec.get('raw_results_sha_git_blob')!=blob:
        raise ValueError('unexpected layout or provenance blob reference')
    for name,row in data.items():
        bits=3 if name.startswith('n2_f11_') else 2
        allowed={format(i,f'0{bits}b') for i in range(2**bits)}
        if set(row)!=allowed or any(type(v) is not int or v<0 for v in row.values()):
            raise ValueError(f'noncanonical counts for {name}')
        if sum(row.values())!=4000:
            raise ValueError('removed or duplicated shots in '+name)
    g=rec['decoder']['G']
    if set(g)!={'0','1','2'}:
        raise ValueError('decoder effects missing')
    for entry in g.values():
        for k in ('re','im'):
            if len(entry[k])!=2 or any(len(row)!=2 for row in entry[k]):
                raise ValueError('malformed decoder')
        gr,gi=entry['re'],entry['im']
        if abs(gr[0][1]-gr[1][0])>1e-10 or abs(gi[0][1]+gi[1][0])>1e-10:
            raise ValueError('not Hermitian decoder effect')
    return True


def correlation(row):
    count=sum(row.values());return sum(n*(1 if bits[-1]==bits[-2] else -1)
                                        for bits,n in row.items())/count


def bell(counts, prefix):
    xx,yy,zz=(correlation(counts[prefix+x]) for x in ('XX','YY','ZZ'))
    return (1+xx-yy+zz)/4


def score(record,*,validated=True):
    if validated: validate(record)
    c=record['counts'];G=record['decoder']['G']
    F0=bell(c,'n1_f0_')
    N=sum(c['n1_f1_ZZ'].values());agree=sum(n for bits,n in c['n1_f1_ZZ'].items() if bits[0]==bits[1])/N
    F1=.5*((1-P)*agree+P*(1-agree))
    f_one=.5*(F0+F1)
    F00=bell(c,'n2_f00_')
    F10=(1-P)*bell(c,'n2_f10_x0_')+P*bell(c,'n2_f10_x1_')
    F01=(1-P)*bell(c,'n2_f01_x0_')+P*bell(c,'n2_f01_x1_')
    sigmas=[]
    for z in range(4):
        probs=[];comp={}
        for basis in 'XYZ':
            row=c['n2_f11_'+basis]
            N=sum(row.values());mass=moment=0.
            for bits,n in row.items():
                if int(bits[-2])+2*int(bits[-3]) !=z:continue
                mass+=n/N;moment+=n/N*(1 if bits[-1]=='0' else -1)
            probs.append(mass);comp[basis]=moment
        sigmas.append((sum(probs)/3,comp))
    F11=0.
    for b in range(3):
        gram=G[str(b)];re,im=gram['re'],gram['im']
        for z,(weight,comp) in enumerate(sigmas):
            pb=0.
            for flip in range(4):
                if ((z&1)^(flip&1)) + (((z>>1)&1)^((flip>>1)&1))!=b:continue
                pb+=(P if flip&1 else 1-P)*(P if flip&2 else 1-P)
            tr=((weight+comp['Z'])/2*re[0][0]
                 +(weight-comp['Z'])/2*re[1][1]
                 +comp['X']*re[1][0]+comp['Y']*im[1][0])
            F11+=pb*tr/2
    f_two=(F00+F10+F01+F11)/4
    return {'one_use':f_one,'two_use':f_two,'gain':f_two-f_one,
            'one_use_branches':{'kept':F0,'erased':F1},
            'two_use_branches':{'00':F00,'10':F10,'01':F01,'11':F11}}


def self_test():
    r=json.loads((HERE/'raw_counts_and_decoder.json').read_text())
    x=score(r)
    expected=(.634979987819821,.6611135918720777,.02613360405225673)
    for actual,value in zip((x['one_use'],x['two_use'],x['gain']),expected):
        assert abs(actual-value)<1e-12,(actual,value)
    assert abs(x['two_use_branches']['10']-x['two_use_branches']['01'])<.02
    fail=json.loads((HERE/'v1_negative_result.json').read_text())
    legacy={**r, 'job':fail['job'], 'layout':fail['layout'],
            'raw_results_sha_git_blob':fail['source_git_blob'], 'counts':fail['counts']}
    f=score(legacy)
    assert abs(f['gain']-fail['reported_gain'])<1e-12
    assert f['gain'] < 0
    from copy import deepcopy
    for change in ('missing','wrong-shots','negative','wrong-basis','changed-decoder'):
        t=deepcopy(r)
        if change=='missing':del t['counts']['n2_f11_X']
        elif change=='wrong-shots':t['counts']['n1_f0_XX']['10']-=1
        elif change=='negative':t['counts']['n1_f0_XX']['10']=-1
        elif change=='wrong-basis':t['counts']['n1_f0_XX']['bogus']=1
        elif change=='changed-decoder':t['decoder']['G']['1']['im'][1][0]+=.1
        try:score(t)
        except ValueError:pass
        else:raise AssertionError('tamper was accepted: '+change)
    print(json.dumps({'verification':'PASS','status':'LOCAL_RESCORING_OF_COMMITTED_IBM_COUNTS_NOT_PROVIDER_AUTHENTICATION',
                          'failed_first_layout':f,**x},indent=2))

if __name__=='__main__':self_test()
