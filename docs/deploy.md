# Deploy LiveKit Cloud

Projekt: `aai` / `aai-j4shxmol.livekit.cloud`  
Region: **eu-central** (immutable nach create)

Aktuell:

| ID | Name |
|---|---|
| `CA_J8AZ7K6yJ5o3` | `amina-soniox-v2` |

Config: `livekit.eu-central.toml`

```bash
lk agent deploy --project aai --config livekit.eu-central.toml
```

Dockerfile `CMD` = `python -m amina.agent_soniox_v2 start`.  
Anderen Agenten deployen = **neuen** `lk agent create` + eigene toml, nicht diese CMD umbiegen ohne Freigabe.

Secrets: `lk agent update --secrets-file=.env.local` (Datei nicht committen).
