import os
import asyncio
import pytest

from P4PCore.model.Ed25519Signer import Ed25519Signer
from P4PCore.model.NodeIdentify import NodeIdentify
from P4PCore.model.HashableEd25519PublicKey import HashableEd25519PublicKey

from P4PNodeGossiper.util.NodeIdentifyConverter import nodeIdentifyToBytes

from P4PSignaling.Config import Config
from P4PSignaling.P4PSignaling import P4PSignaling


def _makeNode(port: int, ip: str = "127.0.0.1") -> NodeIdentify:
    return NodeIdentify(
        ip=ip,
        port=port,
        hashableEd25519PublicKey=HashableEd25519PublicKey(os.urandom(32)),
    )


async def _createSignaling(monkeypatch: pytest.MonkeyPatch, port: int) -> P4PSignaling:
    monkeypatch.setattr(Config, "BIND_IPV4", "127.0.0.1")
    monkeypatch.setattr(Config, "BIND_PORT", port)
    return await P4PSignaling.create()


class TestP4PSignaling:
    @pytest.mark.asyncio
    async def testCreateUsesConfiguredEd25519Key(self, monkeypatch):
        signaling = await _createSignaling(monkeypatch, port=18801)

        expectedPublicKeyBytes = Ed25519Signer(
            bytes.fromhex(Config.ED25519_PRIVATE_KEY_HEX)
        ).publicKey.publicKeyBytes
        assert signaling._runner.ed25519Signer.publicKey.publicKeyBytes == expectedPublicKeyBytes

        await signaling.end()

    @pytest.mark.asyncio
    async def testCreatePassesConfigIntoNodeGossiper(self, monkeypatch):
        signaling = await _createSignaling(monkeypatch, port=18802)

        gossiper = signaling._nodeGossiper._gossiper
        assert gossiper._gossipTTLSeconds == Config.GOSSIP_TTL_SECONDS
        assert gossiper._syncPeerCountPerOneTime == Config.SYNC_PEER_COUNT_PER_ONE_TIME
        assert gossiper._syncIntervalSeconds == Config.SYNC_INTERVAL_SECOUNDS
        assert gossiper._maximumSavedDataCount == Config.MAXIMUM_NODES_COUNT

        await signaling.end()

    @pytest.mark.asyncio
    async def testBeginEndLifecycleDoesNotRaise(self, monkeypatch):
        signaling = await _createSignaling(monkeypatch, port=18803)

        await signaling.begin()
        await asyncio.sleep(0)
        await signaling.end()

    @pytest.mark.asyncio
    async def testTwoSignalingServersCanGossipNodesToEachOther(self, monkeypatch):
        signalingA = await _createSignaling(monkeypatch, port=18804)
        await signalingA.begin()

        signalingB = await _createSignaling(monkeypatch, port=18805)
        await signalingB.begin()

        await asyncio.sleep(0)

        node = _makeNode(port=39999)
        await signalingB._nodeGossiper.addNode(node)

        signalingB._nodeGossiper._gossiper._gossip(
            ("127.0.0.1", 18804),
            nodeIdentifyToBytes(node)
        )

        await asyncio.sleep(0.1)

        assert node in await signalingA._nodeGossiper.getNodeIdentifies()

        await signalingA.end()
        await signalingB.end()
