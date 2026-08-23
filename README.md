# P4PSignaling

A signaling server for the P4P network. Nodes exchange information over a UDP-based gossip protocol.

## Requirements

- Docker
- Docker Compose

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/stsaria/P4PSignaling.git
cd P4PSignaling
```

### 2. Configure environment variables

Create a `.env` file in the repository root. All variables are optional; any not set will fall back to the defaults below.

| Variable | Description | Default |
| --- | --- | --- |
| `BIND_IPV4` | IPv4 address to listen on | `0.0.0.0` |
| `BIND_PORT` | UDP port to listen on | `15987` |
| `ED25519_PRIVATE_KEY_HEX` | Ed25519 private key (hex) used as the node identity | generated automatically if unset |
| `GOSSIP_TTL_SECONDS` | TTL for gossiped info, in seconds | `5` |
| `SYNC_PEER_COUNT_PER_ONE_TIME` | Number of peers picked per sync | `10` |
| `SYNC_INTERVAL_SECOUNDS` | Sync interval, in seconds | `5` |
| `MAXIMUM_NODES_COUNT` | Maximum number of nodes to keep track of | `100` |

Leave `ED25519_PRIVATE_KEY_HEX` unset for a first run — a key will be generated and written back to `.env` automatically. Keep it afterwards to preserve the node's identity across restarts.

## Run

```bash
docker compose up -d --build
```

- The UDP port `15987` (or your custom `BIND_PORT`) is exposed.
- `.env` is mounted into the container at `/app/.env`, so it must exist in the repository root before starting.