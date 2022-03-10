# Cài đặt Snort trên Rasbery PI 
- `apt-get --allow-releaseinfo-change update`
- Cài đặt các gói yêu cầu
  + `apt-get install -y build-essential autotools-dev libdumbnet-dev libluajit-5.1-dev libpcap-dev \
zlib1g-dev pkg-config libhwloc-dev cmake liblzma-dev openssl libssl-dev cpputest libsqlite3-dev \
libtool uuid-dev git autoconf bison flex libcmocka-dev libnetfilter-queue-dev libunwind-dev \
libmnl-dev ethtool`

- Cài đặt các gói snort cần để chạy 
  + `apt install -y build-essential`
  + `apt install -y libpcap-dev libpcre3-dev libdumbnet-dev`
  + `apt install -y bison flex`

- Tạo thư mục chứa toàn bộ source code của Snort
  + `mkdir snort_src`
- Tải gói DAQ
  + `wget https://www.snort.org/downloads/snort/daq-2.0.7.tar.gz`
  + `tar -xvzf daq-2.0.7.tar.gz`
  + `cd daq-2.0.7`
  + `./configure`
  + `make`
  + `make install`

- Cài đặt 1 số lib cho Snort
  + `apt install -y zlib1g-dev liblzma-dev openssl libssl-dev libnghttp2-dev`
- Cài đặt Snort
  + ` wget https://www.snort.org/downloads/snort/snort-2.9.18.1.tar.gz`
  + `tar -xvzf snort-2.9.18.1.tar.gz `
  + `cd snort-2.9.18.1`
  + `./configure --enable-sourcefire`
  + `make`
  + `make install`
- Cập nhật thư viện chia sẻ
  + `ldconfig`
- Đưa liên kết các thư viện của Snort vào `usr/sbin`
- Kiểm tra version của snort
  - `snort -V`

![](https://i.ibb.co/yYgDcq6/Screenshot-from-2021-10-07-23-02-01.png)

![](https://i.ibb.co/FJV3fYt/Screenshot-from-2021-10-07-23-02-30.png)

