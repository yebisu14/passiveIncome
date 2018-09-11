pragma solidity ^0.4.18;

// This is just a simple example of a coin-like contract.
// It is not standards compatible and cannot be expected to talk to other
// coin/token contracts. If you want to create a standards-compliant
// token, see: https://github.com/ConsenSys/Tokens. Cheers!

contract MetaCoin {
	

	/*
		sharesに値が入っていれば引き出せる。
		お金はコントラクト上にshareとして持っておき、それをやりとりする
	*/
    /// Mapping of ether shares of the contract.
    mapping(address => uint) shares;
    /// Withdraw your share.
    function withdraw() public {
        uint share = shares[msg.sender];
        shares[msg.sender] = 0;
        msg.sender.transfer(share);
    }
	function deposit(address to, string uuid) public payable{
		shares[to] += msg.value;
		purchases[uuid].deviceWalletAddress = to;
	}

    function getDepositedBalance() public view returns(uint){
        return shares[msg.sender];
    }
    
    function MetaCoin() public{
        
    }
  

	/*
		動画を許可しているかどうか
		key: ユーザのウォレットアドレス＋ラズパイのUUID
		value: アクセスできるかどうか
	*/
	struct BroadcastStatus{
		bool owner; // dmmがブロードキャストを許可している
		bool user; // userがブロードキャストを許可している
	}

	struct Purchase{
		address deviceWalletAddress; 
	}


	/*
		購入履歴データ
		購入UUIDを紐づける
	*/
	mapping (string => Purchase) purchases;





	/*
		配信デバイスを追加
	*/
	function addDevice(address deviceWalletAddress) public {

	}

	/*
		配信許可かどうか
		とりあえずいつもOK
	*/
	function isBroadcastable(address addr) public constant returns(bool){
		return true;
	}


	function verifyPurchase(string purchaseUuid, address walletAddress) public constant returns(bool){
		if( purchases[purchaseUuid].deviceWalletAddress == walletAddress ){
			return true;
		}
		return false;
	}


}
