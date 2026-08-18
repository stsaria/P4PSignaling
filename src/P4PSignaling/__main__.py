import asyncio

from P4PSignaling.P4PSignaling import P4PSignaling

async def amain() -> None:
    print("Start")
    signaling = await P4PSignaling.create()
    try:
        await signaling.begin()

        while True:
            await asyncio.sleep(0.1)
    except asyncio.exceptions.CancelledError:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        print("End")
        await signaling.end()

if __name__ == "__main__":
    asyncio.run(amain())