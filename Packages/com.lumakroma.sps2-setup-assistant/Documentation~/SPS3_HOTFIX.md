# SPS3 menu compatibility hotfix

## Context Check

- Request: temporary fix for `SPS2 build stopped: Legacy compatibility menu is missing.` in the user's fork.
- Baseline: upstream 1.1.1, commit `7a08706298b91b678a8324b4e60186792cebf539`.
- Compared dependency: VRCFury 1.1452.0, commit `dcd470dd47de78eb4a57e85f27ab14ff7d90cfe7`.
- Scope: recognize the observed SPS3 Auto and Legacy Support menu labels, retaining the SPS1/SPS2 exact labels and duplicate/missing-control guards.
- Non-goals: full SPS3 feature support, changing native SPS Options, shader/contact changes, dependency upgrades or publishing a release/VPM feed.
- Invariants: work only on the existing build clone; no source avatar mutation, dependency patching, fuzzy label matching or suppression of unrelated build errors.
- Validation: add Unity EditMode regression cases; run available static checks and package validation where PowerShell is available. Unity and VRChat runtime verification remain required.
- Workflow: this fork has Issues disabled. This branch and its draft PR track the user-authorized temporary patch instead of an upstream issue. No upstream submission or merge is included.

## Implementation

The existing build lookup now accepts both observed label variants in one exact-match search. Ambiguous variants are rejected together. Native menu control references, types, parameters and build-token checks are preserved.

## Known limits

This patch does not adapt obsolete useLights writes to SPS Options. It also does not relax missing Stealth or disabled-native-option errors, or replace the existing Write Defaults repair. The dependency's default Legacy Support option is the targeted configuration. The package identity/version remains upstream 1.1.1 for this unmerged patch; no distribution release is created.

## Validation status

- Reviewed the patch against the exact VRCFury source revision above.
- `git diff --check` and `git diff --cached --check`: passed locally.
- Nine Unity EditMode regression cases added for old/new labels, ambiguity, non-Toggle controls and exact socket tokens; not executed (Unity is unavailable).
- Local `Tools/Validate-Package.ps1`: not run successfully because PowerShell is unavailable. The existing Windows CI workflow is the intended package validation gate.
- No Unity compilation, SDK build or VRChat runtime pass is claimed.
