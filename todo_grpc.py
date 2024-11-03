import logging
from services.todo import run
import asyncio
from settings import TODO_GRPC_SERVER_ADDR

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    logging.info("Starting gRPC server...")
    try:
        asyncio.run(run(TODO_GRPC_SERVER_ADDR))
    except Exception as e:
        logging.error("Failed to start gRPC server: %s", e)
