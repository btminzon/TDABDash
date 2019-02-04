import paramiko

server = "temsremote-8b71"
username = "root"
password = "!1nf0Vi5ta!"
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect(server, username=username, password=password)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(["cd /temp", "adb logcat |grep temperature"])
