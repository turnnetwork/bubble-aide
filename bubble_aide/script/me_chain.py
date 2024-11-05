import time
from random import randint

from bubble_aide.script.conncet_ssh import pl_ssh


# 创建一个me用户地址,返回创建的用户地址及对应私钥
def create_account(user_name=int(round(time.time() * 1000))):
    ssh_client = pl_ssh(ip='118.175.0.230', password='c]km&Mcd88@0814275381$$$', username='user1', port='31001')
    command = f"me-chaind keys add {user_name} --keyring-backend=test"
    _, stdout, _ = ssh_client.exec_command(command)
    str_res1 = stdout.read().decode()
    command = f"echo y | me-chaind keys export {user_name} --unsafe --unarmored-hex --home=/home/user1/.me-chain --keyring-backend=test"
    _, stdout, _ = ssh_client.exec_command(command)
    str_res2 = stdout.read().decode()
    try:
        new_account = str_res1[11:52]
        ssh_client.close()
        return new_account, str_res2
    except:
        print("用户创建失败")



# 查询me用户地址余额
def get_balance(address):
    ssh_client = pl_ssh()
    command = f"me-chaind q bank balances {address}"
    _, stdout, _ = ssh_client.exec_command(command)
    print(stdout.read().decode())
    ssh_client.close()


# 国库给超管转钱【超管操作】
def send_to_admin(super_admin="me1uswualqpzsv7l95p7pv4ltm5m8zzan3g0audrv"):
    ssh_client = pl_ssh()
    command = f"me-chaind tx bank sendToAdmin 1000000mec --from={super_admin} --chain-id=me-chain --keyring-backend=test --fees=10000umec -y"
    _, stdout, _ = ssh_client.exec_command(command)
    print(stdout.read().decode())
    ssh_client.close()


# 超管往个人用户转钱【超管操作】,返回交易hash
def send_to_user(user_address, balance='10000umec', super_admin="me1uswualqpzsv7l95p7pv4ltm5m8zzan3g0audrv"):
    ssh_client = pl_ssh()
    command = f"me-chaind tx bank send {super_admin} {user_address} {balance} --chain-id=me-chain --keyring-backend=test --fees=100000umec -y"
    _, stdout, _ = ssh_client.exec_command(command)
    str_res = stdout.read().decode()
    print(str_res)
    try:
        tx_hash = str_res[-65:]
        print(tx_hash)
        ssh_client.close()
        return tx_hash
    except:
        print("转账交易执行失败")


# 通过交易hash查询me链上交易回执
def get_tx_by_hash(tx_hash):
    ssh_client = pl_ssh(ip='118.175.0.230', password='c]km&Mcd88@0814275381$$$', username='user1', port='31001')
    command = f"me-chaind q tx {tx_hash}"
    _, stdout, _ = ssh_client.exec_command(command)
    print(stdout.read().decode())
    ssh_client.close()


# me 出金到ETH
def out_token(amount, ibc_address, to_address, from_address, orc1_address='gravity1d9wrxdgtu7rj842zq4ulgk9k5hew3qfayr0gky',):
    ssh_client = pl_ssh()
    command = f"""me-chaind tx ibc-transfer transfer transfer channel-0 {orc1_address} {amount}ibc/{ibc_address} --memo '{"eth_address":{to_address},"bridge_fee":"800000","chain_fee":"0"}' --chain-id me-chain --from {from_address} --keyring-backend test --fees 10000umec -y"""
    _, stdout, _ = ssh_client.exec_command(command)
    print(stdout.read().decode())
    ssh_client.close()




if __name__ == '__main__':
    account, key = create_account()   #me17x768yyx056u7pdkdhqur7k4r96r3mcamncl85
    print(account, key)
    # get_balance('me17x768yyx056u7pdkdhqur7k4r96r3mcamncl85')
    # send_to_user('me17x768yyx056u7pdkdhqur7k4r96r3mcamncl85', '1000000000000umec')
    # get_tx_by_hash('55D99EFAE5ABBE2BB2652D306AB5828205B192007233DFEBBDCD2650D04EA5F6')
    # time.sleep(10)
    # get_balance('me1cutarj7mrmmycgn0fxyc9dj38jdrt92n88dch8')
    # out_token(4000000, 'AFCBD58BDB678E9C1E06D3716999FFB690C09D0E1860F9BFB3E86565E5E7FF55', '0x0E689b2Cb9Dadc0713602E7c7bE64D57E7fF2D5D', 'me1ez7yqsw5dh7zhsxdzg9njyqf49yegyf5wl7pgk')
    # time.sleep(15)
    # get_balance('me1ez7yqsw5dh7zhsxdzg9njyqf49yegyf5wl7pgk')

