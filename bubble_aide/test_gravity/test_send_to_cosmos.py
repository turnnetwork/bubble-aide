import pytest
from bubble.inner_contract import InnerContractEvent
from eth_account import Account

from web3.exceptions import Web3ValidationError, InvalidAddress

from bubble_aide import Aide
from bubble_aide.script.contract_factory import gravity_abi, gravity_address, token_abi, token_address

from bubble_aide.script.me_chain import create_account

uri = 'https://go.getblock.io/2987ac3f2785423aa3399a96e91fd99a'
_tokenContract = '0xC43834641b46A6336d97aADEd4A547D0F5C3D7Dc'
# eth地址私钥
account = Account.from_key('cd0fbefc37cd448e2556a6ec5a07cf2b5adfb4cf5c3c5169b7e2f8563e04ea97')
# key = 'cd0fbefc37cd448e2556a6ec5a07cf2b5adfb4cf5c3c5169b7e2f8563e04ea97'

@pytest.mark.P1
def test_sent_to_cosmos_001():
    """
    测试 入金时，_tokenContract为空
    """
    # 通过Aide实例化节点对象
    aide = Aide(uri)
    # 通过gravity合约地址实例化合约对象
    gravity = aide.init_contract(abi=gravity_abi, address=gravity_address)
    print(gravity.address)
    assert "0x11a563BF4c2998759648bcaAdE832D55df949Ea9" == gravity.address

    _tokenContract = ''
    _destination = create_account()
    print(f"me用户地址地址:{_destination}")
    _amount = 4000000
    with pytest.raises(Web3ValidationError) as e:
        gravity.sendToCosmos(_tokenContract, _destination, _amount, private_key=account.key,
                                  txn={'gas': 800000, 'gasPrice': 50000000000})
    assert "Function invocation failed due to no matching argument types" in e.value.args[0]

@pytest.mark.P1
def test_sent_to_cosmos_002():
    """
    测试 入金时，_tokenContract地址在以太坊链上不存在
    """
    # 通过Aide实例化节点对象
    aide = Aide(uri)
    # 通过gravity合约地址实例化合约对象
    gravity = aide.init_contract(abi=gravity_abi, address=gravity_address)
    print(gravity.address)
    assert "0x11a563BF4c2998759648bcaAdE832D55df949Ea9" == gravity.address

    _tokenContract = '0x11a563BF4c2998759648bcaAdE832D55df949u20'
    _destination = create_account()
    print(f"me用户地址地址:{_destination}")
    _amount = 4000000
    with pytest.raises(InvalidAddress) as e:
        gravity.sendToCosmos(_tokenContract, _destination, _amount, private_key=account.key,
                                  txn={'gas': 800000, 'gasPrice': 50000000000})
    assert f"name: '{_tokenContract}' is invalid" in e.value.args[0]

@pytest.mark.P1
def test_sent_to_cosmos_003():
    """
    测试 入金时，_destination为空
    """
    # 通过Aide实例化节点对象
    aide = Aide(uri)
    # 通过gravity合约地址实例化合约对象
    gravity = aide.init_contract(abi=gravity_abi, address=gravity_address)
    print(gravity.address)
    assert "0x11a563BF4c2998759648bcaAdE832D55df949Ea9" == gravity.address

    _destination = ''
    print(f"me用户地址地址:{_destination}")
    _amount = 4000000

    usdt = aide.init_contract(abi=token_abi, address=token_address)
    befor_send = usdt.balanceOf(account.address)
    contract_balance1 = usdt.balanceOf(gravity.address)

    tx = gravity.sendToCosmos(_tokenContract, _destination, _amount, private_key=account.key,
                                  txn={'gas': 800000, 'gasPrice': 50000000000})
    print(tx)
    after_send = usdt.balanceOf(account.address)
    assert after_send + _amount == befor_send
    # gravity合约地址余额查询
    contract_balance2 = usdt.balanceOf(gravity.address)
    assert contract_balance1 + _amount == contract_balance2



@pytest.mark.P1
def test_sent_to_cosmos_004():
    """
    测试 入金时，_amount为空
    """
    # 通过Aide实例化节点对象
    aide = Aide(uri)
    # 通过gravity合约地址实例化合约对象
    gravity = aide.init_contract(abi=gravity_abi, address=gravity_address)
    print(gravity.address)
    assert "0x11a563BF4c2998759648bcaAdE832D55df949Ea9" == gravity.address

    _destination = create_account()
    print(f"me用户地址地址:{_destination}")
    _amount = None
    with pytest.raises(Web3ValidationError) as e:
        gravity.sendToCosmos(_tokenContract, _destination, _amount, private_key=account.key,
                                  txn={'gas': 800000, 'gasPrice': 50000000000})
    assert "Function invocation failed due to no matching argument types" in e.value.args[0]

@pytest.mark.P1
def test_sent_to_cosmos_005():
    """
    测试 入金时，用户地址上gas费不足
    """
    # 通过Aide实例化节点对象
    aide = Aide(uri)
    # 通过gravity合约地址实例化合约对象
    gravity = aide.init_contract(abi=gravity_abi, address=gravity_address)
    print(gravity.address)
    assert "0x11a563BF4c2998759648bcaAdE832D55df949Ea9" == gravity.address

    _destination = create_account()
    print(f"me用户地址地址:{_destination}")
    _amount = 4000000
    with pytest.raises(ValueError) as e:
        gravity.sendToCosmos(_tokenContract, _destination, _amount, private_key='9d9cb1a11aff872b37d87b4da394b16958228fda119d877b0ce3b731c5e2b053',
                                  txn={'gas': 800000, 'gasPrice': 50000000000})
    assert e.value.args[0]['code'] == -32000
    assert 'insufficient funds for gas * price + value: balance 0' in e.value.args[0]['message']


@pytest.mark.P1
def test_sent_to_cosmos_006():
    """
    测试 入金时，gas足够，_amount>用户地址上token余额
    """
    # 通过Aide实例化节点对象
    aide = Aide(uri)
    # 通过gravity合约地址实例化合约对象
    gravity = aide.init_contract(abi=gravity_abi, address=gravity_address)
    print(gravity.address)
    assert "0x11a563BF4c2998759648bcaAdE832D55df949Ea9" == gravity.address

    _destination = create_account()
    print(f"me用户地址地址:{_destination}")
    _amount = 400000000
    tx = gravity.sendToCosmos(_tokenContract, _destination, _amount, private_key='9d9cb1a11aff872b37d87b4da394b16958228fda119d877b0ce3b731c5e2b053',
                                  txn={'gas': 800000, 'gasPrice': 60000000000})
    print(tx)
    assert tx['status'] == 0

@pytest.mark.P1
def test_sent_to_cosmos_007():
    """
    测试 入金时，gas足够，_amount<=用户地址上token余额
    """
    # 通过Aide实例化节点对象
    aide = Aide(uri)
    # 通过gravity合约地址实例化合约对象
    gravity = aide.init_contract(abi=gravity_abi, address=gravity_address)
    _destination = create_account()
    print(f"me用户地址地址:{_destination}")
    _amount = 4000000
    usdt = aide.init_contract(abi=token_abi, address=token_address)
    befor_send = usdt.balanceOf(account.address)
    contract_balance1 = usdt.balanceOf(gravity.address)

    tx = gravity.sendToCosmos(_tokenContract, _destination, _amount, private_key=account.key,
                              txn={'gas': 800000, 'gasPrice': 50000000000})
    print(tx)
    assert tx['status'] == 1
    after_send = usdt.balanceOf(account.address)
    assert after_send + _amount == befor_send
    # gravity合约地址余额查询
    contract_balance2 = usdt.balanceOf(gravity.address)
    assert contract_balance1 + _amount == contract_balance2

@pytest.mark.P1
def test_sent_to_cosmos_008():
    """
    测试 入金交易成功后，核验交易事件信息正确
    """
    # 通过Aide实例化节点对象
    aide = Aide(uri)
    # 通过gravity合约地址实例化合约对象
    gravity = aide.init_contract(abi=gravity_abi, address=gravity_address)
    _destination = create_account()
    print(f"me用户地址地址:{_destination}")
    _amount = 4000000

    tx = gravity.sendToCosmos(_tokenContract, _destination, _amount, private_key=account.key,
                              txn={'gas': 800000, 'gasPrice': 80000000000})
    print(tx)
    assert tx['status'] == 1
    event = gravity.SendToCosmosEvent(tx)
    print(event)
    assert event[0]['args']['_tokenContract'] == _tokenContract
    assert event[0]['args']['_sender'] == account.address
    assert event[0]['args']['_destination'] == _destination
    assert event[0]['args']['_amount'] == _amount
    assert event[0]['args']['_eventNonce'] == gravity.state_lastEventNonce()



