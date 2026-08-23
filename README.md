# P4PSignaling

A signaling server for the P4P network. Nodes exchange information over a UDP-based gossip protocol.

## Requirements

- Docker
- Docker Compose

## Setup

1. Go to the [Releases page](https://github.com/stsaria/P4PSignaling/releases) and download the `docker-compose.yml` asset from the version you want to run.
2. Place it in an empty directory.
3. In the same directory, create a `.env` file. All variables are optional; any not set will fall back to the defaults below.

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
docker compose up -d
```

- The image is pulled automatically from `ghcr.io/stsaria/p4psignaling`.
- The UDP port `15987` (or your custom `BIND_PORT`) is exposed.