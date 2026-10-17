# Referee requirements for candidate B

| Gate | Status |
|---|---|
| 22 matched named circuit-count dictionaries per run, all 4000 shots | PASS (stored data; 88k shots/run) |
| No omitted negative first run | PASS (v1 and v2 included) |
| Independent branch scorer matches all six reported branch/aggregate values | PASS (Python stdlib, separately implemented) |
| Independent bootstrap confidence interval near stored report | PASS under independent multinomial shot assumption |
| Tampered/missing/negative counts rejected | PASS (negative controls in script) |
| Independent authentication that IBM accepted and ran precisely these source/ISA circuits | PENDING; provider receipt, QPY and source compilation not public |
| Preregistration frozen before *each* submission, publicly auditable hash | PENDING private source release |
| Detector twirl dependence and time drift considered in confidence interval | PENDING |
| Prior-art and comparison class for any 'first' wording | PENDING; no public 'first' claim |
| Physical zero-capacity PPT and erasure channels on device | NOT TESTED; no superactivation claim |

**Publish as a pilot evidence note**, not a full breakthrough claim, until all authenticity/statistics/prior-art gates pass.
