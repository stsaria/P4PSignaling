import importlib.metadata
import logging
import sys

from P4PCore.P4PRunner import P4PRunner
from P4PCore.model.Ed25519Signer import Ed25519Signer
from P4PCore.util.BytesCoverter import itob
from P4PCore.protocol.Protocol import PacketFlag, PacketElementSize

from P4PNodeGossiper.NodeGossiper import EventListener, NodeGossipRecvedEvent, NodeGossiper

from P4PSignaling.Config import Config

class P4PSignaling:
    _runner:P4PRunner
    _nodeGossiper:NodeGossiper
    _logger:logging.Logger
    @classmethod
    async def create(cls) -> "P4PSignaling":
        inst = cls()

        inst._runner = await P4PRunner.create(Ed25519Signer(bytes.fromhex(Config.ED25519_PRIVATE_KEY_HEX)))

        if Config.DISABLE_SECURE_TRANSPORT:
            await inst._runner.baseUserNet.deleteHandler(itob(PacketFlag.SECURE, PacketElementSize.PACKET_FLAG))

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )
        await inst._runner.loggerHandlersManager.insertNext(handler)

        inst._nodeGossiper = await NodeGossiper.create(
            inst._runner,
            gossipTTLSeconds=Config.GOSSIP_TTL_SECONDS,
            syncNodeCountPerOneTime=Config.SYNC_NODE_COUNT_PER_ONE_TIME,
            syncIntervalSeconds=Config.SYNC_INTERVAL_SECONDS,
            maximumNodesCount=Config.MAXIMUM_NODES_COUNT
        )

        inst._logger = await inst._runner.getLogger("P4PSignaling")

        inst._runner.net.v4ListeningAddr = (Config.BIND_IPV4, Config.BIND_PORT)

        return inst

    async def begin(self) -> None:
        self._logger.info(f"""Begin to a P4PSignaling server\n
Version: {importlib.metadata.version('P4PSignaling')}
BindV4:{self._runner.net.v4ListeningAddr}
Ed25519 Public key hex:{self._runner.ed25519Signer.publicKey.publicKeyBytes.hex()}""")
        await self._runner.begin()

    async def end(self) -> None:
        await self._runner.end()


