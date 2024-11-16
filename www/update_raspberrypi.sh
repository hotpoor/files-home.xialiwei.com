python3 version_dev.py
rsync -avz xialiwei@192.168.100.50:~/Sites/files-home.xialiwei.com/www/sqlite_db/ ./sqlite_db/
coffee -c -o static/js static/coffee
rsync -avz . xialiwei@192.168.100.50:~/Sites/files-home.xialiwei.com/www/