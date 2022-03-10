# Kịch bản Snort phát hiện SYN flood attack
## 1. SYN flood attack
- Một cuộc tấn công `SYN flood attack` là một loại tấn công từ chối dịch vụ khi đó kẻ tấn công gửi các yêu cầu `SYN` đến mục tiêu để tiêu tốn tài nguyên của máy chủ làm cho hệ thống không phản hồi các yêu cầu chính đáng.
- Một cuộc tấn công DDoS SYN flood tận dụng quy trình bắt tay 3 bước của TCP. Ở điều kiện bình thường, kết nối TCP được thể hiện 3 bước riêng biệt để tạo được kết nối như sau:
  
  ![](https://i.ibb.co/PQYcYdm/Screenshot-from-2021-10-31-21-51-31.png)

  + Client gửi 1 packet SYN đến Server để yêu cầu kết nối.
  + Sau khi tiếp nhận packet SYN, Server phản hồi lại client bằng một packet SYN/ACK để xác nhận thông tin từ Client.
  + Cuối cùng sau khi Client nhận được packet SYN/ACK sẽ trả lời server bằng packet ACK báo với server biết rằng nó đã nhận được packet SYN/ACK, kết nối đã được thiết lập và sẵn sàng trao đổi.
- Kẻ tấn công lợi dụng quy trình này để thực hiện tấn công từ chối dịch vụ -> Quy trình tấn công từ chối dịch vụ này được thể hiện như sau: 
  
  ![](https://i.ibb.co/p43H0LD/Screenshot-from-2021-10-31-21-51-44.png)

  + Kẻ tấn công gửi một khối lượng lớn các packet SYN đến Server mục tiêu.
  + Sau đó server phản hồi lại từng yêu cầu kết nối để lại 1 cổng mở sẵn sàng tiếp nhận và phản hồi.
  + Trong khi server chờ packet ACK ở bước cuối cùng từ client, packet này sẽ không bao giờ được gửi đến mà kẻ tấn công sẽ gửi thêm các packet SYN. Sự xuất hiện của các packet SYN mới khiến máy chủ tạm thời duy trì kết nối trong thời gian nhất định. Một khi tất cả các cổng có sẵn đều được sử dụng thì Server không thể hoạt động như bình thường.
   
  ![](https://i.ibb.co/0Y6tdN7/Screenshot-from-2021-10-31-21-54-28.png)

## 2. Snort phát hiện các cuộc tấn công SYN flood
- Mô hình lab
  + Attacker sẽ tấn công vào Web server có địa chỉ IP ghi như bên dưới.
  + Snort sẽ phát hiện cuộc tấn công từ attacker.
![](https://i.ibb.co/qDYhWyt/Screenshot-from-2021-10-31-21-54-37.png)

- Cấu hình phát hiện tấn công trên Snort

  ![](https://i.ibb.co/bNpG3Bw/Screenshot-from-2021-10-31-22-17-39.png)

  + `alert TCP $EXTERNAL_NET any  -> $HOME_NET any (msg:"TCP  SYN flood  attack  detected";  flags:S; threshold: type threshold, track by_dst, count 1000 , seconds 60; sid: 5000002;)`
  + `track_by_dst:` được theo dõi bởi IP đích.

- Thực hiện chạy snort để phát hiện bản tin.
![](https://i.ibb.co/T2mFfqr/Screenshot-from-2021-10-31-22-26-37.png)

- Thực hiện tấn công `SYN flood` bằng hping trên máy attacker.
  + `hping3 -S --flood -p 80 192.168.10.100`
- Trên Snort đã phát hiện thấy cuộc tấn công `SYN flood`
  ![](https://i.ibb.co/3ThkYLH/Screenshot-from-2021-10-31-22-28-48.png)

__Docs__
- https://www.ijcaonline.org/archives/volume178/number40/karmadenur-2019-ijca-919283.pdf?fbclid=IwAR2QDncYpAcba7F0i_1U-5gzuiEjed3tCDGx3Ht-XEmWqvYxCMsel496omA
- https://securitylab.disi.unitn.it/lib/exe/fetch.php?media=teaching%3Anetsec%3A2016%3Areports%3At11%3Agroup8_snort_lab_report.pdf&fbclid=IwAR19XsMqRM1DK1shkycqv_RJQeMGJKTQj8hBn_GfDv9CsrsxgsD6odKUQQ4

