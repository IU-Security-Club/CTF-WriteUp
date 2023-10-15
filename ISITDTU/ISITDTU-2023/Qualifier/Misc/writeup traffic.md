Bài này sử dụng wireshark để mở và đọc file pcap, sau đó dùng chức năng Follow TCP stream để đọc các context trao đổi của data

![tcp stream](/traffic/tcp.png "tcp stream")

Ta thấy được có 1 stream chứa tham số flag.

![traffic](/traffic/solve.png "flag")

Dùng cyberchef thì decode ra được flag.

![flag](/traffic/flag.png "flag")