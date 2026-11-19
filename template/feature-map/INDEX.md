# Feature index

One row per feature. Open the spec in the "Spec" column; terms are in [GLOSSARY.md](GLOSSARY.md), rules for every feature in [principles.md](principles.md), and the reasoning behind product decisions in [decisions/](decisions/).

Status per platform, in the order iOS / Android / Web / Backend (the order of `status` in [features/_template.md](features/_template.md)):

| Status | Meaning |
|---|---|
| `implemented` | Built and released. |
| `in-progress` | Partly built. |
| `planned` | Decided and scheduled, not built. |
| `n/a` | Does not exist on that platform by design. |

## Accounts and access

| ID | Feature | Summary | iOS / Android / Web / Backend | Spec |
|---|---|---|---|---|
| AUTH | Sign-in | Signing in with email and password, the errors a sign-in can meet, and signing out. | implemented / implemented / planned / implemented | [features/sign-in.md](features/sign-in.md) |
