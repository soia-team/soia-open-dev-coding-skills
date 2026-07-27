# Collaborator Access Management


Use for: "给 `<user>` 在 `<repo>` 加个能提交 PR 的权限" / "把 xxx 加到这个仓库" /
"看看这个仓库现在有哪些协作者" / "把 xxx 从这个仓库移除".

### Permission levels

GitHub collaborator permissions, narrowest to broadest:

| Level | Grants | Typical fit |
|---|---|---|
| `pull` | Read-only; can fork and open cross-fork PRs | External contributor on a private repo — on a public repo, anyone can already fork and PR without being added at all |
| `triage` | `pull` + manage issue/PR labels and assignees, no code writes | Triage-only, no code access |
| `push` | `triage` + push branches, open PRs from branches in the repo itself | What "能提交 PR 的权限" usually means |
| `maintain` | `push` + manage some repo settings (not sensitive ones, not collaborators) | Needs to manage issue templates/wiki, not full admin |
| `admin` | Full control: delete repo, manage collaborators, manage secrets | Rare; treat as a distinct, higher-bar request |

Default rule: when the user says "加个能提交 PR 的权限" without naming a
level, confirm whether the person is an internal collaborator (→ `push`)
or an external contributor (→ usually no grant needed on a public repo;
on a private repo, `pull` or `triage` is enough to see the repo and open
PRs against it — `push` is more than they need). Do not default to `push`
without asking when it's ambiguous which case this is. Never grant
`maintain`/`admin` unless the user names that level explicitly.

### Commands

```bash
# List current collaborators and their permission (read-only, always safe)
gh api repos/<owner>/<repo>/collaborators \
  --jq '.[] | {login: .login, permission: .role_name}'

# Look up one person's current permission (read-only)
gh api repos/<owner>/<repo>/collaborators/<username>/permission \
  --jq '{permission: .permission, role_name: .role_name}'

# Grant or change a collaborator's permission (write — see Safety Gate below)
gh api repos/<owner>/<repo>/collaborators/<username> \
  -X PUT -f permission=<pull|triage|push|maintain|admin>

# Remove a collaborator (write — same Safety Gate)
gh api repos/<owner>/<repo>/collaborators/<username> -X DELETE
```

### Safety Gate

This is the one operation in this skill that never runs on inferred intent —
restate and get explicit confirmation on all of the following in the current
exchange before the write call:

- Target repo: `<owner>/<repo>`
- Target user: the actual GitHub username, not a display name or email —
  if you only have an email or display name, resolve the username first
  (`gh api "search/users?q=<query>"` — note the query goes in the URL so `gh
  api` stays a GET; passing it via `-f` would switch the call to a POST and
  fail — or ask the user) rather than guessing the spelling
- Permission level: `pull` / `triage` / `push` / `maintain` / `admin`
- If revoking: confirm this removes their direct collaborator access —
  it does not close their open PRs/branches (this skill does not cascade
  that cleanup), and it does not touch access granted through org Team
  membership, which is a separate permission path this call cannot revoke

Inviting someone to a private repo sends them a GitHub notification/email —
an externally visible action — so the confirmation gate applies even when it
feels like "just adding one person."

### Verify after granting

```bash
gh api repos/<owner>/<repo>/collaborators/<username>/permission \
  --jq '.permission'
```

Confirm the returned value matches what was requested before reporting
success. Do not treat a 2xx response alone as proof the grant took effect:
GitHub's collaborator-add endpoint returns `201` when it creates a pending
invitation (not in effect until the person accepts) versus `204` when it
updates an existing collaborator (in effect immediately) — for a `201`, say
explicitly in the report that access is pending acceptance, not yet active.

### Verify after revoking

```bash
gh api repos/<owner>/<repo>/collaborators/<username> --silent && echo "still a direct collaborator" || echo "removed as direct collaborator"
```

A successful `DELETE` (2xx) only means direct-collaborator access is gone —
it is not proof the person has no access at all. If `<owner>` is an org (not
a personal account), check whether a Team grants them access independently
before reporting "access revoked" as a complete statement:

```bash
gh api orgs/<owner>/teams --jq '.[].slug' \
  | xargs -I{} gh api orgs/<owner>/teams/{}/repos/<owner>/<repo> --silent 2>/dev/null \
    && echo "a team still grants access to this repo — check its membership"
```

If any Team still has access to the repo, report both facts separately:
direct-collaborator access removed, Team-based access (if applicable)
unchanged — do not collapse them into one "access revoked" claim.
