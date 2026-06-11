#!/bin/bash

# 1. 尝试修改配置 (不成功也没关系，所以不加 set -e)
find /etc/mysql/ -name "*.cnf" -print0 | xargs -0 sed -i 's/bind-address.*/bind-address = 0.0.0.0/' 2>/dev/null
find /etc/mysql/ -name "*.cnf" -print0 | xargs -0 sed -i 's/skip-networking/#skip-networking/' 2>/dev/null

# 2. 启动服务
service mariadb start

# 3. 关键：等待数据库真正准备好
echo "Waiting for MariaDB to start..."
MAX_TRIES=30
while ! mysqladmin ping -u root --silent; do
  sleep 1
  MAX_TRIES=$((MAX_TRIES - 1))
  if [ $MAX_TRIES -le 0 ]; then
    echo "MariaDB startup failed."
    exit 1
  fi
done

# 4. 权限设置 (使用兼容性更好的语法)
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING '';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;"
mysql -e "CREATE USER IF NOT EXISTS 'root'@'127.0.0.1' IDENTIFIED BY '';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'127.0.0.1' WITH GRANT OPTION;"
mysql -e "FLUSH PRIVILEGES;"

# 5. 导入数据
if [ -f /tmp/01init.sql ]; then
  echo "Importing SQL..."
  mysql </tmp/01init.sql
fi

# 6. 写入 GZCTF Flag
if [ "$GZCTF_FLAG" ]; then
  mysql -e "USE cttraining; UPDATE user SET password='$GZCTF_FLAG' WHERE name='Re0l flag';"
fi

echo "Everything is ready. Starting Apache..."
# 7. 必须以这个命令结尾，确保 Apache 在前台运行
apache2-foreground
