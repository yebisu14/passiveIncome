      /*
        送金処理を行ってから、ブロックチェーン上に書き込まれるまでに時間がかかるので
        自分の残高が変化したかどうかで書き込まれたかどうかを判定します
      */
     class BalanceWatchdog{
        
        constructor(address, onChanged, onTimeout){
          this.count = 0;
          this.spend = 0;
          this.TIMEOUT = 30000; // 30秒間チェックする
          this.INTERVAL = 1000; // 1秒間隔でチェックする
          this.onChanged = onChanged;
          this.onTimeout = onTimeout;
          this.myAddress = address;
          this._pool = 0;

          web3.eth.getBalance(this.myAddress, this.handler);
          this.timer = setInterval(this.tick, this.INTERVAL);
        }

        handler(err, b){
            var n = web3.fromWei(b[0], "ether");
            console.log(n);
            this.pool = n;
        }

        stop(){
          clearInterval(this.timer);
        }

        tick(){
            console.log("tick");
            //console.log(this.pool);
        }        

        balanceCheck(b){

        }

        
        set pool(val){
            this._pool = val;
        }

        get pool(){
            return this._pool;
        }
        

    };