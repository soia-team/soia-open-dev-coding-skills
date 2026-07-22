# THIRD_PARTY_NOTICES

> Last updated: 2026-07-22
> License values are metadata snapshots. Recheck the upstream source before reuse.

## Managed external CLIs

| Upstream | License snapshot | Used by | Relationship |
|---|---|---|---|
| [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | Apache-2.0 | `soia-dev-agent-cli-dispatch` | User-installed external AI CLI that the skill can dispatch. |
| [google-antigravity/antigravity-cli](https://github.com/google-antigravity/antigravity-cli) | NOASSERTION | `soia-dev-agent-cli-dispatch` | User-installed external AI CLI (`agy`) that the skill can dispatch; no code is copied. |

The dispatcher can also invoke other user-installed AI CLIs. They are execution targets rather than dependencies distributed by this repository and are not enumerated here.

## Maintenance

- NOASSERTION upstreams remain external tools; do not copy their code.
- Record newly documented upstream links or install commands here.
