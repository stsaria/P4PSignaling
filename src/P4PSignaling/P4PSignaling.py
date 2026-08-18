import logging
import sys

from P4PCore.P4PRunner import P4PRunner
from P4PCore.model.Ed25519Signer import Ed25519Signer

from P4PNodeGossiper.NodeGossiper import NodeGossiper

from P4PSignaling.Config import Config

class P4PSignaling:
    _runner:P4PRunner
    _nodeGossiper:NodeGossiper
    _logger:logging.Logger
    @classmethod
    async def create(cls) -> "P4PSignaling":
        inst = cls()

        inst._runner = await P4PRunner.create(Ed25519Signer(bytes.fromhex(Config.ED25519_PRIVATE_KEY_HEX)))

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
            syncPeerCountPerOneTime=Config.SYNC_PEER_COUNT_PER_ONE_TIME,
            syncIntervalSeconds=Config.SYNC_INTERVAL_SECOUNDS,
            maximumNodesCount=Config.MAXIMUM_NODES_COUNT
        )

        inst._logger = await inst._runner.getLogger("P4PSignaling")

        inst._runner.net.v4ListeningAddr = (Config.BIND_IPV4, Config.BIND_PORT)

        return inst

    async def begin(self) -> None:
        self._logger.info(f"""Begin to a P4PSignaling server
BindV4:{self._runner.net.v4ListeningAddr}
Ed25519 Public key hex:{self._runner.ed25519Signer.publicKey.publicKeyBytes.hex()}""")
        await self._runner.begin()
        await self._nodeGossiper.begin()

    async def end(self) -> None:
        await self._nodeGossiper.end()
        await self._runner.end()


