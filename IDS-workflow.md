# Cơ chế hoạt động của IDS 
## 1. Kiến trúc của Snort
- Snort bao gồm nhiều thành phần. mỗi phần có một chức năng riêng biệt
    + `Module giải mã gói tin`
    + `Module tiền xử lý`
    + `Module phát hiện`
    + `Module log và cảnh báo`
    + `Module kết xuất thông tin`
### Module giải mã gói tin 
- Snort sử dụng thư viện pcap để bắt mọi gói tin trên mạng lưu thông qua hệ thống.
- Một gói tin sau khi giải mã sẽ đưa tiếp vào module tiền xử lý.

### Module tiền xử lý
- Module này gồm 3 nhiệm vụ chính
    + `Kết hợp lại các gói tin:` Khi một dữ liệu lớn được gửi đi, thông tin sẽ không đóng gói vào một gói tin mà thực hiện phân mảnh rồi mới gửi đi -> Module tiền xử lý giúp Snort hiểu được các phiên làm việc khác nhau.
    + `Giải mã và chuẩn hóa giao thức (decode/normalize):` Công việc phát hiện xâm nhập dựa trên dấu hiệu nhận dạng nhiều khi thất bại khi kiểm tra các giao thức có dữ liệu có thể được biểu diễn dưới nhiều dạng khác nhau. 
        + Ví dụ: một Web server có thể nhận nhiều dạng URL: URL viết dưới dạng hexa/unicode hay URL chấp nhận dấu / hay \. 
        + Nếu Snort chỉ thực hiện đơn thuần việc so sánh dữ liệu với dấu hiệu nhận dạng sẽ xảy ra tình trạng bỏ sót hành vi xâm nhập. Do vậy, 1 số Module tiền xử lý của Snort phải có nhiệm vụ giải mã và chỉnh sửa, sắp xếp lại các thông tin đầu vào.
    + `Phát hiện các xâm nhập bất thường (nonrule/anormal):` các plugin dạng này thường để xử lý với các xâm nhập không thể hoặc rất khó phát hiện bằng các luật thông thường. Phiển bản hiện tại của Snort có đi kèm 2 plugin giúp phát hiện xâm nhập bất thường đó là portscan và bo (backoffice). 
        + `Portscan` dùng để đưa ra cảnh báo khi kẻ tấn công thực hiện quét cổng để tìm lỗ hổng. 
        + `Bo` dùng để đưa ra cảnh báo khi hệ thống nhiễm trojan backoffice.
    
### Module phát hiện 
- Chịu trách nhiệm phát hiện các dấu hiệu xâm nhập.
- Module sử dụng các rule được định nghĩa ra trước để so sánh với dữ liệu thu thập được.
- Module phát hiện có khả năng tách các phần của gói tin ra và áp dụng rule lên từng phần của gói tin.
    + IP header
    + Header tầng transport: TCP, UDP
    + Header tầng application: DNS, HTTP, FTP,...
    + Data gói tin

### Module log và cảnh báo
- Các file log là các file dữ liệu có thể ghi dưới nhiều định dạng khác nhau.

### Module kết xuất thông tin 
- Module này thực hiện các thao tác khác nhau tùy thuộc vào việc cấu hình lưu kết quả được xuất ra đâu.

## 3. Rule của Snort
- `alert icmp any any -> $HOME_NET any (msg:"ICMP test detected"; GID:1; sid:10000001; rev:001; classtype:icmp-event;)`
- Gồm 2 phần là header và option:
    + Phần header chứa thông tin về hành động mà luật đó sẽ thực hiện khi phát hiện có xâm nhập, nó cũng chứa tiêu chuẩn để áp dụng luật với gói tin đó.
    + Phần option chứa thông điệp cảnh báo và các thông tin về các phần của gói tin dùng để tạo nên cảnh báo. Phần option chứa các tiêu chuẩn phụ thêm để đối sánh với gói tin.

### 3.2. Cấu trúc phần header

Action|Protocol|Address|Port|Direction|Address|Port|
|-----|--------|--------|---|---------|-------|----|
|alert|icmp|any|any|->|192.168.1.0/24|any|

#### 3.2.1. Action
- Là phần quy định loại hành động nào được thực thi. Thông thường các hành động tạo ra một cảnh báo hoặc log thông điệp hoặc kích hoạt một hành động khác.
- Có 5 hành động được định nghĩa
    + `Pass:` Cho phép bỏ qua gói tin này.
    + `Log:` Dùng để log gói tin. Có thể log ngay vào CSDL.
    + `Alert:` Gửi thông điệp cảnh báo khi dấu hiệu xâm nhập được phát hiện.
    + `Activate:` Tạo cảnh báo và kích hoạt thêm các luật khác để kiểm tra thêm điều kiện của gói tin.
    + `Dynamic:` Luật được gọi bằng các luật khác có action là `activate`.

#### 3.2.2. Protocol
- Chỉ ra gói tin mà giao thức được áp dụng.
- Sử dụng header IP để xác định loại giao thức.

#### 3.2.3. Address
- Có 2 phần là địa chỉ đích hoặc địa chỉ nguồn.
- Có thể là một IP đơn hoặc 1 dải mạng, nếu là any thì áp dụng cho tất cả các địa chỉ trong mạng.
- Nếu là một host thì có dạng `X.X.X.X/32`.
- Snort cung cấp phương pháp để loại trừ địa chỉ IP bằng cách sử dụng dấu !.
    + `alert icmp ![192.168.0.0/22] any -> any any (msg: “Ping with TTL=100”; ttl: 100;)`

#### 3.2.4. Port
- Số port để áp dụng cho các rule.
- Để sử dụng một dãy port thì dùng dấu `:`. 
    + `alert udp any any 1024:9090 -> any any ...`

#### 3.2.5. Direction
- Chỉ ra đâu là nguồn đâu là đích.
- `<>` khi muôn kiểm tra cả client và cả server.

### 3.3. Phần Option
- Nằm ngay sau phần header và được bọc trong dấu ngoặc đơn. Nếu có nhiều option thì sẽ phân biệt với nhau bằng dấu `;`.
- Một option sẽ gồm 2 phần, 2 phần này ngăn cách nhau bằng dấu `:`.

#### 3.3.1. Classtype
#### 3.3.2. Content
#### 3.3.3. dsize
#### 3.3.4. Flags
#### 3.3.5. fragbits

__Docs__
- https://viblo.asia/p/network-tim-hieu-co-che-cach-hoat-dong-cua-ids-phan-2-pDljMbe5RVZn