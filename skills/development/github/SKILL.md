---
name: GitHubCLI
description: Guidelines and command-line references for Git and GitHub operations using the GitHub CLI (gh) tool, including issue management, pull requests, repository operations, direct API calls, and action workflow runs.
tools: [executeSessionCommand]
---

# GitHub CLI Skill

This skill provides references and instructions for managing GitHub repositories, issues, pull requests, workflows, and raw API queries using the GitHub CLI (`gh`).

All commands are executed inside the `./session` sandbox environment using the `executeSessionCommand` tool (running via Windows `cmd.exe`).

---

## Execution Guidelines

1. **Host Environment**: Commands execute in Windows `cmd.exe`. Use Windows-compatible command formatting or cross-platform Python scripts when scripting filesystem actions.
2. **Authentication**: The GitHub CLI is already pre-configured and authenticated on the host machine. Do not attempt to run `gh auth login`.
3. **Current Context**: Commands naturally run in the context of the repository/folder where the shell is executing. When running inside the `./session` directory, make sure you clone or navigate to the target repository folder using the `dir` argument in `executeSessionCommand`.

---

## Command Reference

### 1. Authentication Status

Verify authentication state and verify username context.

```cmd
gh auth status
```

### 2. Issue Management

#### List Issues

Retrieve open issues (limited to 10 by default to prevent output flood).

```bash
gh issue list --limit 10 [--state open|closed|all] [--assignee "@me"]
```

#### View Issue

Get details and comments for a specific issue.

```bash
gh issue view [issue_number] [--comments]
```

#### Create Issue

Open a new issue with a title and body.

```bash
gh issue create --title "[Issue Title]" --body "[Detailed Markdown Body]" [--assignee "[username]"] [--label "[label]"]
```

#### Close/Reopen Issue

```bash
gh issue close [issue_number]
gh issue reopen [issue_number]
```

#### Add Comment

Post a comment to an issue.

```bash
gh issue comment [issue_number] --body "[Comment Text]"
```

### 3. Pull Request (PR) Management

#### List Pull Requests

```bash
gh pr list --limit 10 [--state open|closed|merged|all] [--base [branch]]
```

#### View PR Details

```bash
gh pr view [pr_number] [--comments]
```

#### Create Pull Request

Create a PR from the current head branch.

```bash
gh pr create --title "[PR Title]" --body "[PR Description]" --base [target_branch] --head [source_branch]
```

#### Checkout PR Branch

Checks out the branch for the specified PR locally.

```bash
gh pr checkout [pr_number]
```

#### Review PR

Submit a code review.

```bash
gh pr review [pr_number] [--approve|--comment|--request-changes] --body "[Review text]"
```

#### Merge PR

Merge the pull request.

```bash
gh pr merge [pr_number] [--merge|--squash|--rebase] --delete-branch
```

#### View PR Changes

View diff for a pull request.

```bash
gh pr diff [pr_number]
```

### 4. Repository Operations

#### Clone Repository

Clones a repository into the session directory.

```bash
gh repo clone [owner]/[repo]
```

#### View Repository Info

```bash
gh repo view [owner]/[repo]
```

#### Create Repository

```bash
gh repo create [repo_name] --public|--private [--clone]
```

#### Fork Repository

```bash
gh repo fork [owner]/[repo] [--clone]
```

### 5. Tag & Release Operations

#### Create and Push Git Tag

```bash
git tag -a [tag_name] -m "[Tag message/description]" [commit_sha]
git push origin [tag_name]
```

#### List Tags

```bash
git tag -l
```

#### Delete Git Tag

```bash
git tag -d [tag_name]
git push origin --delete [tag_name]
```

#### Create GitHub Release

Creates a GitHub release (this also creates the git tag automatically if it doesn't exist yet).

```bash
gh release create [tag_name] [--title "[title]"] [--notes "[notes]"] [--draft] [--prerelease] [files...]
```

#### List Releases

```bash
gh release list --limit 10
```

#### Create Tag Ref via GitHub REST API

Directly create a tag reference on GitHub via the API without local git repo checkout.

```bash
gh api -X POST repos/{owner}/{repo}/git/refs -f ref="refs/tags/[tag_name]" -f sha="[commit_sha]"
```

### 6. Workflow & Runs (GitHub Actions)

#### List Runs

View recent workflow runs.

```bash
gh run list --limit 10
```

#### View Run Status/Logs

```bash
gh run view [run_id] [--log]
```

#### Rerun Run

Trigger a rerun of a failed workflow run.

```bash
gh run rerun [run_id]
```

### 7. Raw API Operations (`gh api`)

For any GitHub functionality not supported by direct CLI commands, use the raw REST/GraphQL API.

#### GET Request

```bash
gh api repos/{owner}/{repo}/commits
```

#### POST Request

```bash
gh api -X POST repos/{owner}/{repo}/issues/{issue_number}/labels -F "labels[]=bug"
```

#### GraphQL Query

```bash
gh api graphql -F query='query { viewer { login } }'
```
