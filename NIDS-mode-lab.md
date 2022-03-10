# Cấu hình Snort NIDS mode
## 1. Cấu hình Snort mode NIDS
- Tạo các thư mục snort
    - `mkdir /etc/snort`
    - `mkdir /etc/snort/rules`
    - `mkdir /etc/snort/rules/iplists`
    - `mkdir /etc/snort/preproc_rules`
    - `mkdir /usr/local/lib/snort_dynamicrules`
    - `mkdir /etc/snort/so_rules`

- Tạo file để lưu trữ rule và danh sách IP
    - `touch /etc/snort/rules/iplists/black_list.rules`
    - `touch /etc/snort/rules/iplists/white_list.rules`
    - `touch /etc/snort/rules/local.rules`
    - `touch /etc/snort/sid-msg.map`

- Tạo thư mục lưu trữ log
    - `mkdir /var/log/snort`
    - `mkdir /var/log/snort/archived_logs`

- Copy các file cấu hình có sẵn trong source vào đường dẫn `/etc/snort`
   - `cd snort_src/snort-2.9.18.1/etc/`
   - `cp *.conf* /etc/snort`
   - `cp *.map /etc/snort/`
   - `cp *.dtd /etc/snort/`
   - `cd snort_src/snort-2.9.18.1/src/dynamic-preprocessors/build/usr/local/lib/snort_dynamicpreprocessor/`
   - `cp * /usr/local/lib/snort_dynamicpreprocessor/`
- Chỉnh lại thông số trong file cấu hình `/etc/snort/snort.conf`
   + `sed -i "s/include \$RULE\_PATH/#include \$RULE\_PATH/ " /etc/snort/snort.conf`
    
    ```
    # LINE 45 thay bằng internal network. Nếu muốn dải mạng external thì nên xài !$HOME_NET
    ipvar HOME_NET 192.168.0.0/24

    # LINE 104
    var RULE_PATH /etc/snort/rules
    var SO_RULE_PATH /etc/snort/so_rules
    var PREPROC_RULE_PATH /etc/snort/preproc_rules

    var WHITE_LIST_PATH /etc/snort/rules/iplists
    var BLACK_LIST_PATH /etc/snort/rules/iplists

    # Sử dụng file local.rules thì tại dòng 546 ta bỏ dấu #
    include /etc/snort/rules/local.rules
    ```

    ![](https://i.ibb.co/hdyg4TK/Screenshot-from-2021-10-08-21-41-33.png)

- Sau khi cấu hình xong, xác nhận lại file bằng câu lệnh:
   + `snort -T -i eth1 -c /etc/snort/snort.conf`

![](https://i.ibb.co/MPfgTd2/Screenshot-from-2021-10-08-21-44-04.png)

- Viết một rule đơn giản để test Snort Detection. Trong file `/etc/snort/rules/local.rules` thêm dòng sau:
   + `alert icmp any any -> $HOME_NET any (msg:"ICMP test detected"; GID:1; sid:10000001; rev:001; classtype:icmp-event;)`
- Cấu hình vào rule `/etc/snort/sid-msg.map` để bật cảnh báo
    ```
    #v2
    1 || 10000001 || 001 || icmp-event || 0 || ICMP Test detected || url,tools.ietf.org/html/rfc792`
    ```
- Chạy lại lệnh sau để chắc chắn cấu hình đúng
   + `snort -T -c /etc/snort/snort.conf -i eth1`

- Chạy test
    + `/usr/local/bin/snort -A console -q -c /etc/snort/snort.conf -i eth1`
- Thực hiện đứng từ máy khác ping tới máy snort để test 
   + Snort phát hiện được máy ping tới
   ![](https://i.ibb.co/vJz1db5/Screenshot-from-2021-10-08-21-56-41.png)

## 2. Cài đặt Barnyard 2 -> hỗ trợ xuất dữ liệu ra CSDL Mysql 
- Cài đặt các gói cần thiết
  + ` apt install gnupg`
  + `wget https://dev.mysql.com/get/mysql-apt-config_0.8.13-1_all.deb`
  + `dpkg -i mysql-apt-config_0.8.13-1_all.deb`
  + ` apt-get install -y default-mysql-server default-mysql-client autoconf libtool libmariadbclient-dev default-libmysqlclient-dev libgmp-dev`
- Barnyard2 sử dụng dữ liệu dưới dạng Binary nên cấu hình trong `/etc/snort/snort.conf` cần thay đổi như sau
  + `output unified2: filename snort.u2, limit 128`
- Cài đặt Barnyard2
    - `cd ~/snort_src`
    - `wget https://github.com/firnsy/barnyard2/archive/master.tar.gz`
    - `-O   barnyard2-Master.tar.gz`
    - `tar -xzvf barnyard2-Master.tar.gz`
    - `cd barnyard2-master/`
    - `autoreconf -fvi -I ./m4`
- Barnyard2 cần truy cập vào thư viện dnet.h, nên ta tạo một chỉ định cho thư viện
   + `ln -s /usr/include/dumbnet.h /usr/include/dnet.h`
   + `ldconfig`
- Trỏ từ barnyard tới MySQL xem đã đúng thư viện MySQL chưa bằng lệnh sau (do tôi sử dụng OS x64)
   + `./configure --with-mysql --with-mysql-libraries=/usr/lib/i386-linux-gnu/`
- Thực hiện cài đặt:
   + `make`
   + `make install`

![](https://i.ibb.co/gTgzZ1F/Screenshot-from-2021-10-08-22-55-05.png)

- Sau khi cài đặt xong, copy một số file cấu hình mà Barnyard2 yêu cầu để chạy:
    + `cp ~/snort_src/barnyard2-master/etc/barnyard2.conf /etc/snort/`
    + `mkdir /var/log/barnyard2`
    + `touch /var/log/snort/barnyard2.waldo`
- Cài đặt cơ sở dữ liệu 
    + `mysql -u root -p`
    + `create database snort;`
    + `use snort;`
    + `source ~/snort_src/barnyard2-master/schemas/create_mysql`
    + `CREATE USER 'snort'@'localhost' IDENTIFIED BY 'network123';`
    + `grant create, insert, select, delete, update on snort.* to 'snortdb'@'localhost';`
- Điền thông số kết nối cơ sở dữ liệu cho Barnyard2 trong file /etc/snort/barnyard2.conf, thêm vào cuối cùng của file dòng sau:
    ```
    # set the appropriate paths to the file(s) your Snort process is using.
    #
    config reference_file:      /etc/snort/etc/reference.config
    config classification_file: /etc/snort/etc/classification.config
    config gen_file:            /etc/snort/gen-msg.map
    config sid_file:            /etc/snort/sid-msg.map
    ```
   - `output database: log, mysql, user=snortdb password=network123 dbname=snort host=localhost sensor name=sensor01`
- Lúc này khi chạy câu lệnh snort sẽ không hiện ra log mà log sẽ thực hiện ở bên chạy lệnh barnyard2

   ![](https://i.ibb.co/7QB2vMV/Screenshot-from-2021-10-10-11-45-37.png)

- Cài đặt chạy Snort và Barnyard2 dưới dạng service cho hệ điều hành
  + Tạo file `/lib/systemd/system/snort.service` với nội dung như sau
  
  ![](https://i.ibb.co/k3jkGsv/Screenshot-from-2021-10-10-11-39-59.png)

  + Tạo file `/lib/systemd/system/barnyard2.service` với nội dung như sau

  ![](https://i.ibb.co/LgWcRXB/Screenshot-from-2021-10-10-11-41-17.png)

- Chạy 2 service
  + `service snort start`
  + `service barnyard2 start`
  -> Thực hiện ping như ở trên thì log không còn show ra màn hình nữa mà lưu vào cơ sở dữ liệu 

  ![](https://i.ibb.co/sHdYNwx/Screenshot-from-2021-10-10-11-42-34.png)

# 3. Cài đặt Base sử dụng giao diện web
- Cài đặt php-5.6 và apache2
  + `wget -q https://packages.sury.org/php/apt.gpg -O- | sudo apt-key add -`
  + `echo "deb https://packages.sury.org/php/ stretch main" | sudo tee /etc/apt/sources.list.d/php.list`
  + `apt-get install -y libapache2-mod-php5.6 php5.6 php5.6-common php5.6-gd php5.6-cli php5.6-xml php5.6-mysql`

- Tải và cài đặt ADODB:
   - `cd ~/snort_src`
   - `wget https://sourceforge.net/projects/adodb/files/adodb-php5-only/adodb-520-for-php5/adodb-5.20.8.tar.gz`
   - `tar -xvzf adodb-5.20.8.tar.gz`
   - `mv adodb5 /var/adodb`
   - `chmod -R 755 /var/adodb`

- Tải Base và copy vào apache
   - `cd ~/snort_src`
   - `wget http://sourceforge.net/projects/secureideas/files/BASE/base-1.4.5/base-1.4.5.tar.gz`
   - `tar xzvf base-1.4.5.tar.gz`
   - `mv base-1.4.5 /var/www/html/base/`

- Tạo file cấu hình Base
   + `cd /var/www/html/base`
   + `cp base_conf.php.dist base_conf.php`

- Cấu hình base_conf.php
   ```
   # line 50
   $BASE_urlpath = '/base'; 
   # line 80
   $DBlib_path = '/var/adodb/adodb5';
   # line 102
   $alert_dbname = 'snort'; 
   $alert_host = 'localhost';
   $alert_port = '';
   $alert_user = 'snort';
   # line 106
   $alert_password = 'network123'; 
   ```

   ![](https://i.ibb.co/jhXp18m/Screenshot-from-2021-10-10-16-25-11.png)

- Thiết lập quyền cho thư mục Base
   - `chown -R www-data:www-data /var/www/html/base`
   - `chmod o-r /var/www/html/base/base_conf.php`

- Truy cập vào đường dẫn `http://192.168.0.107/base/base_main.php`

![](https://i.ibb.co/zrTBzcG/Screenshot-from-2021-10-10-16-35-32.png)

![](https://i.ibb.co/kqLhfFT/Screenshot-from-2021-10-10-16-37-02.png)









