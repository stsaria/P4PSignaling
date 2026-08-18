import os
from dataclasses import asdict, dataclass
from dotenv import load_dotenv

from P4PCore.model.Ed25519Signer import Ed25519Signer

DOTENV_PATH = ".env"
load_dotenv(DOTENV_PATH)

@dataclass(frozen=True)
class Config:
    BIND_IPV4:str = os.getenv("BIND_IPV4", "0.0.0.0")
    BIND_PORT:int = int(os.getenv("BIND_PORT", "15987"))
    ED25519_PRIVATE_KEY_HEX:str = os.getenv("ED25519_PRIVATE_KEY_HEX", Ed25519Signer()._privateKey.private_bytes_raw().hex())
    GOSSIP_TTL_SECONDS:int = int(os.getenv("GOSSIP_TTL_SECONDS", "5"))
    SYNC_PEER_COUNT_PER_ONE_TIME:int = int(os.getenv("SYNC_PEER_COUNT_PER_ONE_TIME", "10"))
    SYNC_INTERVAL_SECOUNDS:int = int(os.getenv("SYNC_INTERVAL_SECOUNDS", "5"))
    MAXIMUM_NODES_COUNT:int = int(os.getenv("MAXIMUM_NODES_COUN", "100"))
    def save(self):
        data = asdict(self)
        with open(DOTENV_PATH, "w", encoding="utf-8") as f:
            for key, value in data.items():
                f.write(f"{key.upper()}={value}\n")

Config().save()