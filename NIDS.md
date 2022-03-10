# IDS (intrusion detection system)
## 1. Overview
- `IDS (instrustion detection system - hệ thống phát hiện xâm nhập)` là một thiết bị hoặc một ứng dụng phần mềm giám sát mạng, hệ thống máy tính về những hoạt động ác ý hoặc vi phạm các chính sách.
- `IDS` được chia thành 2 loại 
   + `Network-based IDS (NIDS)`: giám sát toàn bộ mạng, nguồn thông tin chủ yếu là các gói dữ liệu đang lưu thông trên mạng. `NIDS` thường được lắp đặt tại ngõ vào của mạng (inline), có thể đứng trước hoặc sau firewall.
   ![](https://raw.githubusercontent.com/hocchudong/ghichep-IDS-IPS-SIEM/master/Images/1_0.png)
   + `Host-based IDS (HIDS)`: giám sát hoạt động của từng máy tính riêng biệt, nguồn thông tin ngoài lưu lượng đến và đi trên máy chủ còn có hệ thống dữ liệu system log và system audit.
   ![](https://raw.githubusercontent.com/hocchudong/ghichep-IDS-IPS-SIEM/master/Images/2.png)

