/*
    コントラクトにアクセスするためのメソッド類を集めた
*/

//  web3.version == 0.20.2

var abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"constant":false,"inputs":[],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"uuid","type":"string"}],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"getDepositedBalance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"deviceWalletAddress","type":"address"}],"name":"addDevice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"isBroadcastable","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"purchaseUuid","type":"string"},{"name":"walletAddress","type":"address"}],"name":"verifyPurchase","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"}]'
var abiJson = JSON.parse(abi)
var contractAddress = '0xd329d886f1131c43bb62966755761ecaa16e9318';
var contract = web3.eth.contract(abiJson).at(contractAddress);

function buyMovieOnContract(to, u4, onSuccess, onError){
    contract.deposit(to, u4, {value: web3.toWei(0.1, "ether")}, (err, result)=>{
        if(err){
            onError(err);
        }else{
            onSuccess(result);
        }
    });
}

function getDepositedBalanceInEthOnContract(onSuccess, onError){
    var myAddress = web3.eth.defaultAccount;
    
    contract.getDepositedBalance(myAddress, function(err, balance){
        if(err){
            onError(err);   
        }else{
            var n = web3.fromWei(balance, "ether");
            onSuccess(n);
        }
    });

}

function withdrawOnContract(onSuccess, onError){
    /* withdrawコントラクトの発行 */
    contract.withdraw(function(err, result){
        if(err){
            onError(err);
        }else{
            onSuccess(result);
        }
    });
}







