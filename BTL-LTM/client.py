import socket
import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter import messagebox
from tkinter import PhotoImage
from network import Network
from game import Game
from PIL import Image, ImageTk
from replays import *

ip = "192.168.1.220"


def main_menu():
    root = tk.Tk()
    root.title("Main Menu")

    window_width = 650
    window_height = 450

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    image = Image.open("data/images/wallpaper/00_menu.png")
    image = image.resize((window_width, window_height), Image.Resampling.LANCZOS)
    background_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    btn_create_room = tk.Button(root, text="Tạo phòng", command=create_room_client)
    btn_create_room.place(relx=0.1, rely=0.7, anchor=tk.W)

    btn_join_room = tk.Button(root, text="Tham gia phòng", command=prompt_ip_port)
    btn_join_room.place(relx=0.1, rely=0.8, anchor=tk.W)

    btn_replay = tk.Button(root, text="Replay", command=choose_replay_file)
    btn_replay.place(relx=0.1, rely=0.9, anchor=tk.W)

    root.background_image = background_image
    root.mainloop()


# Chức năng chọn replay
def choose_replay_file():
    file_path = filedialog.askopenfilename(
        title="Chọn file replay",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
    )
    if file_path:
        start_replay(file_path)
    else:
        messagebox.showinfo("Thông báo", "Không có file được chọn.")


def start_replay(file_path):
    gameReplay = GameReplay()  #
    gameReplay.run_replay(file_path)


# Tạo phòng
def create_room_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            # Connect to the server
            sock.connect((ip, 5555))
            # Gửi yêu cầu phòng
            sock.sendall("new room please".encode())

            data = sock.recv(1024)

            message = data.decode()

            if message.isdigit():
                port = int(message)
                print(f"Received port number for new room: {port}")
                start_game(ip, port)
            else:
                print(f"Received message from the server: {message}")
        except socket.error as e:
            print(f"Socket error: {e}")


# Tham gia phòng
def prompt_ip_port():
    prompt_window = tk.Toplevel()
    prompt_window.title("Connect to Server")

    # Center the prompt window on the screen
    prompt_window_width = 300
    prompt_window_height = 200
    screen_width = prompt_window.winfo_screenwidth()
    screen_height = prompt_window.winfo_screenheight()
    center_x = int(screen_width / 2 - prompt_window_width / 2)
    center_y = int(screen_height / 2 - prompt_window_height / 2)
    prompt_window.geometry(
        f"{prompt_window_width}x{prompt_window_height}+{center_x}+{center_y}"
    )

    # IP
    tk.Label(prompt_window, text="Enter server IP:").pack()
    ip_entry = tk.Entry(prompt_window)
    ip_entry.pack()

    # Port
    tk.Label(prompt_window, text="Enter server port:").pack()
    port_entry = tk.Entry(prompt_window)
    port_entry.pack()

    # Nút kết nối
    def on_connect_button():
        ip = ip_entry.get()
        try:
            port = int(port_entry.get())
            start_game(ip, port)
            prompt_window.destroy()
        except ValueError:
            messagebox.showerror("Lỗi kết nối", "Cổng không hợp lệ. Vui lòng nhập lại.")
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới server: {e}")

    # Connect Button
    connect_button = tk.Button(
        prompt_window, text="Vào phòng", command=on_connect_button
    )
    connect_button.pack()


def start_game(ip, port):
    network = Network(ip, port)
    game = Game(network)
    game.run()


if __name__ == "__main__":
    main_menu()
