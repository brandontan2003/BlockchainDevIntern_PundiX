from datetime import datetime
from web3 import Web3
import json
import time, schedule
import csv

API_KEY = "e06d458abf304e1eac724658a3f04420"
url = f"https://mainnet.infura.io/v3/{API_KEY}"

w3 = Web3(Web3.HTTPProvider(url))

smart_contract = '0x6f1D09Fed11115d65E1071CD2109eDb300D80A27'
abi = json.loads('[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')

storage = []


def execute():
    block_number = w3.eth.get_block_number()

    # Get date from timestamp on the ETH blockchain
    timestamp = w3.eth.getBlock(block_number).timestamp
    date_time = datetime.fromtimestamp(timestamp)
    date = str(date_time)

    #PundiX Balance
    pundix_address = "0x0FD10b9899882a6f2fcb5c371E17e70FdEe00C38"
    pundix_contract = w3.eth.contract(address=pundix_address, abi=abi)

    pundix_balance = pundix_contract.functions.balanceOf(smart_contract).call()
    pundix_decimals = pundix_contract.functions.decimals().call()
    smart_contract_pundix_balance = pundix_balance / (10 ** pundix_decimals)
    pundix_symbol = pundix_contract.functions.symbol().call()


    #USDT Balance
    usdt_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    usdt_contract = w3.eth.contract(address=usdt_address, abi=abi)

    usdt_balance = usdt_contract.functions.balanceOf(smart_contract).call()
    usdt_decimals = usdt_contract.functions.decimals().call()
    smart_contract_usdt_balance = usdt_balance / (10 ** usdt_decimals)
    usdt_symbol = usdt_contract.functions.symbol().call()


    #WETH Balance
    weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    weth_contract = w3.eth.contract(address=weth_address, abi=abi)

    weth_balance = weth_contract.functions.balanceOf(smart_contract).call()
    weth_decimals = weth_contract.functions.decimals().call()
    smart_contract_weth_balance = weth_balance / (10 ** weth_decimals)
    weth_symbol = weth_contract.functions.symbol().call()


    #DAI Balance
    dai_address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    dai_contract = w3.eth.contract(address=dai_address, abi=abi)

    dai_balance = dai_contract.functions.balanceOf(smart_contract).call()
    dai_decimals = dai_contract.functions.decimals().call()
    smart_contract_dai_balance = dai_balance / (10 ** dai_decimals)
    dai_symbol = dai_contract.functions.symbol().call()

    result = date, block_number, (str(smart_contract_pundix_balance) + pundix_symbol), (str(smart_contract_usdt_balance) + usdt_symbol), (str(smart_contract_weth_balance) + weth_symbol), (str(smart_contract_dai_balance) + dai_symbol)
    storage.append(result)
    return storage


schedule.every(1).seconds.do(execute)

start = time.time()

PERIOD_OF_TIME = 60

header = ['Timestamp', 'Block Number', 'PUNDIX', 'USDT', 'WETH', 'DAI']

while True:
    schedule.run_pending()
    if time.time() > start + PERIOD_OF_TIME:
        f = open('fx-bridge token supply.csv', 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(header)
        for i in storage:
            writer.writerow(i)
        f.close()
        break
