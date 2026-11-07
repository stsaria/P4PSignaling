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
- macOS Intel: `P4PSignaling-macos-x86_64`
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