import socket
import pickle
import time
from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional


@dataclass
class PlayerState:
    x: int
    y: int
    health: int
    animation_index: int
    animation_frame: int
    attacking: bool
    attack_type: int
    jump: bool
    flip: bool
    run: bool
    timestamp: float = field(default_factory=time.time)


class NetworkClient:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.player_id = None
        self.connected = False

    def connect(self) -> bool:
        try:
            self.client.connect(self.addr)
            self.player_id = int(self.client.recv(4096).decode())
            self.connected = True
            print(f"Connected as player {self.player_id}")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            self.connected = False
            return False

    def send(self, data: Dict) -> Optional[Dict]:
        if not self.connected:
            print("Not connected to the server.")
            return None

        try:
            # Serialize and send the data
            serialized_data = pickle.dumps(data)
            data_length = len(serialized_data)
            self.client.sendall(data_length.to_bytes(4, byteorder='big') + serialized_data)

            # Receive the response length first
            response_length = int.from_bytes(self.client.recv(4), byteorder='big')
            response_data = b""
            while len(response_data) < response_length:
                packet = self.client.recv(4096)
                if not packet:
                    raise ConnectionError("Connection lost while receiving data.")
                response_data += packet

            return pickle.loads(response_data)

        except (socket.error, pickle.PickleError) as e:
            print(f"Network or serialization error: {e}")
            self.connected = False
            return None

    def get_player_id(self) -> int:
        return self.player_id

    def reconnect(self, retries=3, delay=5):
        for attempt in range(retries):
            print(f"Attempting to reconnect ({attempt + 1}/{retries})...")
            if self.connect():
                print("Reconnected successfully.")
                return True
            time.sleep(delay)
        print("Failed to reconnect.")
        return False
