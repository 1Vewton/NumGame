from typing import List, Dict
from logging import getLogger
# Asyncio
from threading import Lock
import asyncio
# Fastapi Dependencies
from fastapi import WebSocket
# Project dependencies
from utils.utils import generate_uuid

logger = getLogger("PVP")


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
            public: bool,
    ):
        self.room_id: str = room_id
        self.connections: List[Connection] = []
        self.public: bool = public
        # lock the connections list
        self.lock: Lock = Lock()

    # Delete
    def __del__(self) -> None:
        logger.info(f"Room {self.room_id} deleted")
        try:
            for connection in self.connections:
                asyncio.run(connection.client.close())
        except Exception as e:
            logger.error(e)

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
                logger.error(f"Room {self.room_id} fulled")
                raise Exception(f"Room {self.room_id} fulled")

    # Disconnect
    async def disconnect(
            self,
            user_id: str,
    ) -> None:
        with self.lock:
            for connection in self.connections:
                if connection.user_id == user_id:
                    self.connections.remove(connection)
                    logger.info(f"{user_id} disconnected from room {self.room_id}")

    # Broadcast
    async def broadcast(
            self,
            data: dict,
    ) -> None:
        for connection in self.connections:
            await connection.client.send_json(data)

    # Send to certain user
    async def send(
            self,
            user_id: str,
            data: dict,
    ) -> None:
        for connection in self.connections:
            if connection.user_id == user_id:
                await connection.client.send_json(data)
                return None
        raise Exception(f"No such user connected to room {self.room_id}")

    # Turn the data of the room to dict
    def to_dict(self) -> dict:
        players = []
        for connection in self.connections:
            players.append(connection.user_id)
        return {
            "room_id": self.room_id,
            "public": self.public,
            "player_ids": players,
        }


# Connection Manager
class ConnectionManager:
    def __init__(
            self,
    ):
        self.rooms: Dict[str, Room] = {}

    # Room id
    async def new_room(self, public: bool) -> str:
        room_id = generate_uuid()
        self.rooms[room_id] = Room(
            room_id=room_id,
            public=public,
        )
        return room_id
