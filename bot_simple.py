"""Совместимая точка запуска; основная реализация находится в main.py."""
import asyncio

from main import main


if __name__ == "__main__":
    asyncio.run(main())
