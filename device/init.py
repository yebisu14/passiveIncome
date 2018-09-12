# -*- coding: utf-8 -*-

import requests
import json
from web3 import Web3, HTTPProvider
import urllib

"""
設定を合わせてください
"""
PRIVATE_KEY = "89A6CA8822BEE5ECFDA4E7709F561597D577FE5D3718894ABAAB3BBBD3C5003B"
ACCOUNT_ADDRESS = Web3.toChecksumAddress("0x5b865df8f925b557f21f19885ec2f88c73e0aab4")
BROADCAST_URI = "http://10.101.79.107:8080/"


DB_NAME = "./data.db"
INFURA = "https://ropsten.infura.io/v3/35d7622ec4464668b44f8313abfc09a9"
CONTRACT_ADDRESS = Web3.toChecksumAddress("0xd329d886f1131c43bb62966755761ecaa16e9318")

web3 = Web3(HTTPProvider(INFURA)) 

def initContract():
    # コントラクト初期化
    contractAddress = CONTRACT_ADDRESS
    abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[{"name":"purchaseUuid","type":"string"},{"name":"deviceWalletAddress","type":"address"}],"name":"addPurchase","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"deviceWalletAddress","type":"address"}],"name":"addDevice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"isBroadcastable","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"purchaseUuid","type":"string"},{"name":"walletAddress","type":"address"}],"name":"verifyPurchase","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]'

    abiJson = json.loads(abi)
    contract = web3.eth.contract(abi = abiJson, address = contractAddress)
    print("Contract was regulated.")
    return contract


"""
サムネイルのアップロード
"""
def upload():
    url = 'http://0.0.0.0:5000/upload'
    files = {
        'img': open("lena.png", "rb")
    }
    #url = '{}?{}'.format(url, urllib.parse.urlencode(params)))
    response = requests.post(url, files=files)
    response = json.loads(response.text)
    if(response['status'] == "OK"):
        return response['filename']
    
    return None


"""
配信リクエストの送信
デバイスの登録を行いたい
@param contract
@param walletAddress 自分のウォレットのID
@param uri 自分が配信しているURI
"""
def sendBroadcastRequest(contract, walletAddress, imgUri, broadcastUri):
    print("Sending broadcast request.")
    print("My address", walletAddress)
    print("My broadcast uri", broadcastUri)
    # コントラクト上に書き込む
    transaction = contract.functions.addDevice(walletAddress).buildTransaction({
        'nonce': web3.eth.getTransactionCount(ACCOUNT_ADDRESS)
    })
    signed = web3.eth.account.signTransaction(transaction, PRIVATE_KEY)
    result = web3.eth.sendRawTransaction(signed.rawTransaction)
    print("transaction result", Web3.toHex(result))

    # DMMに登録する、URLもいるのかな？
    url = 'http://0.0.0.0:5000/broadcast'
    params = {
        'addr': walletAddress,
        'img_uri': imgUri,
        'broadcast_uri': broadcastUri
    }
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    response = urllib.request.urlopen(req)
    res = response.read()
    print(res)


# コントラクト初期化
contract = initContract()

# ウォレットを作成する
#walletAddress = web3.eth.privateKeyToAccount(PRIVATE_KEY)
walletAddress = ACCOUNT_ADDRESS
print(walletAddress)

# サムネイルのアップロード
imgUri = upload()

# ブロードキャスト登録
sendBroadcastRequest(contract, walletAddress, imgUri, BROADCAST_URI)


