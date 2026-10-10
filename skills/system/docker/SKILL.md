---
name: DockerSkill
description: Guidelines and tool instructions for discovering, inspecting, monitoring, starting, stopping, restarting, running, and diagnosing Docker containers, container images, and container logs using DockerTool.
tools: [dockerListContainers, dockerContainerLogs, dockerStartContainer, dockerStopContainer, dockerRestartContainer, dockerRemoveContainer, dockerListImages, dockerInspectContainer, dockerRunContainer, dockerCheckContainers]
---

# Docker Container & Infrastructure Skill

This skill outlines how the agent interacts with the Docker engine and manages containerized infrastructure via the `DockerTool` suite.

---

## 1. Available Tools Overview

| Tool | Purpose | Key Parameters |
| :--- | :--- | :--- |
| `dockerListContainers` | Lists active or all containers | `all` (boolean: true to include stopped) |
| `dockerListImages` | Lists locally cached container images | *None* |
| `dockerContainerLogs` | Fetches console logs (stdout/stderr) | `containerIdOrName` (string), `tailLines` (int) |
| `dockerInspectContainer` | Returns complete low-level JSON metadata | `containerIdOrName` (string) |
| `dockerRunContainer` | Launches a new detached container | `image` (string), `name` (opt), `ports` (opt), `env` (opt), `volumes` (opt) |
| `dockerStartContainer` | Starts an existing stopped container | `containerIdOrName` (string) |
| `dockerStopContainer` | Gracefully stops a running container | `containerIdOrName` (string) |
| `dockerRestartContainer` | Reboots a container | `containerIdOrName` (string) |
| `dockerRemoveContainer` | Deletes a container instance | `containerIdOrName` (string), `force` (boolean) |
| `dockerCheckContainers` | Audits entire fleet for abnormal exit codes | *None* |

---

## 2. Discovery & Auditing Guidelines

### 2.1 Listing Containers (`dockerListContainers`)
- **Active Containers Only**: Call `dockerListContainers(all: false)` to see healthy running containers, port mappings, and uptime.
- **All Containers (Including Stopped/Exited)**: Call `dockerListContainers(all: true)` to check terminated or non-running containers.
- **Status Decoding**:
  - `Up X minutes / hours`: Healthy running state.
  - `Exited (0)`: Cleanly finished task (e.g. batch jobs or migrations).
  - `Exited (1)` or non-zero: Process crash or configuration failure.
  - `Exited (137)`: Killed by OOM (Out Of Memory) killer or `SIGKILL`.

### 2.2 Fleet Health Check (`dockerCheckContainers`)
- Use `dockerCheckContainers()` to perform a fleet-wide health audit.
- Scans all containers and automatically publishes `container_crashed` staff events into the Nadia event pipeline for any containers with non-zero exit codes.

### 2.3 Image Inventory (`dockerListImages`)
- Call `dockerListImages()` to verify whether an image (e.g. `postgres:16-alpine`, `redis:7-alpine`) is cached locally before attempting to run it.

---

## 3. Container Lifecycle Management

### 3.1 Starting, Stopping, and Restarting
- **Start**: `dockerStartContainer(containerIdOrName: "<id_or_name>")`
  - Resumes an existing stopped container without altering storage or port allocations.
  - Dispatches `container_started` staff event upon success.
- **Stop**: `dockerStopContainer(containerIdOrName: "<id_or_name>")`
  - Sends `SIGTERM` followed by `SIGKILL` for graceful shutdown.
  - Dispatches `container_stopped` staff event upon success.
- **Restart**: `dockerRestartContainer(containerIdOrName: "<id_or_name>")`
  - Reboots a container to apply configuration changes or recover from a hung state.
  - Dispatches `container_restarted` staff event upon success.

### 3.2 Removing Containers (`dockerRemoveContainer`)
- **Safe Removal**: `dockerRemoveContainer(containerIdOrName: "<id_or_name>", force: false)` removes stopped containers.
- **Force Removal**: `dockerRemoveContainer(containerIdOrName: "<id_or_name>", force: true)` forcefully terminates and deletes a running or unresponsive container.
- Dispatches `container_removed` staff event upon completion.

---

## 4. Spawning New Containers (`dockerRunContainer`)

Use `dockerRunContainer` to launch a new container in detached (`-d`) mode:

```json
{
  "image": "postgres:16-alpine",
  "name": "nadia-postgres",
  "ports": "5432:5432",
  "env": "POSTGRES_DB=nadia,POSTGRES_USER=nadia,POSTGRES_PASSWORD=secret",
  "volumes": "nadia_pg_data:/var/lib/postgresql/data"
}
```

### Parameter Rules:
- **`image`** *(Required)*: Repository name and tag (e.g. `"redis:7-alpine"`, `"nginx:alpine"`).
- **`name`** *(Optional)*: Custom container name (e.g. `"local-redis"`).
- **`ports`** *(Optional)*: Host-to-container port mapping (e.g. `"8080:80"`, `"6379:6379"`).
- **`env`** *(Optional)*: Comma-separated list of `KEY=VALUE` environment variables.
- **`volumes`** *(Optional)*: Volume or bind mount string (e.g. `"/host/path:/container/path"`).

---

## 5. Troubleshooting & Diagnostics

### 5.1 Reading Logs (`dockerContainerLogs`)
- Always inspect container logs when a service fails to start or exits prematurely:
  ```
  dockerContainerLogs(containerIdOrName: "<name_or_id>", tailLines: 100)
  ```
- Look for database connection timeouts, syntax errors in application config, or missing environment variables.

### 5.2 Deep Inspection (`dockerInspectContainer`)
- Call `dockerInspectContainer(containerIdOrName: "<name_or_id>")` to retrieve full JSON configuration:
  - Network IP addresses and bridge gateway.
  - Mounted volume host bindings.
  - Exact runtime environment variables.
  - Healthcheck state history and exit codes.

---

## 6. Diagnostic Workflow Guide

```
┌───────────────────────────────┐
│     dockerCheckContainers     │ ──► Identify crashed/stopped containers
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│      dockerContainerLogs      │ ──► Inspect root cause (exceptions, port bind errors)
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│    dockerRestartContainer     │ ──► Restart or fix via dockerRunContainer
└───────────────────────────────┘
```

## Setup Instructions

### 1. Prerequisites & Docker Daemon
- **Docker Engine / Desktop**: Docker must be installed and running on the host machine.
- **Daemon Socket / Pipe Configuration**:
  - **Linux / macOS**: Ensure the Unix socket at `/var/run/docker.sock` is accessible with appropriate read/write permissions for the Nadia process.
  - **Windows**: Ensure the Windows named pipe `//./pipe/docker_engine` is enabled or TCP daemon listening on `tcp://localhost:2375`.
- **Nadia Docker Client**: Nadia utilizes standard Docker Java client libraries (`DockerTool`) to communicate with the daemon.

### 2. Permissions & Container Resource Constraints
- **User Groups**: On Linux environments, ensure the running user is added to the `docker` user group (`sudo usermod -aG docker $USER`).
- **Resource Allocations**: Ensure Docker Engine has sufficient CPU, memory, and disk space allocated for running development sandboxes, databases, and microservices.

