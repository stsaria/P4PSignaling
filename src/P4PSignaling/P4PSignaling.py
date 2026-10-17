import importlib.metadata
import logging
import sys

from P4PCore.P4PRunner import P4PRunner
from P4PCore.common.model.Ed25519Signer import Ed25519Signer
from P4PCore.common.util.BytesCoverter import itob
from P4PCore.core.protocol.Protocol import PacketFlag, PacketElementSize, STR_ENCODING

from P4PCore.plugin.append.nodeGossiper.NodeGossiper import NodeGossiper

from P4PSignaling.Config import Config

class P4PSignaling:
    _runner:P4PRunner
    _nodeGossiper:NodeGossiper
    _logger:logging.Logger
    @classmethod
    async def create(cls) -> "P4PSignaling":
        inst = cls()

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )

        inst._runner = P4PRunner(
            ed25519Signer=Ed25519Signer(bytes.fromhex(Config.ED25519_PRIVATE_KEY_HEX)),
            magic=Config.MAGIC_STR.encode(encoding=STR_ENCODING),
            loggerHandlers=[handler],
            netV4ListeningAddr=(Config.BIND_IPV4, Config.BIND_PORT)
        )

        inst._runner.net.semaphoreLimits = Config.NET_SEMAPHORE_LIMITS

        if Config.DISABLE_SECURE_TRANSPORT:
            inst._runner.baseUserNet.deleteHandler(itob(PacketFlag.SECURE, PacketElementSize.PACKET_FLAG))

        inst._nodeGossiper = NodeGossiper(
            inst._runner,
            gossipTTLSeconds=Config.GOSSIP_TTL_SECONDS,
            syncNodeCountPerOneTime=Config.SYNC_NODE_COUNT_PER_ONE_TIME,
            syncIntervalSeconds=Config.SYNC_INTERVAL_SECONDS,
            maximumNodesCount=Config.MAXIMUM_NODES_COUNT,
            minimumNodesCount=Config.MINIMUM_NODES_COUNT
        )

        inst._logger = inst._runner.getLogger(__name__)

        return inst

    async def begin(self) -> None:
        self._logger.info(f"""Begin to a P4PSignaling server\n
Version: {importlib.metadata.version('P4PSignaling')}
BindV4:{(Config.BIND_IPV4, Config.BIND_PORT)}
Ed25519 Public key hex:{self._runner.ed25519Signer.publicKey.publicKeyBytes.hex()}""")
        await self._runner.begin()

    async def end(self) -> None:
        await self._runner.end()


