import os
from dataclasses import asdict, dataclass
from dotenv import load_dotenv

from P4PCore.common.model.Ed25519Signer import Ed25519Signer

DOTENV_PATH = ".env"
load_dotenv(DOTENV_PATH)

@dataclass(frozen=True)
class Config:
    BIND_IPV4:str = os.getenv("BIND_IPV4", "0.0.0.0")
    BIND_PORT:int = int(os.getenv("BIND_PORT", "15987"))
    ED25519_PRIVATE_KEY_HEX:str = os.getenv("ED25519_PRIVATE_KEY_HEX", Ed25519Signer()._privateKey.private_bytes_raw().hex())
    GOSSIP_TTL_SECONDS:float = float(os.getenv("GOSSIP_TTL_SECONDS", "5"))
    SYNC_NODE_COUNT_PER_ONE_TIME:int = int(os.getenv("SYNC_NODE_COUNT_PER_ONE_TIME", "10"))
    SYNC_INTERVAL_SECONDS:float = float(os.getenv("SYNC_INTERVAL_SECONDS", "5"))
    MAXIMUM_NODES_COUNT:int = int(os.getenv("MAXIMUM_NODES_COUNT", "100"))
    DISABLE_SECURE_TRANSPORT:bool = os.getenv("DISABLE_SECURE_TRANSPORT", "true").lower() in ("true", "1", "t")
    MINIMUM_NODES_COUNT:int = int(os.getenv("MINIMUM_NODES_COUNT", "20"))
    MAGIC_STR:str = os.getenv("MAGIC", "P4P6")
    NET_SEMAPHORE_LIMITS:int = int(os.getenv("NET_SEMAPHORE_LIMITS", "500"))
    def save(self):
        data = asdict(self)
        with open(DOTENV_PATH, "w", encoding="utf-8") as f:
            for key, value in data.items():
                f.write(f"{key.upper()}={value}\n")

Config().save()