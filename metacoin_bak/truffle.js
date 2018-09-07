var HDWalletProvider = require('truffle-hdwallet-provider');
var mnemonic = "fossil bronze around betray indoor pigeon usage priority valid sun effort number";
var endpoint = "https://ropsten.infura.io/v3/35d7622ec4464668b44f8313abfc09a9"


module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!

  networks:{
    development: {
    },
    ropsten: {
      provider: function() {
        return new HDWalletProvider(
          mnemonic,
          endpoint
        );
      },
      network_id: 3,
      gas: 500000
    }
  }
};
