# Chủ đề
Ứng dụng chơi game online "BattleArena.io"
# Thông tin nhóm
Phạm Huy Khôi - B20DCCN384
Mai Văn Thành - B20DCCN648
# Công nghệ sử dụng/ Ngôn ngữ
1. Python
2. TCP Socket
3. Multi Threading

# Mô tả kiến trúc, giao tiếp, chức năng chính
### Kiến trúc
+ Client - Server

### Giao tiếp
Lần đầu tiên khi một người dùng kết nối tới máy chủ game:
- Người dùng (client) gửi yêu cầu đến máy chủ
- Server sẽ phản hồi lại tuy yêu cầu tạo phòng hay tham gia
    Tạo phòng: server nhận yêu cầu và thực hiện mở 1 port để tạo 1 phòng chơi
    Tham gia: Người chơi sẽ kết nối vào port (phòng) tương ứng
Quá trình giao tiếp cho người chơi:
- Client có thể tạo phòng hoặc tham gia phòng có sẵn
- Server sẽ nhận yêu cầu tạo phòng và tạo phòng chơi
- Khi người chơi điều khiển nhân vật, client sẽ liên tục cập nhật vị trí, tình trạng, thông tin của nhân vật cho server 
- Server sẽ gửi dữ liệu tới client còn lại
- Quá trình trên sẽ được lặp đi lặp lại cho đến khi trận đấu kết thúc hoặc một người chơi thoát ra.

### Chức năng chính
Client:
- tham gia phòng có sẵn
- có thể yêu cầu tạo phòng mới
- xem lại trận đấu
Server:
- xử lý tạo phòng cho client
- quản lý thread của các phòng
- quản lý người chơi trong các phòng
- quản lý thông tin phòng và phân phối tới các client
### Thư viện xử lý
1. Sockets
2. Threading
3. Tkinter
4. Pygame
5. json
6. math

# Preview giao diện
2 client kết nối với server (2/11)
![image](https://github.com/jnp2018/g6_proj-384648/assets/116443724/bb99446b-9c71-4f40-b0c9-866955e1361a)

Menu
![image](https://github.com/jnp2018/g6_proj-384648/assets/108706249/5936c87e-48bd-4d3f-9a7a-de6cd6894e70)

Tham gia phòng
![image](https://github.com/jnp2018/g6_proj-384648/assets/108706249/549d1f3e-b3df-4b0e-9fb2-521e0738c14c)

Giao diện phòng chơi
![image](https://github.com/jnp2018/g6_proj-384648/assets/108706249/a881ec4a-eb69-47d1-a720-5c66c6d6db6d)

Thông tin trạng thái phòng được server quản lý
![image](https://github.com/jnp2018/g6_proj-384648/assets/108706249/ce23b2fa-6f6b-430d-af2e-2a8891156963)

Chức năng xem lại game đấu
![image](https://github.com/jnp2018/g6_proj-384648/assets/108706249/ac32f5a5-85ab-47a1-ac4b-ca8fb707742c)
![image](https://github.com/jnp2018/g6_proj-384648/assets/108706249/0f5000bc-29a5-4ff7-9ef8-838664e3c1c7)


# Cài đặt môi trường


# Triển khai
1. **Server**:
    - Chạy script `server.py` trên máy chủ.
    - Máy chủ sẽ lắng nghe trên một cổng cụ thể (ví dụ: 8080).
    
2. **Client**:
    - Chạy script `client.py` trên máy của người chơi.
    - Màn hình hiện thị 3 lựa chọn tạo phòng hoặc tham gia phòng, xem replay
    - Sau đó, người chơi có thể chọn và tham gia

