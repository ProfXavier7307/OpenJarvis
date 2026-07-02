# Security Hardening Defaults

This fork keeps the OpenJarvis stack, but changes the default posture for high-risk local actions.

## What this branch changes

- Capability policy is now deny-by-default when an agent has no explicit policy.
- `shell_exec` is a fail-closed stub and does not run host commands.
- `file_read` is a fail-closed stub and does not read host files.
- `file_write` is a fail-closed stub and does not modify host files.

## Why

A personal AI assistant should not start with broad access to the host shell or filesystem. Those abilities are useful later, but they should be exposed only through narrow tools that perform one approved action at a time.

## Recommended next step

Instead of re-enabling generic tools, add small purpose-built tools such as:

- `open_allowed_app` — opens apps from a hardcoded allowlist.
- `read_workspace_file` — reads files only under a configured workspace folder.
- `write_workspace_note` — writes only to a notes folder controlled by the assistant.
- `minecraft_rcon_command` — sends only approved Minecraft server commands.

## Still not handled in this branch

These should be reviewed before running on a main machine:

- External analytics defaults.
- Public skill/plugin installation and auto-sync.
- One-line remote installers.
- Connector credentials for Gmail, Discord, Slack, email, etc.
- Any server mode exposed beyond `127.0.0.1`.
