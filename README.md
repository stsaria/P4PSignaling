# P4PSignaling

A signaling server for P4P (Peer-to-Peer) applications, providing secure and
efficient communication between peers. This project is designed to facilitate
the discovery and connection of peers in a decentralized network.

## Run a release binary

The recommended way to run P4PSignaling is to download the binary for your
operating system and CPU architecture from the
[latest release](https://github.com/stsaria/P4PSignaling/releases/latest).

- Linux x86_64: `P4PSignaling-linux-x86_64`
- Windows x86_64: `P4PSignaling-windows-x86_64.exe`
- macOS Apple Silicon: `P4PSignaling-macos-arm64`

On Linux and macOS, make the file executable once and run it:

```bash
chmod +x P4PSignaling-linux-x86_64
./P4PSignaling-linux-x86_64
```

Use the corresponding macOS filename on macOS. On Windows, run
`P4PSignaling-windows-x86_64.exe` from PowerShell or Command Prompt.
Configuration uses the same environment variables as the Python package. A
`.env` file can also be placed next to the executable.

## Run with Docker and Kubernetes

On each version tag, CI builds and publishes the image to
`ghcr.io/stsaria/p4psignaling:<tag>`. Stable releases are also published as
`ghcr.io/stsaria/p4psignaling:latest`. To build an image locally:

```bash
docker build -t p4psignaling:local .
```

To run it locally with Docker Compose:

```bash
cp .env.example .env
printf 'ED25519_PRIVATE_KEY_HEX=%s\n' "$(openssl rand -hex 32)" >> .env
docker compose up --build
```

The Compose configuration publishes UDP port `15987` and loads configuration
from `.env`. Keep the private key unchanged across restarts to preserve the
server identity.

Before deploying, create the `p4psignaling` Kubernetes Secret with a
64-character hexadecimal Ed25519 private key as `ED25519_PRIVATE_KEY_HEX`.
Use a secret manager for production, and keep the same key across pod restarts
to preserve the server identity. For a local setup, generate a key in a
temporary file and create the Secret:

```bash
key_file="$(mktemp)"
trap 'rm -f "$key_file"' EXIT
openssl rand -hex 32 > "$key_file"
kubectl create secret generic p4psignaling \
  --from-file=ED25519_PRIVATE_KEY_HEX="$key_file"
```

Then deploy the single-replica workload and UDP LoadBalancer Service:

```bash
kubectl apply -f deploy/k8s.yaml
kubectl get service p4psignaling
kubectl logs deployment/p4psignaling
```

The cluster must support UDP LoadBalancer services, and UDP port `15987` must
be reachable by peers. The manifest uses the `latest` image tag; pin the
Deployment to a version tag for controlled upgrades. CI publishes images but
does not deploy to a cluster; automatic deployment requires cluster-specific
credentials and configuration.

## Run from Python

The release binary is recommended for normal use. To run the package with
Python without using `install.sh`, clone the repository and install it in a
virtual environment:

```bash
git clone https://github.com/stsaria/P4PSignaling.git
cd P4PSignaling
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install git+https://github.com/stsaria/P4PCore.git@d
python -m pip install .
python3 -m P4PSignaling
```