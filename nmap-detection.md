# Detection NMAP Scan Using Snort - cách phát hiện quét nmap sử dụng Snort

- Thực hiện Snort chống lại quá trình quét `nmap` khác nhau, điều này giuups nhà phân tích an ninh mạng thiết lập quy tắc snort để phát hiện bất kì loại quét nmap nào.

## Phát hiện NMAP ping scan
- Như chúng ta đã biết, bất kì kẻ tấn công nào cũng bắt đầu cuộc tấn công bằng cách xác dịnh trạng thái máy chủ bằng cách gửi gói ICMP 
- Thêm luật để phát hiện lưu lượng đi tới của giao thức ICMP

![](https://i.ibb.co/j4hKXDC/2021-12-02-21-36.png)

- Trên máy attacker thực hiện dò quét qua câu lệnh nmap.
    + `nmap -sP 192.168.0.103 --disable-arp-ping`

## Phát hiện NMAP TCP scan
- Để kết nối đến mạng mục tiêu, kẻ tấn công có thể tiến hành liệt kê mạng bằng cách sử dụng giao thức TCP hoặc giao thức UDP. Giả sử kẻ tấn công có thể chọn quét TCP để liệt kê mạng thì trong tình húông đó chúng ta có thể áp dụng quy tắc sau trong file quy tắc của Snort

![](https://i.ibb.co/ygvLTsd/2021-12-02-21-37-1.png)


- Quy tắc trên chỉ áp dụng cho port 22, nếu muốn thay thế từ bất kì cổng nào khác thì thay thế cổng 22 bằng cổng muốn quét -> Có thể sử dụng any để cảnh báo cho toàn bộ các cổng.

![](https://i.ibb.co/9cqxkwx/2021-12-02-21-38.png)

![](https://i.ibb.co/LnNxrBg/2021-12-02-21-38-1.png)

## UDP Scan

![](https://i.ibb.co/9pyRSwq/2021-12-02-21-50.png)

![](https://i.ibb.co/jysLPfv/2021-12-02-21-52.png)

![](https://i.ibb.co/w6yFmdt/2021-12-02-21-51.png)

## NMAP XMAS Scan

![](https://i.ibb.co/CPNqQ4P/2021-12-02-21-57.png)

![](https://i.ibb.co/6HGdGG2/2021-12-02-21-58.png)

![](https://i.ibb.co/Qnv1tkZ/2021-12-02-21-58-1.png)



