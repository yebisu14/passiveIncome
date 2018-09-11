# -*- coding: utf-8 -*-

import configparser
from web3 import Web3, HTTPProvider
import json

config = configparser.ConfigParser()
config.read('config.ini')
accountAddress = Web3.toChecksumAddress(config.get('general', 'account_address'))

INFURA = "https://ropsten.infura.io/v3/35d7622ec4464668b44f8313abfc09a9"
CONTRACT_ADDRESS = Web3.toChecksumAddress("0xd329d886f1131c43bb62966755761ecaa16e9318")

web3 = Web3(HTTPProvider(INFURA)) 

abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"uuid","type":"string"}],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"getDepositedBalance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"deviceWalletAddress","type":"address"}],"name":"addDevice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"isBroadcastable","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"purchaseUuid","type":"string"},{"name":"walletAddress","type":"address"}],"name":"verifyPurchase","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]'
abiJson = json.loads(abi)
contract = web3.eth.contract(abi = abiJson, address = CONTRACT_ADDRESS)

n = contract.functions.getDepositedBalance(accountAddress).call()
n = Web3.fromWei(n, 'ether')
print("{} ETH".format(n))