from typing import List
from threading import Lock
# Fastapi Dependencies
from fastapi import WebSocket
# Redis
import redis.asyncio as aioredis


# Connections
class Connection:
    def __init__(
            self,
            client: WebSocket,
            user_id: str,
    ):
        self.client: WebSocket = client
        self.user_id: str = user_id


# Rooms
class Room:
    def __init__(
            self,
            room_id: str,
            redis_client: aioredis.Redis,
    ):
        self.room_id: str = room_id
        self.connections: List[Connection] = []
        # lock the connections list
        self.lock: Lock = Lock()
        self.redis: aioredis.Redis = redis_client

    # Connect to the room
    async def connect(
            self,
            user_id: str,
            connection: WebSocket,
    ) -> None:
        await connection.accept()
        new_connection = Connection(
            client=connection,
            user_id=user_id,
        )
        with self.lock:
            if len(self.connections) < 2:
                self.connections.append(new_connection)
            else:
                raise Exception("Room fulled")

    # Disconnect
    async def disconnect(
            self,
            user_id: str,
    ) -> None:
        with self.lock:
            for connection in self.connections:
                if connection.user_id == user_id:
                    self.connections.remove(connection)
