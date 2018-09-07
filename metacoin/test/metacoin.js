var MetaCoin = artifacts.require("./MetaCoin.sol");

contract('MetaCoin', function(accounts) {
  
  /*
    現在のブロードキャスト状態の登録をチェックします
    アカウント1~6で適当にUUID振って、それを基準に登録していきます.
  */
  it("check status registration", ()=>{
    return MetaCoin.deployed().then((instance)=>{
      return instance.setBroadcastStatus.call(true);
    }).then(()=>{
    });
  });

  /*
    ブロードキャスト状態の取得をチェックします
  */
  it("check status fetching", ()=>{
    return MetaCoin.deployed().then((instance)=>{
      return instance.getBroadcastStatus.call(account[1]);
    });
  });
  


});
