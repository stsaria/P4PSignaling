# P4PSignaling
A signaling server for P4P (Peer-to-Peer) applications, providing secure and efficient communication between peers. This project is designed to facilitate the discovery and connection of peers in a decentralized network.
## Getting Started
Basically, you should use isolated environment to run P4PSignaling. You can use `venv` or `conda` to create an isolated environment. Here is an example using `venv`:
```bash
mkdir p4psignaling
cd p4psignaling

python3 -m venv .venv
source .venv/bin/activate

curl -sSL https://raw.githubusercontent.com/stsaria/p4p/main/install.sh | bash

python3 -m P4PSignaling
```
But, you can't run P4PSignaling with alpha version.