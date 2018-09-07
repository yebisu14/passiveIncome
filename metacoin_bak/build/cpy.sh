var=`cat contracts/MetaCoin.json | jq -c .abi`
sed -i.bak -e "s/var abiArray = '.+'/var abiArray = '${var}'/g" index.html 


