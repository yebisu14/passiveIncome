"use strict";


/*
    送金処理を行ってから、ブロックチェーン上に書き込まれるまでに時間がかかるので
    自分の残高が変化したかどうかで書き込まれたかどうかを判定します
*/

var BalanceWatchdog = function(address, onChanged, onTimeout){
    this.count = 0;
    this.spend = 0;
    this.TIMEOUT = 30000; // 30秒間チェックする
    this.INTERVAL = 1000; // 1秒間隔でチェックする
    this.onChanged = onChanged;
    this.onTimeout = onTimeout;
    this.myAddress = address;
    this.pool = 0;
    this.timer = this.timer = setInterval(this.tick, this.INTERVAL);
};


BalanceWatchdog.prototype.tick = function(){
    console.log("tick");
    console.log(this);
    console.log(this.myAddress);
    this.stop();
    return;

    web3.eth.getBalance(this.myAddress, (err, val)=>{
        console.log(val);
    });
};

BalanceWatchdog.prototype.stop = function(){
    this.clearInterval(this.timer);
}



