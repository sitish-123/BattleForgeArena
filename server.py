import socket
import threading
import pickle
from _thread import start_new_thread
from network import PlayerState


class GameServer:
    playercount = 0

    def __init__(self, host='localhost', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server.bind((host, port))
        except socket.error as e:
            print(f"Server binding error: {e}")
            exit(1)
        self.server.listen(2)
        self.players = {}
        self.game_states = {
            0: PlayerState(200, 300, 100, 1, 0, False, 0, False, False, False),
            1: PlayerState(600, 300, 100, 1, 0, False, 0, False, True, False),
        }
        print("Server started, waiting for connections...")

    def threaded_client(self, conn, player_id):
        try:
            # Send player ID to the client
            conn.send(str(player_id).encode())

            while True:
                try:
                    # Receive and process incoming data
                    data_length = int.from_bytes(conn.recv(4), byteorder='big')
                    data = b""
                    while len(data) < data_length:
                        packet = conn.recv(4096)
                        if not packet:
                            raise ConnectionError("Connection lost while receiving data.")
                        data += packet

                    client_state = pickle.loads(data)

                    # Update the server's state for this player
                    self.game_states[player_id] = client_state

                    # Prepare and send the updated states back
                    response_data = pickle.dumps(self.game_states)
                    conn.sendall(len(response_data).to_bytes(4, byteorder='big') + response_data)

                except (socket.error, pickle.PickleError) as e:
                    print(f"Error handling player {player_id}: {e}")
                    break

        except ConnectionError as e:
            print(f"Player {player_id} disconnected unexpectedly: {e}")

        finally:
            print(f"Connection lost from Player {player_id}")
            self.game_states.pop(player_id, None)
            conn.close()

    def run(self):
        player_count = 0
        while True:
            try:
                conn, addr = self.server.accept()
                print(f"Connected to: {addr}")

                if player_count < 2:
                    start_new_thread(self.threaded_client, (conn, player_count))
                    player_count += 1
                    playercount=player_count
                else:
                    print("Maximum players connected. Rejecting new connection.")
                    conn.close()

            except Exception as e:
                print(f"Server error: {e}")

        self.server.close()


if __name__ == "__main__":
    server = GameServer()
    server.run()
