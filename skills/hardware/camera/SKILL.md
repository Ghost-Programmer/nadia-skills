---
name: camera
description: Discovers, connects, streams, captures snapshots, and records video from local USB webcams, ONVIF/RTSP/MJPEG IP cameras, and Bambu Lab 3D printer chamber cameras (storing media under ~/.nadia/captures).
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: hardware
  display-name: CameraSkill
allowed-tools: listCameras discoverCameras addRemoteIpCamera removeCamera connectCamera disconnectCamera takePhoto startRecording stopRecording getCameraCapabilities openCameraViewer
tools: [listCameras, discoverCameras, addRemoteIpCamera, removeCamera, connectCamera, disconnectCamera, takePhoto, startRecording, stopRecording, getCameraCapabilities, openCameraViewer]
---

# Camera & Visual Inspection Skill

Provides procedural instructions for discovering, connecting, streaming, capturing high-resolution still photos, and recording video from local USB/integrated webcams, LAN/WAN IP cameras (MJPEG, RTSP, HTTP Snapshot, ONVIF), and Bambu Lab 3D printer chamber cameras (`cam-bambu-<ip>`).

---

## Setup Instructions

### External App & Integration Setup

1. **USB / Integrated UVC Webcams & EMEET Pixy AI PTZ Camera**:
   - Plug the camera into a host USB port and grant OS camera permissions to Java/Nadia:
     - **Windows**: *Settings ➔ Privacy & security ➔ Camera ➔ Let desktop apps access your camera (On)*.
     - **macOS**: *System Settings ➔ Privacy & Security ➔ Camera*.
     - **Linux**: Ensure your user belongs to the `video` group (`sudo usermod -aG video $USER`).
   - **EMEET Pixy AI PTZ**: Works natively over USB UVC + USB HID (`hid4java`) for hardware AI tracking, pan-tilt-zoom actuation, and DSP audio modes without third-party vendor software.
2. **ONVIF / RTSP / MJPEG Network IP Cameras**:
   - In your IP camera's admin web interface, enable **ONVIF** and/or **RTSP** streaming and create a camera username/password.
   - Approve the local LAN subnet in **View ➔ 🌐 Network Engineer** (`approveCurrentNetwork`), then run `discoverCameras()` or register the stream URL via `addRemoteIpCamera` / **View ➔ 📷 Camera Monitor**.
3. **Bambu Lab 3D Printer Chamber Cameras (`cam-bambu-<ip>`)**:
   - Configure the printer in **⚙️ System Settings ➔ Bambu 3D Printers** on an approved network; Nadia automatically registers its TLS chamber feed (`port 6000` / `322`) as `cam-bambu-<ip>`.

---

## 1. Capture Storage & Camera Identifiers

- **Photo Capture Directory**: Still photos captured via `takePhoto` are stored by default under `~/.nadia/captures/photos/`.
- **Video Capture Directory**: Video recordings captured via `startRecording` / `stopRecording` are stored by default under `~/.nadia/captures/videos/`.
- **Bambu 3D Printer Chamber Cameras**: Discovered Bambu Lab 3D printers with integrated chamber cameras are automatically registered in the camera list with ID `cam-bambu-<ip>` (type `BAMBU_3D_PRINTER`, TLS JPEG stream on port `6000` or RTSPS on port `322`).

---

## 2. Core Operational Workflows

### 2.1 Camera Discovery & Inspection
1. **List Registered Cameras**:
   - Call `listCameras()` to inspect all currently registered local webcams, network IP cameras, and Bambu 3D printer chamber cameras along with their status (`CONNECTED`, `STREAMING`, `DISCONNECTED`), FPS, resolution, and recording state.
2. **Active Hardware & Network Discovery**:
   - Call `discoverCameras()` to scan for newly attached USB cameras and probe the local subnet for ONVIF cameras (subject to Zero-Trust network approval).
3. **Inspect Capabilities**:
   - Call `getCameraCapabilities(cameraId)` to check supported resolutions, frame rates, and PTZ capabilities.

### 2.2 Stream Connection & Snapshot Capture
1. **Connect Stream**:
   - Call `connectCamera(cameraId)` to start live frame acquisition, or `openCameraViewer(cameraId)` to open the interactive Camera Monitor window in the Nadia desktop UI.
2. **Capture Still Photo**:
   - Call `takePhoto(cameraId, savePath)` (pass `null` or `""` for `savePath` to store automatically in `~/.nadia/captures/photos/`).
3. **Record Video**:
   - Call `startRecording(cameraId, savePath)` to begin recording to `~/.nadia/captures/videos/`, and call `stopRecording(cameraId)` to finalize the video file.
4. **Disconnect Stream**:
   - Call `disconnectCamera(cameraId)` when live streaming is no longer needed.

### 2.3 Automated 1-Minute 3D Print Visual Defect Inspection
- When a Bambu Lab 3D printer is actively printing (`RUNNING` / `Printing`), Nadia automatically captures a snapshot every 60 seconds from `cam-bambu-<ip>` into `~/.nadia/captures/photos/` and dispatches it to the **3D Printer** staff specialist to inspect for:
  1. **Clogged or Jammed Extruder**
  2. **Under-Extrusion & Gaps**
  3. **Stringing & Oozing**
  4. **First-Layer Detachment & Warping**
- If any defect is detected, the print is immediately paused (`pausePrintJob`) and an alert is dispatched to the Slack Alert channel (`sendSlackNotification`).
