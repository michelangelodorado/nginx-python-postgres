# nginx-python-postgres-grafana



To run the modified script in the background, you can use a process manager like systemd (on Linux) to ensure it continues to run as a service. Here's how you can set up the script to run as a background service using systemd:

1. Save your Python script (e.g., nginxlog-to-postgres.py) in a directory of your choice.
2. Create a systemd service unit file to manage the script: Create a nginx_log_listener.service file in the /etc/systemd/system/ directory or /etc/systemd/user/ if you want to run it as a user service. You can create the file using a text editor like nano or vim.
For a system-wide service (requires root access):
sudo nano /etc/systemd/system/nginx_log_listener.service

3. Add the following content to the .service file, replacing <PATH_TO_SCRIPT> with the full path to your Python script:

```bash
[Unit]
Description=Continuous Nginx Log Listener

[Service]
ExecStart=/usr/bin/python3 <PATH_TO_SCRIPT>
WorkingDirectory=<DIRECTORY_OF_SCRIPT>
Restart=always
User=<YOUR_USERNAME>
Group=<YOUR_GROUP>
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=nginx_log_listener

[Install]
WantedBy=multi-user.target
```

Example:

```bash
[Unit]
Description=Continuous Nginx Log Listener

[Service]
ExecStart=/usr/bin/python3 /home/ubuntu/nginx-to-postgres.py
WorkingDirectory=/home/ubuntu/
Restart=always
User=ubuntu
Group=ubuntu
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=nginx_log_listener

[Install]
WantedBy=multi-user.target
```

ExecStart: Set this to the full path to your Python script.
WorkingDirectory: Set this to the directory containing your script.
User and Group: If running as a specific user is necessary, specify the user and group here.

4. Save the file and exit the text editor.
5. Reload systemd to apply the new service:
For a system-wide service:
```bash
sudo systemctl daemon-reload
```
6. Enable the service to start on boot:
For a system-wide service:
```bash
sudo systemctl enable nginx_log_listener.service
```
7. Start the service:
For a system-wide service:
```bash
sudo systemctl start nginx_log_listener.service
```

Your Python script will now run continuously in the background as a systemd service. You can check its status with:

```bash
systemctl status nginx_log_listener.service
```

template1=# SELECT http_apikey, COUNT(*) FROM nginx_logs GROUP BY http_apikey;
       http_apikey        | count
--------------------------+-------
 KxN+XQmvdb6Xnth7UaAtlczY |    29
(1 row)

template1=# SELECT http_apikey, DATE(time_local) AS day, COUNT(*) FROM nginx_logs GROUP BY http_apikey, day;
       http_apikey        |    day     | count
--------------------------+------------+-------
 KxN+XQmvdb6Xnth7UaAtlczY | 2023-11-06 |    29
(1 row)

template1=# SELECT http_apikey, DATE_TRUNC('hour', time_local) AS dayhr, COUNT(*) FROM nginx_logs GROUP BY http_apikey, dayhr;
       http_apikey        |        dayhr        | count
--------------------------+---------------------+-------
 KxN+XQmvdb6Xnth7UaAtlczY | 2023-11-06 11:00:00 |    17
 KxN+XQmvdb6Xnth7UaAtlczY | 2023-11-06 10:00:00 |     3
 KxN+XQmvdb6Xnth7UaAtlczY | 2023-11-06 13:00:00 |     9
(3 rows)
