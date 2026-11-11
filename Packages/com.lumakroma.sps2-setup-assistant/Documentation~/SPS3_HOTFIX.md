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
