# Security Hardening Defaults

This fork keeps the OpenJarvis stack, but changes the default posture for high-risk local actions.

## What this branch changes

- Capability policy is now deny-by-default when an agent has no explicit policy.
- `shell_exec` is a fail-closed stub and does not run host commands.
- `file_read` can read files only inside `Personal-Memory` at the OpenJarvis repository/install root.
- `file_write` is a fail-closed stub and does not modify host files.
- `Personal-Memory/.gitignore` keeps local memory files from being committed by default.

## Why

A personal AI assistant should not start with broad access to the host shell or filesystem. File access is limited to one intentional memory folder so the assistant can use local notes without seeing the rest of the machine.

## Personal-Memory usage

Create local memory files after cloning or installing the project:

- `Personal-Memory/profile.md`
- `Personal-Memory/projects/doa.md`
- `Personal-Memory/preferences.md`

The restricted `file_read` tool accepts paths like `profile.md`, `projects/doa.md`, or `Personal-Memory/profile.md`. Path traversal outside `Personal-Memory` is denied.

Do not commit private memory files. This fork is public, and the folder's `.gitignore` is designed to keep your local notes local. The safe pattern is to keep real memory files only on your computer, not in GitHub.

## Recommended next step

Instead of re-enabling generic tools, add small purpose-built tools such as:

- `open_allowed_app` — opens apps from a hardcoded allowlist.
- `write_workspace_note` — writes only to a notes folder controlled by the assistant.
- `minecraft_rcon_command` — sends only approved Minecraft server commands.

## Still not handled in this branch

These should be reviewed before running on a main machine:

- External analytics defaults.
- Public skill/plugin installation and auto-sync.
- One-line remote installers.
- Connector credentials for Gmail, Discord, Slack, email, etc.
- Any server mode exposed beyond `127.0.0.1`.
