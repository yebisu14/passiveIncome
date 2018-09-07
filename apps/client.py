# -*- coding: utf-8 -*-

import urllib.request
import json
import hashlib
import uuid
from web3 import Web3, HTTPProvider


UUID_FILE = "./purchase.dat"

def makeUuid():
    u4 = str(uuid.uuid4())
    print("Uuid was generated.", u4)
    return u4

def saveUuid(uuid):
    # uuidを保存しておく
    with open(UUID_FILE, 'a') as f:
        f.write(uuid)
    print("UUID was saved.", uuid)

def initContract():
    # コントラクト初期化
    web3 = Web3(HTTPProvider('http://localhost:9545'))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    contractAddress = Web3.toChecksumAddress("0x057d2360abbe75f9fdf142f2cfe68cfc9a74ec12")
    abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[{"name":"purchaseUuid","type":"string"},{"name":"deviceWalletAddress","type":"address"}],"name":"addPurchase","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"deviceWalletAddress","type":"address"}],"name":"addDevice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"isBroadcastable","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"purchaseUuid","type":"string"},{"name":"walletAddress","type":"address"}],"name":"verifyPurchase","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]'

    abiJson = json.loads(abi)
    contract = web3.eth.contract(abi = abiJson, address = contractAddress)
    print("Contract was regulated.")
    return contract


"""
1. 購入リクエストの送信
クライアントサイドで購入UUIDと呼ばれるものを生成し、保存しておく。
購入UUIDと購入者のウォレットアドレス、配信者のウォレットアドレスをペアにしてコントラクトに書き込む。
True or Falseが帰ればOK。
@param contract
@param buyerWalletAddress 買う人のアドレス(自己参照で解決できる)
@param sellerWalletAddress 売る人のアドレス(QRコードに乗っけておく)
@param uuidPurchase 購入UUID(自分で作成する)
"""
def sendPurchaseRequest(contract, buyerWalletAddress, sellerWalletAddress, uuidPurchase):
    # 購入情報をコントラクトに書き込む
    contract.functions.addPurchase(uuidPurchase, sellerWalletAddress).transact()
    #contract.functions.transfer()...
    # 購入の結果のみを表示する
    print("Purchase transaction OK.")


"""
2. 閲覧リクエストの送信
DMMに対して、閲覧の可否を聞く。
閲覧がOKなら動画URL、そうでなければinvalidが帰ってくる、。
"""
def sendWatchingRequest(uuidPurchase, sellerWalletAddress):
    print("Sending watching request.")
    print("Target device's wallet_address", sellerWalletAddress)
    print("Reciept to verify", uuidPurchase)

    url = 'http://0.0.0.0:5000/watch'
    params = {
        'pid': uuidPurchase,
        'addr': sellerWalletAddress
    }
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    response = urllib.request.urlopen(req)
    res = response.read()
    print(res)


"""
3. 配信リクエストの送信
デバイスの登録を行いたい
@param contract
@param walletAddress 自分のウォレットのID
@param uri 自分が配信しているURI
"""
def sendBroadcastRequest(contract, walletAddress, uri):
    print("Sending broadcast request.")
    print("My address", walletAddress)
    print("My broadcast uri", uri)
    # コントラクト上に書き込む
    contract.functions.addDevice(walletAddress).transact()
    # DMMに登録する、URLもいるのかな？
    url = 'http://0.0.0.0:5000/broadcast'
    params = {
        'addr': walletAddress,
        'uri': uri
    }
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    response = urllib.request.urlopen(req)
    res = response.read()
    print(res)




# 配信者側テストコード
# コントラクト初期化
contract = initContract()
# 自分のウォレットアドレス
myAddr = Web3.toChecksumAddress("0xf17f52151ebef6c7334fad080c5704d77216b732") # accounts[1]
#myAddr = Web3.toChecksumAddress("0xc5fdf4076b8f3a5357c5e395ab970b5b54098fef")
# 自分の配信アドレス
uri = "https://google.co.jp"
# リクエストを送る
sendBroadcastRequest(contract, myAddr, uri)



# 閲覧者側テストコード
"""
# UUIDを生成
uuidPurchase = makeUuid()
# UUIDを保存
saveUuid(uuidPurchase)
# コントラクトインスタンス生成
contract = initContract()
# 自身のアドレスも持ってきたことにする。
myAddr = Web3.toChecksumAddress("0x627306090abab3a6e1400e9345bc60c78a8bef57") # accounts[0]
# QRコードから購入動画と売り手のアドレスは持ってきたことにする。
sellAddr = Web3.toChecksumAddress("0xf17f52151ebef6c7334fad080c5704d77216b732")
print("my_wallet_address", sellAddr)
# あるデバイスに対して購入リクエストを送る
sendPurchaseRequest(contract, myAddr, sellAddr, uuidPurchase)
# あるデバイスに対して閲覧リクエストを送る
sendWatchingRequest(uuidPurchase, sellAddr)
"""
