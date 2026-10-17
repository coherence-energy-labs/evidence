#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
expected=json.loads((root/'MANIFEST.json').read_text())
assert expected['schema']=='oneq-public-review-integrity-v1'
for path,sha in expected['sha256'].items():
    f=root/path
    if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=sha:
        raise SystemExit(f'INTEGRITY FAIL {path}')
print('PASS',len(expected['sha256']),'source bytes pinned; self-pinned manifest is NOT an issuer signature')
