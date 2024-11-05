import paramiko
import sys


def pl_ssh(ip="192.168.0.207", password="12345678", username="user1", port="22"):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    try:
        ssh_client.connect(hostname=ip, username=username, password=password, port=port)
        print('服务器%s连接成功' % ip)
    except Exception as e:
        print('服务器%s连接失败' % ip)
        print(e)
        sys.exit()
    # stdin, stdout, stderr = ssh_client.exec_command(cmd)
    # print('服务器%s磁盘使用率情况' % ip)
    # print(stdout.read().decode("utf-8"))
    return ssh_client


if __name__ == '__main__':
    servers = {
        "192.168.0.207": {
            "username": "user1",
            "password": "12345678",
            "cmd": "df -h",
            "port": "22"
        },
        # "192.168.0.8":{
        #     "username": "root",
        #     "password": "hadoop",
        #     "cmd": "df -h",
        #     "port": "22"
        # }
    }
    # for ip, info in servers.items():
    #     pl_ssh(ip=ip,
    #            username=info.get("username"),
    #            password=info.get("password"),
    #            cmd=info.get("cmd"),
    #            port=info.get("port")
    #            )
    ssh_client = pl_ssh()
    path_command = "cd gravity-Bridge/bin/"
    _, _, _ = ssh_client.exec_command(path_command)
    _, stdout, _ = ssh_client.exec_command("me-chaind keys add cc09 --keyring-backend=test")

    print(stdout.read().decode())
    ssh_client.close()
