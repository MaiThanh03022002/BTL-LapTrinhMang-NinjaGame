# server.py
from room import Room
import threading
import socket

host_ip = "192.168.1.220"


def find_available_port(start_port, end_port):
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host_ip, port))
                return port
            except socket.error:
                continue
    return None


def handle_new_room_request(conn, host):
    try:
        port = find_available_port(5556, 5565)
        if port:
            threading.Thread(target=start_server_room, args=(host, port)).start()
            conn.sendall(str(port).encode())
        else:
            conn.sendall("No available port".encode())
    finally:
        conn.close()


def listen_for_room_requests(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server is listening for room requests on {host}:{port}")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle_new_room_request, args=(conn, host)).start()


def start_server_room(host, port):
    room = Room(host, port)
    room.create_room()


request_listen_port = 5555  # Lắng nghe tạo phòng

threading.Thread(
    target=listen_for_room_requests, args=(host_ip, request_listen_port)
).start()

stop_event = threading.Event()

try:
    while not stop_event.is_set():
        stop_event.wait(timeout=1)
except KeyboardInterrupt:
    print("Shutting down the server.")
    stop_event.set()
