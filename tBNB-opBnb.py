from web3 import Web3
import time
from tqdm import tqdm
import random

with open("wallets.txt", "r") as f:
    privatekeys = [row.strip() for row in f]
    random.shuffle(privatekeys)

############################################  ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ  #######################################
TST_FROM = 8 # от в процентах от баланса
TST_TO = 16 # до в процентах

wal_sleep_min = 40    # минимальная задержка между кошелька
wal_sleep_max = 70    # максимальная задержка между кошелька
###########################################################################################################


def sleep_indicator(secs):
    for i in tqdm(range(secs), desc='wait', bar_format="{desc}: {n_fmt}s / {total_fmt}s {bar}", colour='green'):
        time.sleep(1)


def withdraw(privatekey):
    w3 = Web3(Web3.HTTPProvider("https://data-seed-prebsc-1-s1.binance.org:8545"))
    account = w3.eth.account.from_key(privatekey)
    address = account.address
    token_balance = w3.eth.get_balance(w3.to_checksum_address(address))
    proc_of_min = int(token_balance * TST_FROM / 100)
    proc_of_max = int(token_balance * TST_TO / 100)
    _amount = int(round(random.uniform(proc_of_min, proc_of_max), 1))
    aw_round = int(round((_amount/10**18),5)*10**18) # делаем округление до 5 после запятом

    address_edited = address.rpartition('x')[2]
    data = '0xb1a1a8820000000000000000000000000000000000000000000000000000000000030d4000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000'
    try:
        tx = {
            'from': address,
            'to': Web3.to_checksum_address('0x677311fd2ccc511bbc0f581e8d9a07b033d5e840'),
            'value': int(aw_round),
            'nonce': w3.eth.get_transaction_count(address),
            'data': data,
            'chainId': w3.eth.chain_id,
            'gasPrice': int(w3.eth.gas_price)
        }

        tx['gas'] = w3.eth.estimate_gas(tx)
        sign = account.sign_transaction(tx)
        hash_ = w3.eth.send_raw_transaction(sign.rawTransaction)
        print(f'ADDRESS: {address}')
        print(f'Transaction hash: https://testnet.bscscan.com/tx/{hash_.hex()}')
        print('Waiting for receipt...')
        tx_receipt = w3.eth.wait_for_transaction_receipt(hash_, timeout=140)
        print('Отправил ETH: ' + str(aw_round/10**18))
        sleep_indicator(random.randint(wal_sleep_min, wal_sleep_max))
    except Exception as e:
        print(f'ADDRESS: {address}')
        print(f'Ошибка: {e}')



def main():
    for privatekey in privatekeys:
        withdraw(privatekey)
    print('Успешный вывод с tBNB в opBNB c ' + str(len(privatekeys)) + ' кошельков через официальный бридж')

if __name__ == '__main__':
    main()

