# Sovereign AI Radio Station (`sovereign-ai-radio-station`)
**Autonomous 24/7 Cyber-Broadcast Playout Engine, Web Audio API DSP Ducking, Dynamic AI DJ Voice Synthesis, and Cross-Station Media Simulcast for Sovereign Biz Box**

[![Port](https://img.shields.io/badge/Port-8811-blue.svg?style=for-the-badge)](n8n/webhook_adapter.py)
[![Architecture](https://img.shields.io/badge/Architecture-Tier--1%20Production%20Hardened-brightgreen.svg?style=for-the-badge)](ROADMAP.md)
[![Status](https://img.shields.io/badge/Status-HEALTHY%20%7C%20ONLINE-success.svg?style=for-the-badge)](http://127.0.0.1:8811/health)
[![Package ID](https://img.shields.io/badge/Package%20ID-PKG--031-8A2BE2?style=for-the-badge)](https://github.com/BlackFoxgamingstudio/ai-radio-station)
[![n8n Node](https://img.shields.io/badge/n8n%20Node-SovereignAiRadioStation-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

---

## Table of Contents
1. [Executive Summary & Broadcast Manifesto](#1-executive-summary--broadcast-manifesto)
2. [Station Architecture & Playout Topology](#2-station-architecture--playout-topology)
3. [Cyber-Broadcast Web Console & Web Audio DSP Engine](#3-cyber-broadcast-web-console--web-audio-dsp-engine)
   - [3.1 Web Audio API 64-Band Real-Time Spectrum Visualizer](#31-web-audio-api-64-band-real-time-spectrum-visualizer)
   - [3.2 Hardware VU Meters & Peak Level Detection](#32-hardware-vu-meters--peak-level-detection)
   - [3.3 Sub-Second -14dB Audio Ducking DSP Curves](#33-sub-second--14db-audio-ducking-dsp-curves)
4. [Streaming Subsystem: HTTP 206 Partial Content & Byte-Range Requests](#4-streaming-subsystem-http-206-partial-content--byte-range-requests)
5. [Autonomous AI DJ Synthesis & Daypart Scheduling](#5-autonomous-ai-dj-synthesis--daypart-scheduling)
   - [5.1 Daypart Matrix & Programming Clock](#51-daypart-matrix--programming-clock)
   - [5.2 Dynamic AI DJ Interstitial Generation Engine](#52-dynamic-ai-dj-interstitial-generation-engine)
   - [5.3 Categorized Track Library Management](#53-categorized-track-library-management)
6. [SQLite Persistence Layer (`radio_schedule.db`)](#6-sqlite-persistence-layer-radio_scheduledb)
7. [Cross-Station Media Simulcast with TV Broadcast Station (`:8812`)](#7-cross-station-media-simulcast-with-tv-broadcast-station-8812)
8. [Comprehensive REST API Reference](#8-comprehensive-rest-api-reference)
9. [n8n Automation & Custom Community Node (`SovereignAiRadioStation`)](#9-n8n-automation--custom-community-node-sovereignairadiostation)
10. [SRE Runbook, Telemetry & Disaster Recovery](#10-sre-runbook-telemetry--disaster-recovery)
11. [Verification Suite & Automated Unit Tests](#11-verification-suite--automated-unit-tests)
12. [Authors, Governance & MIT License](#12-authors-governance--mit-license)

---

## 1. Executive Summary & Broadcast Manifesto

### 1.1 The Vision of Sovereign Cyber-Broadcasting
Traditional terrestrial radio and cloud-hosted streaming stations (e.g., Live365, Icecast relays, Spotify for Podcasters) introduce crippling latency, ongoing egress costs, and third-party platform censorship risks. Furthermore, conventional automated playout software lacks context-awareness: music stops abruptly for rigid commercial blocks, DJ breaks sound robotic, and synchronizing radio stems with live television broadcasts requires manual human studio engineering.

The **Sovereign AI Radio Station** (`PKG-031`) represents a paradigm shift: an autonomous, self-scheduling, 24/7 cyber-broadcast station microservice executing locally on loopback Port 8811 (`http://127.0.0.1:8811`). Designed as a foundational pillar of the **Sovereign Biz Box (SBB)** media cluster, this microservice blends high-fidelity audio playout, real-time Web Audio API signal processing, intelligent audio ducking curves, automated AI DJ interstitial voice synthesis, and synchronized multi-station simulcast with the TV Broadcast Station (`:8812`).

### 1.2 Five Core Engineering Tenets
The station is engineered according to five fundamental architectural tenets:

1. **Zero-Dropout Autonomous Playout**: The station runs 24 hours a day, 7 days a week, continuously streaming curated Lo-Fi, Deep Cyber-Builds, episodic narrative drama, and commercial station breaks without audio buffer underruns or operator intervention.
2. **Dynamic DSP Audio Ducking**: When an on-air AI DJ speaks or emergency station ident triggers, the background music bed automatically attenuates by exactly -14 dB along smooth logarithmic attack and release curves, guaranteeing perfect vocal clarity.
3. **HTTP 206 Partial Content Streaming**: Audio stems in arbitrary formats (`.mp3`, `.wav`, `.aif`, `.m4a`, `.ogg`) are streamed using standard HTTP Range headers, enabling instantaneous seeking, zero-latency buffer pre-loading, and full native HTML5 audio compatibility.
4. **Context-Aware Daypart Rotation**: The broadcast schedule dynamically morphs across four distinct operational dayparts (Morning Drive, Afternoon Cyber-Lab, Night Shift, and Deep Focus), adjusting tempo, genre selection, and DJ demeanor.
5. **Deterministic Simulcast Sync**: Serves as the authoritative audio engine for the television network, providing sample-accurate timecode synchronization between audio stems and 16:9 stage visual slide transitions.

---

## 2. Station Architecture & Playout Topology

The AI Radio Station operates as a high-performance Python FastAPI service integrated with the local SQLite persistence layer, native file system audio vaults, and the SBB Autonomous Command Center (`:5678`):

```
+===================================================================================================+
|                              SOVEREIGN AI RADIO STATION (:8811)                                   |
|                          FastAPI / Web Audio API DSP / SQLite WAL                                 |
+===================================================================================================+
|                                                                                                   |
|  [ Inbound Control Gateway ]                                                                      |
|  * Webhook Adapter (/api/v1/execute, /api/v1/radio/play)                                          |
|  * CNCF CloudEvents Ingestion (/api/radio/event)                                                  |
|  * n8n Workflow Trigger Interface (Port 5678)                                                     |
|                                                                                                   |
|  [ Core Streaming & DSP Playout Engine ]                                                          |
|  +-----------------------------------+-----------------------------------+                        |
|  | HTTP 206 Partial Content Streamer | Real-Time Web Audio DSP Graph     |                        |
|  | - Chunk Size: 1MB Streaming Buffer| - 64-Band FFT Biquad Analyzer     |                        |
|  | - Formats: MP3, WAV, AIF, M4A, OGG| - Hardware Dual VU Meters (dBFS)  |                        |
|  | - Byte-Range Header Validation    | - Sub-Second -14dB Gain Ducking   |                        |
|  +-----------------------------------+-----------------------------------+                        |
|                                                                                                   |
|  [ Intelligent Broadcast Automation ]                                                             |
|  * Daypart Rotation Engine (Morning / Cyber-Lab / Night / Deep Focus)                             |
|  * AI DJ Script Generator & ElevenLabs/Local TTS Speech Synthesizer                               |
|  * Dynamic Categorized Catalog: Songs (35), Stories (2), Podcasts (2), Commercials (1)             |
|                                                                                                   |
|  [ Persistence Layer: radio_schedule.db ]                                                         |
|  * Tracks Table: File paths, duration, category, energy rating, tags                              |
|  * Play_Log Table: Timestamp, track_id, daypart, listener_count, ducking_events                   |
|                                                                                                   |
+===================================================================================================+
                                  |                     |
          +-----------------------+                     +-----------------------+
          |                                                                     |
          v Audio Feed (HTTP 206)                                               v Sync Signals (ZeroMQ/HTTP)
+------------------------------------+                                +-------------------------------------+
|    CYBER-BROADCAST WEB CONSOLE     |                                |        TV BROADCAST STATION         |
|  - HTML5 / Web Audio API Canvas    |                                |  - Port 8812 (Visual Stage Master)  |
|  - Real-Time Spectrum Visualizer   |                                |  - 16:9 Slide Manifest Timing Sync  |
|  - Neon HUD CRT Scanlines          |                                |  - Dual-Channel Media Simulcast     |
+------------------------------------+                                +-------------------------------------+
```

---

## 3. Cyber-Broadcast Web Console & Web Audio DSP Engine

The station serves a high-performance, single-page web console accessible at `http://127.0.0.1:8811/` or `http://127.0.0.1:8811/radio`. Engineered in vanilla HTML5, CSS Grid, and the W3C Web Audio API, the console operates with zero external JavaScript dependencies and renders at 60 frames per second.

```
+===================================================================================================+
|  [🔴 LIVE] SBB CYBER-BROADCAST CONSOLE 88.11 FM                       SIGNAL: 100% STEREO LOCK    |
+===================================================================================================+
|                                                                                                   |
|   CURRENT TRACK: "Episode 1 Freedom Final Master"                                                 |
|   CATEGORY: Narrative Story / Master Score            DAYPART: Morning Cyber-Drive                |
|                                                                                                   |
|   [SPECTRUM VISUALIZER - 64 BANDS]                                                                |
|   ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  |
|   30Hz                  250Hz                  1kHz                  8kHz                 16kHz   |
|                                                                                                   |
|   [VU METERS]                                                                                     |
|   LEFT  [■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□] -4.2 dBFS                                          |
|   RIGHT [■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□] -4.1 dBFS                                          |
|                                                                                                   |
|   [TRANSPORT]                                                                                     |
|   [ ▶ PLAY ]   [ ⏸ PAUSE ]   [ ⏭ SKIP ]   [ 🎙️ TRIGGER DJ BREAK ]   VOLUME: [========|==] 85%     |
|                                                                                                   |
|   [ACTIVE PLAYLIST: SONGS (35 Tracks)]                                                            |
|   1. 01. lo-fi-beats-13-140-bpm.wav               [3:12] [SONG]      [▶ PLAY NOW]                |
|   2. 02. retro-synth-wave-80s-120-bpm.wav         [4:05] [SONG]      [▶ PLAY NOW]                |
|   3. Project 16.aif                               [2:48] [STORY]     [▶ PLAY NOW]                |
|   4. freedom.aif                                  [1:30] [STORY]     [▶ PLAY NOW]                |
|                                                                                                   |
+===================================================================================================+
```

### 3.1 Web Audio API 64-Band Real-Time Spectrum Visualizer
The audio visualizer is powered by an `AnalyserNode` connected directly to the master `AudioDestinationNode`. It evaluates fast Fourier transforms with a `fftSize` of 128 (yielding 64 discrete frequency bins):

```javascript
// Web Audio API Frequency Analysis Pipeline
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
const audioElement = document.getElementById('radioAudioPlayer');
const sourceNode = audioCtx.createMediaElementSource(audioElement);

const analyserNode = audioCtx.createAnalyser();
analyserNode.fftSize = 128;
analyserNode.smoothingTimeConstant = 0.82;

const gainNode = audioCtx.createGain();

sourceNode.connect(analyserNode);
analyserNode.connect(gainNode);
gainNode.connect(audioCtx.destination);

const bufferLength = analyserNode.frequencyBinCount; // 64 bins
const dataArray = new Uint8Array(bufferLength);

function renderSpectrum() {
  requestAnimationFrame(renderSpectrum);
  analyserNode.getByteFrequencyData(dataArray);

  const canvas = document.getElementById('spectrumCanvas');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const barWidth = (canvas.width / bufferLength) * 0.85;
  let x = 0;

  for (let i = 0; i < bufferLength; i++) {
    const barHeight = (dataArray[i] / 255) * canvas.height;
    
    // Dynamic Cyber-Gradient: Cyan to Neon Purple
    const gradient = ctx.createLinearGradient(0, canvas.height, 0, 0);
    gradient.addColorStop(0, '#00e5ff');
    gradient.addColorStop(0.7, '#8a2be2');
    gradient.addColorStop(1, '#ff007f');

    ctx.fillStyle = gradient;
    ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
    x += barWidth + 2;
  }
}
renderSpectrum();
```

### 3.2 Hardware VU Meters & Peak Level Detection
The console samples RMS (Root Mean Square) audio levels and peak dBFS (decibels relative to full scale) across Left and Right stereo channels. The VU meter components feature ballistic damping mimicking physical analog needle movements, changing from neon green (`< -12 dBFS`) to amber (`-12 to -3 dBFS`) and red clipping indicators (`> -0.1 dBFS`).

### 3.3 Sub-Second -14dB Audio Ducking DSP Curves
When an on-air DJ voice interstitial is cued via `/api/v1/radio/generate-dj`, the Web Audio `gainNode` executes an automated volume reduction curve:

```javascript
// DSP Audio Ducking Implementation
function applyDjDucking(enableDucking, durationSeconds = 5.0) {
  const currentTime = audioCtx.currentTime;
  const currentVolume = gainNode.gain.value;

  if (enableDucking) {
    // Attack Curve: Smoothly attenuate down to -14dB (approx 0.20 linear gain) in 350ms
    gainNode.gain.cancelScheduledValues(currentTime);
    gainNode.gain.setValueAtTime(currentVolume, currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.20, currentTime + 0.35);
    
    console.log('[DSP] Music bed ducked to -14dB for DJ interstitial.');
  } else {
    // Release Curve: Smoothly restore full gain over 800ms
    gainNode.gain.cancelScheduledValues(currentTime);
    gainNode.gain.setValueAtTime(currentVolume, currentTime);
    gainNode.gain.exponentialRampToValueAtTime(1.0, currentTime + 0.80);
    
    console.log('[DSP] Music bed restored to 0dB.');
  }
}
```

---

## 4. Streaming Subsystem: HTTP 206 Partial Content & Byte-Range Requests

To guarantee instantaneous seeking and zero-latency audio playback across desktop browsers and native macOS AVFoundation players, the streaming router implements standard HTTP 206 Partial Content negotiation:

```python
# HTTP 206 Partial Content Implementation in FastAPI
import os
import re
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter()

def parse_byte_range(range_header: str, file_size: int):
    '''Parses standard HTTP Range headers (e.g. 'bytes=0-1048575').'''
    match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    if not match:
        return 0, file_size - 1
    start = int(match.group(1))
    end = int(match.group(2)) if match.group(2) else file_size - 1
    return start, min(end, file_size - 1)

@router.get("/audio/{file_name}")
async def stream_audio_file(file_name: str, request: Request):
    base_dir = "/Users/russellpowers/Sovereign Biz Box/solutions"
    file_path = os.path.join(base_dir, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found.")

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("range")

    if range_header:
        start, end = parse_byte_range(range_header, file_size)
        content_length = (end - start) + 1

        def chunk_generator():
            with open(file_path, "rb") as f:
                f.seek(start)
                bytes_left = content_length
                while bytes_left > 0:
                    read_size = min(bytes_left, 1024 * 1024) # 1MB buffer chunks
                    chunk = f.read(read_size)
                    if not chunk:
                        break
                    bytes_left -= len(chunk)
                    yield chunk

        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            "Content-Type": "audio/x-aiff" if file_name.endswith(('.aif', '.aiff')) else "audio/mpeg",
        }
        return StreamingResponse(chunk_generator(), status_code=206, headers=headers)

    # Fallback to full file streaming if no Range header present
    return StreamingResponse(open(file_path, "rb"), media_type="audio/mpeg")
```

---

## 5. Autonomous AI DJ Synthesis & Daypart Scheduling

### 5.1 Daypart Matrix & Programming Clock
The station divides the 24-hour broadcast cycle into four distinct programming blocks:

| Daypart Name | Hours (Local Time) | Genre & Format | DJ Demeanor & Style | Ducking Depth |
| :--- | :--- | :--- | :--- | :--- |
| **Morning Cyber-Drive** | 06:00 – 12:00 | Upbeat Synthwave, Tech News, Project Standups | High Energy, Motivational, Crisp | -14 dB |
| **Afternoon Cyber-Lab** | 12:00 – 18:00 | Deep Electronic, Lo-Fi House, Architecture Deep Dives | Focused, Analytical, Technical | -12 dB |
| **Night Shift Playout** | 18:00 – 00:00 | Dark Ambient, Narrative Audio Dramas, Cyberpunk Stems | Mysterious, Cinematic, Deliberate | -16 dB |
| **Deep Focus Matrix** | 00:00 – 06:00 | Pure Binaural Beats, Sub-Bass Drones, Zero Vocals | Minimal Speech, Ambient Sweeps | -10 dB |

### 5.2 Dynamic AI DJ Interstitial Generation Engine
When `/api/v1/radio/generate-dj` is invoked, the station generates contextual broadcast banter tailored to the active daypart, current track title, and simulated listener count:

```python
# Dynamic AI DJ Interstitial Synthesis
from pydantic import BaseModel
import random

class DjBreakRequest(BaseModel):
    station_callsign: str = "KSBB-FM"
    current_track: str
    daypart: str = "Morning Cyber-Drive"

def generate_dj_script(req: DjBreakRequest) -> str:
    templates = [
        f"You are locked into {req.station_callsign}, broadcasting live across the sovereign bare-metal network. "
        f"That was '{req.current_track}' setting the pace for this {req.daypart}. "
        f"Up next, we are rolling straight into the deep architecture vault. Keep your terminals open and stay calibrated.",
        
        f"This is KSBB Cyber-Radio. Smooth telemetry and 100 percent signal purity. "
        f"We just heard '{req.current_track}'. Up next, fresh stems from the Save the Cat! Storyboard engine. "
        f"Let the frequencies resonate.",
        
        f"System health nominal, zero packet drops. You are listening to the autonomous voice of Black Fox Studio. "
        f"Coming out of '{req.current_track}', get ready for our next sonic movement."
    ]
    return random.choice(templates)
```

### 5.3 Categorized Track Library Management
The station catalogs all audio assets into distinct broadcast categories:
- **Songs (`SONG`)**: High-fidelity music stems (e.g., 35 curated Lo-Fi, Synthwave, and Instrumental tracks).
- **Stories (`STORY`)**: Episodic narrative voice dramas and soundtrack mixes (e.g., `Project 16.aif`, `freedom.aif`).
- **Podcasts (`PODCAST`)**: Long-form interviews, architectural podcasts, and technical tutorials.
- **Commercials (`COMMERCIAL`)**: Station identification jingles, SBB sponsor messages, and audio teasers.

### 5.4 Track Catalog Specifications & Musical Key Alignment
To prevent jarring harmonic clashes during automated crossfading, tracks in the station's library are cataloged with harmonic Camelot keys, tempos (BPM), and loudness targets (-14 LUFS):

| Track Title | File Identifier | Category | BPM | Key / Mode | Target Daypart |
| :--- | :--- | :--- | :-: | :---: | :--- |
| **01. Lo-Fi Beats 13** | `01. lo-fi-beats-13-140-bpm.wav` | `SONG` | 140 | 8A (A Minor) | Morning Cyber-Drive |
| **02. Retro Synthwave 80s** | `02. retro-synth-wave-80s-120-bpm.wav`| `SONG` | 120 | 4A (F Minor) | Afternoon Cyber-Lab |
| **03. Deep Chillhop Groove** | `03. deep-chillhop-groove-95-bpm.wav`| `SONG` | 95 | 11B (A Major) | Deep Focus Matrix |
| **04. Cyberpunk Drive Master** | `04. cyberpunk-drive-130-bpm.wav` | `SONG` | 130 | 5A (C Minor) | Night Shift Playout |
| **Episode 1: Freedom Master**| `freedom.aif` | `STORY` | 85 | 10A (B Minor) | Prime Time Special |
| **Episode 1: Final Orchestral**| `Project 16.aif` | `STORY` | 88 | 10A (B Minor) | Prime Time Special |
| **SBB Autonomous Jingle** | `commercial_sbb_ident_01.mp3` | `COMMERCIAL`| 120 | 12B (E Major) | Top-of-Hour Ident |

---

## 6. SQLite Persistence Layer (`radio_schedule.db`)


All track metadata, daypart schedules, play logs, and DJ voice events are persisted inside `.n8n/radio_schedule.db`:

```sql
-- Track Registry Table
CREATE TABLE IF NOT EXISTS tracks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    category TEXT CHECK(category IN ('SONG', 'STORY', 'PODCAST', 'COMMERCIAL')),
    duration_seconds REAL NOT NULL,
    bpm INTEGER,
    energy_level INTEGER CHECK(energy_level BETWEEN 1 AND 10),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Historical Playout Log Table
CREATE TABLE IF NOT EXISTS play_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id TEXT NOT NULL,
    track_title TEXT NOT NULL,
    played_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    daypart TEXT NOT NULL,
    listener_count INTEGER DEFAULT 142,
    ducking_applied BOOLEAN DEFAULT 0,
    FOREIGN KEY(track_id) REFERENCES tracks(id)
);

-- Indices for Fast Schedule Lookups
CREATE INDEX IF NOT EXISTS idx_tracks_category ON tracks(category);
CREATE INDEX IF NOT EXISTS idx_play_log_time ON play_log(played_at DESC);
```

---

## 7. Cross-Station Media Simulcast with TV Broadcast Station (`:8812`)

The AI Radio Station coordinates with the **TV Broadcast Station** (`:8812`) via the SBB Autonomous Command Center (`:5678`):
1. **Master Audio Source**: The radio station serves as the primary audio carrier for television stage visuals.
2. **Timecode Broadcast**: When an episodic narrative track plays (e.g., `Project 16.aif`), the radio station emits a CloudEvent (`radio.playout.started`).
3. **Stage Visual Synchronization**: The TV Broadcast Station ingests the event and cues corresponding visual slides matching the narration beats.

### 7.1 Cross-Station Webhook Handshake Payload
```json
{
  "event": "radio.simulcast.cue",
  "track_id": "track-ep01-final",
  "track_title": "Project 16.aif",
  "audio_stream_url": "http://127.0.0.1:8811/audio/Project%2016.aif",
  "duration_seconds": 168.4,
  "timecode_offsets": [
    { "slide_index": 1, "offset_seconds": 0.0, "beat": "Opening Image" },
    { "slide_index": 2, "offset_seconds": 12.4, "beat": "Theme Stated" },
    { "slide_index": 3, "offset_seconds": 24.8, "beat": "Set-Up" },
    { "slide_index": 4, "offset_seconds": 38.2, "beat": "Catalyst" },
    { "slide_index": 5, "offset_seconds": 51.0, "beat": "Debate" }
  ],
  "ducking_profile": {
    "enabled": true,
    "depth_db": -14.0,
    "attack_ms": 350,
    "release_ms": 800
  }
}
```

---


## 8. Comprehensive REST API Reference

| Method | Route | Description | Request Body / Parameters | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` or `/radio` | Serves Cyber-Broadcast Web Console UI | None | `200 text/html` |
| `GET` | `/health` | Heartbeat & service readiness probe | None | `200 application/json` |
| `GET` | `/audio/{file_name}` | High-fidelity byte-range streaming | Header: `Range: bytes=0-...` | `206 Partial Content` |
| `GET` | `/api/v1/radio/tracks` | Full catalog of categorized tracks | Query: `?category=SONG` | `200 application/json` |
| `GET` | `/api/v1/radio/now-playing` | Active track, daypart & listeners | None | `200 application/json` |
| `POST`| `/api/v1/radio/play` | Changes active track & logs playout | `{"file_path": "...", "title": "..."}` | `200 application/json` |
| `POST`| `/api/v1/radio/generate-dj` | Synthesizes AI DJ voice break script | `{"current_track": "...", "daypart": "..."}` | `200 application/json` |
| `POST`| `/api/v1/execute` | Universal n8n / desktop app webhook | `{"action": "play_track", ...}` | `200 application/json` |

---

## 9. n8n Automation & Custom Community Node (`SovereignAiRadioStation`)

The station provides seamless drag-and-drop integration inside the SBB Autonomous Command Center through the compiled community node **`SovereignAiRadioStation`**:

```typescript
// SovereignAiRadioStation INodeType Definition Extract
export class SovereignAiRadioStation implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Sovereign AI Radio Station',
    name: 'sovereignAiRadioStation',
    icon: 'file:radio.svg',
    group: ['transform'],
    version: 1,
    description: 'Control autonomous 24/7 AI Radio playout, ducking DSP, and AI DJ breaks',
    defaults: { name: 'AI Radio Station' },
    inputs: ['main'],
    outputs: ['main'],
    properties: [
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        options: [
          { name: 'Get Station Health', value: 'getHealth' },
          { name: 'Get Now Playing', value: 'getNowPlaying' },
          { name: 'List Tracks', value: 'listTracks' },
          { name: 'Play Track', value: 'playTrack' },
          { name: 'Generate DJ Break', value: 'generateDj' }
        ],
        default: 'getNowPlaying'
      }
    ]
  };
}
```

---

## 10. SRE Runbook, Telemetry & Disaster Recovery

### 10.1 Starting the Station Daemon
```bash
cd "/Users/russellpowers/Sovereign Biz Box/solutions/ai-radio-station"
python3 n8n/webhook_adapter.py
```

### 10.2 Verifying Server Availability
```bash
curl -i http://127.0.0.1:8811/health
```
Expected output:
```json
{
  "status": "healthy",
  "service": "sovereign-ai-radio-station",
  "port": 8811,
  "current_daypart": "Morning Cyber-Drive",
  "listeners": 142
}
```

### 10.3 Inspecting Active Process
```bash
lsof -i tcp:8811
```

---

## 11. Verification Suite & Automated Unit Tests

To run the automated station test suite:
```bash
pytest tests/ -v
```

Tests validate:
- Range header parsing and byte calculations
- Zero-trust token enforcement (`X-SBB-Auth`)
- Web Audio console UI template rendering
- SQLite transaction logging

---

## 12. Authors, Governance & MIT License

The **Sovereign AI Radio Station** is engineered and governed by **Russell Alan Powers** and **Black Fox Gaming Studio**.

- **Lead Broadcast Engineer**: Russell Alan Powers (<russell@blackfoxgaming.com>)
- **Organization**: Black Fox Gaming Studio
- **Ecosystem**: Sovereign Biz Box (SBB) Bare-Metal Infrastructure
- **License**: Released under the terms of the **MIT License**.

```
MIT License

Copyright (c) 2026 Black Fox Gaming Studio & Russell Powers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
