pragma solidity ^0.4.18;

import "./ConvertLib.sol";

// This is just a simple example of a coin-like contract.
// It is not standards compatible and cannot be expected to talk to other
// coin/token contracts. If you want to create a standards-compliant
// token, see: https://github.com/ConsenSys/Tokens. Cheers!

contract MetaCoin {
	
	mapping (address => uint) balances;
	event Transfer(address indexed _from, address indexed _to, uint256 _value);

	function sendCoin(address receiver, uint amount) public returns(bool sufficient){
		if( balances[msg.sender] < amount ) return false;
		balances[msg.sender] -= amount;
		balances[receiver] += amount;
		Transfer(msg.sender, receiver, amount);
		return true;
	}

	function getBalance(address addr) public view returns(uint){
		return balances[addr];
	}


	//	コントラクトを作成したアカウントのアドレス
	address owner;

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
		コンストラクタ
	*/
	function MetaCoin() public {
		owner = msg.sender;
		
	}

	/*
		コントラクトの作成者のみが使用できることを意味する修飾子
	*/
	modifier onlyOwner{
		require(msg.sender == owner);
		_;
	}

	/*
		購入履歴を追加
	*/
	function addPurchase(string purchaseUuid, address deviceWalletAddress) public {
		purchases[purchaseUuid].deviceWalletAddress = deviceWalletAddress;
	}

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
