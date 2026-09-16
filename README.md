# Sovereign AI Radio Station (`sovereign-ai-radio-station`)

[![Port](https://img.shields.io/badge/Port-8811-blue.svg)](n8n/webhook_adapter.py)
[![Architecture](https://img.shields.io/badge/Tier-1_Production_Ready-brightgreen.svg)](ROADMAP.md)
[![Status](https://img.shields.io/badge/Status-HEALTHY-success.svg)](http://127.0.0.1:8811/health)

Autonomous 24/7 audio broadcast and radio station microservice. Generates dynamic AI DJ voice synthesis, mixes real-time background audio ducking curves, schedules programming blocks via SQLite, and synchronizes live broadcast audio with TV stage playout.

---

## 📻 Core Capabilities

1. **Continuous Lo-Fi & Deep Build Playout Engine**:
   - 24/7 autonomous background music streaming with zero listener dropouts.
   - Dynamic track scheduling and metadata broadcasting.

2. **Automated DJ Voice & Ducking DSP**:
   - Sub-second volume ducking curves automatically lower music levels during station voice announcements and ident drops.
   - Smooth crossfading transitions between program blocks.

3. **Multi-Station Simulcast Sync**:
   - Synchronizes audio feed with the TV Broadcast Station (`:8812`) for dual-channel television and radio simulcasts.

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Returns station health, current show title, port, and uptime. |
| `POST` | `/api/v1/execute` | Standard n8n microservice execution endpoint (track cueing, schedule queries). |

---

## ⚡ n8n Microservice Integration

- **Webhook Adapter (`solutions/ai-radio-station/n8n/webhook_adapter.py`)**:
  - Listens on port `8811`.
  - Exposes health probes and automation webhook triggers.
- **Workflow Template (`solutions/ai-radio-station/n8n/workflow.json`)**:
  - Automated radio broadcast status and health trigger workflow.
- **Custom n8n Node (`SovereignAiRadioStation`)**:
  - Registered in `sbb-n8n-command-center/custom-nodes`.
  - Enables visual n8n workflows to query station health, cue tracks, and synchronize audio streams.

---

## 🛠️ Playout Server Command

```bash
cd solutions/ai-radio-station
python3 n8n/webhook_adapter.py
```

