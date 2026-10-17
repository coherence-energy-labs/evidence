# ONE_Q release candidate A: two-use finite-blocklength superactivation

**Status: PUBLIC MATHEMATICAL REVIEW CANDIDATE. Not peer reviewed. Not an experimental result.**

This **standalone** package does not require access to private ONE_Q. It isolates a two-use logical transmission construction and a proposed family of PPT channels, and gives strangers tests that can produce negative outcomes. It contains no private machine credentials, ONE_Q orchestration code, or hardware configuration.

## What is independently reproducible now

- `python verify_closed.py`: integer-isqrt rational enclosures, no dependencies. Checks the **explicit** code `|0_L> = |++>`, `|1_L> = |-->`, its four flagged branch fidelities and `F_e=(7-6p+2p^2)/8`. Certifies `F_e>3/4` for *each* `d >= 22` by monotonicity from `d=22` (for `p=1/(1+sqrt(d))`). Confirms the same simple code fails at `d=21`.
- `python -m pip install numpy` then `python check_ppt_small.py`: independently constructed Choi matrices for shield dimensions 2-5; checks positivity, trace preservation and PPT at the required mixture, then **refuses** PPT on a perturbed mixture. These small-matrix tests do NOT prove the general-dimension algebra.
- `proof_note.tex` and `proof_note.pdf`: mathematical definitions, proof steps, literature provenance, precise limitations and open referee checks.

## Claim gate

This is a **constructive candidate** for two-shot superactivation in the *finite-blocklength fidelity* sense of Parentin, Bergh, Datta and Wilde (2026), **with a different, larger PPT channel**. The article's 17-use demonstration was for its original `d=2` PPT channel. It is not a same-resource or same-channel 17-to-2 speedup.

**The full candidate theorem still depends on independently auditing** the analytical PPT spectrum of the general channel family, the exact simulation of the effective flagged channel from one `P_d x A_1/2` use, and all encoder/decoder CPTP operations. The archived private ONE_Q ledger claims these steps; the public scripts above cross-check important subsets but do not independently establish them for every `d`.

Private ONE_Q reports separately optimized d=20,21 code fidelities exceeding 3/4. Those numerical certificates do **not** ship here as independently verifiable decoder maps. They are explicitly **withheld from the theorem claim**, pending a complete portable witness and an external mathematical review.

## Other limits

- This is not hardware teleportation, and it is not an IBM-to-Japan quantum connection.
- Two uses counts joint channel calls, not physical qubits or gates. Shield dimension grows with d.
- We do not claim an improvement to the asymptotic capacity bound by itself.
- A broader literature/patent review, independent specialist review and company disclosure/IP review remain open.

## Prior work and credits

1. G. Smith and J. Yard (2008), original PPT/erasure quantum capacity superactivation.
2. M. Parentin, B. Bergh, N. Datta and M. M. Wilde, *Onset of superactivation of quantum capacity*, arXiv:2604.27042v2 (2026), finite-blocklength definition, base channel, reduction and 17-use numerical code: https://arxiv.org/abs/2604.27042
3. A. Rutkowski, M. Studzinski, P. Cwiklinski, M. Horodecki, Phys. Rev. A 91 012335 (2015), prior PPT private states in arbitrary dimensions: https://doi.org/10.1103/PhysRevA.91.012335
4. T. Cubitt et al., *Unbounded number of channel uses may be required to detect quantum capacity* (2015). Related two-switch-channel constructions are **not** the same finite-n fidelity claim.
5. Current private research basis: ONE_Q ledger R132, R140-R143 (2026-10-16), author-reported, not public scientific verification.

**Contact:** https://coherenceenergylabs.com. Authorship details and release license require an owner-approved publication check; this research package is an invitation to peer review, not an arXiv submission.
