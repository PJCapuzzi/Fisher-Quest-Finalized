import asyncio

from src.game import Game


async def main() -> None:
    game = Game()
    await game.run_async()


if __name__ == "__main__":
    asyncio.run(main())
