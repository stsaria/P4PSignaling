import importlib.metadata
import logging
from logging import Logger
import sys

from P4PCore.P4PRunner import P4PRunner
from P4PCore.common.model.Ed25519Signer import Ed25519Signer
from P4PCore.common.util.BytesCoverter import itob
from P4PCore.core.protocol.Protocol import PacketFlag, PacketElementSize, STR_ENCODING

from P4PCore.plugin.append.nodeGossiper.NodeGossiper import NodeGossiper

from P4PSignaling.Config import Config

class P4PSignaling:
    def __init__(self):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )

        self._runner:P4PRunner = P4PRunner(
            ed25519Signer=Ed25519Signer(bytes.fromhex(Config.ED25519_PRIVATE_KEY_HEX)),
            magic=Config.MAGIC_STR.encode(encoding=STR_ENCODING),
            loggerHandlers=[handler],
            netV4ListeningAddr=(Config.BIND_IPV4, Config.BIND_PORT)
        )

        self._runner.net.semaphoreLimits = Config.NET_SEMAPHORE_LIMITS

        if Config.DISABLE_SECURE_TRANSPORT:
            self._runner.baseUserNet.deleteHandler(itob(PacketFlag.SECURE, PacketElementSize.PACKET_FLAG))

        self._nodeGossiper:NodeGossiper = NodeGossiper(
            self._runner,
            gossipTTLSeconds=Config.GOSSIP_TTL_SECONDS,
            syncNodeCountPerOneTime=Config.SYNC_NODE_COUNT_PER_ONE_TIME,
            syncIntervalSeconds=Config.SYNC_INTERVAL_SECONDS,
            maximumNodesCount=Config.MAXIMUM_NODES_COUNT,
            minimumNodesCount=Config.MINIMUM_NODES_COUNT
        )

        self._logger:Logger = self._runner.getLogger(__name__)

    async def begin(self) -> None:
        self._logger.info(f"""Begin to a P4PSignaling server\n
Version: {importlib.metadata.version('P4PSignaling')}
BindV4:{(Config.BIND_IPV4, Config.BIND_PORT)}
Ed25519 Public key hex:{self._runner.ed25519Signer.publicKey.publicKeyBytes.hex()}""")
        await self._runner.begin()
        await self._nodeGossiper.begin()

    async def end(self) -> None:
        await self._nodeGossiper.end()
        await self._runner.end()


