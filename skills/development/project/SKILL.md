---
name: ProjectSkill
description: Guidelines and instructions for starting, switching, deleting, and managing sandbox workspaces.
tools: [startProject, stopProject, deleteProject, listProjects]
---

# Project Workspace Management Skill

This skill guides the agent in managing multiple project workspaces, sandboxing commands, and switching active directories.

## Setup Instructions

- **Prerequisites**: Ensure `startProject`, `stopProject`, `deleteProject`, and `listProjects` tools are registered in `ToolRegistry`.
- **Directory Permissions**: Sandbox root directory `./session/projects/` (or `~/.nadia/session/projects/`) must have read, write, and directory creation permissions.
- **Database Tracking**: Relational database connection active if project metadata persistence is enabled in `application.yml`.

---

## Project Workspace Sandboxing

Nadia supports sandboxed project workspaces. When a project is started, the workspace context is changed from `./session` to `./session/projects/[Project Name]`.
This allows working on multiple distinct directories independently.

## Guidelines

### 1. Starting or Switching to a Project

- To start a new project or switch to an existing one, call `startProject` with the project name.
- **IMPORTANT**: Once a project is started, the current base directory of execution becomes `./session/projects/[Project Name]`. All relative path operations and skills reference files within this project sandbox.
- When running commands via `executeSessionCommand` while a project is active, the relative path to the skill directory must be addressed as `../../../skills/` instead of `../skills/`.

### 2. Stopping a Project

- When the work on a project is finished, call `stopProject` to reset the active sandbox context back to the default `./session` directory.

### 3. Deleting a Project

- When a user requests to delete a project, it deletes the database reference and deletes all local project files recursively.
- **IMPORTANT**: Deletion is permanent and requires a confirmation. Always verify the request first by prompting or verifying `confirm=true` is specified.
