# Evidence

**Every public claim Coherence Energy Labs makes resolves to an entry in this repository - or it doesn't get made.**

Each entry under [`claims/`](claims/) is a machine-readable `claim.json` stating exactly what is claimed, what its evidence status is, and - where the status permits - how a stranger can verify it with no trust in us. This is the same standard we apply to our own systems (receipts, gates that can say no, falsification-first), applied to our marketing surface.

## Statuses

| Status | Meaning |
|---|---|
| `verified-public` | You can check this yourself, today, with linked artifacts and commands. A claim only carries this status if the verification path has actually been executed. |
| `private-development` | The capability and its gates exist in private repositories. We attest to it; you cannot currently check it. We say so plainly instead of implying otherwise. Verification packages can be arranged for serious counterparties - [contact us](mailto:info@coherenceenergylabs.com). |
| `research` | A hypothesis under active investigation. Not a demonstrated capability, and never presented as one. |
| `retired` / `falsified` | A claim we no longer make, preserved with the reason. Negative results are load-bearing. |

## The claims

| Claim (as stated on the [org profile](https://github.com/coherence-energy-labs)) | Status |
|---|---|
| [0 ULP drift across CPU, GPU, WASM, and browser](claims/0-ulp-cross-substrate/) | `verified-public` (browser demos; full torture suites private) |
| [Compiler equivalence proven over all 2⁶⁴ⁿ inputs](claims/compiler-equivalence-proofs/) | `private-development` |
| [7 compilation backends proven to agree](claims/seven-backends/) | `private-development` |
| [29 cryptographic primitives verified byte-exact](claims/crypto-29-primitives/) | `private-development` |
| [15 formally model-checked protocol specifications](claims/protocol-model-checking/) | `private-development` |
| [~9 ms million-point GPU proof round; client-side verification](claims/gpu-proof-9ms/) | `private-development` (client-side verification is `verified-public` via The Gauntlet) |
| [The org banner is a re-executable figure](claims/org-banner-re-executable/) | `verified-public` |
| [HazardPulse forecasts are signed, frozen before outcomes, and stranger-verifiable](claims/hazardpulse-signed-forecasts/) | `verified-public` |

## Why publish attestations at all?

Because the honest alternative to "trust us" is not silence - it is a precise statement of what you *can* and *cannot* check. We build provable-ignorance certificates into our AI systems; this repository is the same idea applied to our own disclosure. When a `private-development` claim gains a public verification path, its status changes here, in a commit you can diff.

---

Maintained by [Coherence Energy Labs](https://coherenceenergylabs.com) · [info@coherenceenergylabs.com](mailto:info@coherenceenergylabs.com)
