import json
import socket
import threading

class Room:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.scores = {0: 0, 1: 0}
        self.connected = 0
        self.pos = ["0:50,50", "1:100,100"]
        self.currentId = "0"
        
    def display_room_details(self):
        print(f"Room Details - Host: {self.host}, Port: {self.port}")
        print(f"Connected Clients: {self.connected}")
        print(f"Player Positions: {self.pos}")
        print(f"Player Scores: {self.scores}")
        
    def threaded_client(self, conn, currentId):
        conn.send(str.encode(currentId))
        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                
                reply = data.decode("utf-8")
         
                arr = reply.split(":")
                id = int(arr[0])
                self.pos[id] = reply
                
                # Dữ liệu thông tin phòng
                port_str = str(self.port)
                num_str = str(self.connected)
                # Sắp xếp từ điểm số cao xuống thấp trong scores_dict và tạo chuỗi
                sorted_scores_str = ','.join([f"{player_id}:{score}" for player_id, score in sorted(self.scores.items(), key=lambda item: item[1], reverse=True)])
                string_detail = f"{port_str},{num_str},{sorted_scores_str}"
                if id == 0:
                    data_to_send = {
                        "opponent_position": self.pos[1],
                        "room_info": string_detail,
                        "player_id": id
                    }
                    json_data_to_send = json.dumps(data_to_send)
                    conn.sendall(json_data_to_send.encode())
                    # print(f"Sent to player {currentId}: {json_data_to_send}")
                elif id == 1:
                    # Create a dictionary with the data
                    data_to_send = {
                        "opponent_position": self.pos[0],
                        "room_info": string_detail,
                        "player_id": id
                    }
                    json_data_to_send = json.dumps(data_to_send)
                    conn.sendall(json_data_to_send.encode())
                    # print(f"Sent to player {currentId}: {json_data_to_send}")                    
            except Exception as e:
                print(f"An error occurred: {e}")
                break
        print("Player " + currentId + " has left the room.")

        self.connected -= 1
        self.display_room_details()
        print("Connection Closed")
        conn.close()

    def create_room(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            s.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))
            return

        s.listen(20)
        print(f"Waiting for a connection, Server Started on host {self.host}, port {self.port}")

        while True:
            conn, addr = s.accept()
            print("Connected to:", addr)
            self.scores[int(self.currentId)] = 0
            self.connected += 1
            self.display_room_details()
            threading.Thread(target=self.threaded_client, args=(conn, self.currentId)).start()
            self.currentId = "1" if self.currentId == "0" else "0"
            # if self.connected >= 2:  # Assuming only 2 players per room
            #     break
