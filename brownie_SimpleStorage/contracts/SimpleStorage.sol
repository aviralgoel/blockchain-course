// SPDX-License-Identifier: MIT

// This is the code for our smart contract
// To deploy this, we need to follow the following steps
// 1. compile the solidity code
// 2. dump the compiled code into a json file
// 3. fetch the bytecode and abi of the contract from the json into the python program
// 4. connect to the blockchain
// 5. using the fetched abi and bytecode create a Contract object in python
// 6. create, sign and then send a transaction to the blockchain to deploy the contract
// 7. get the transaction hash (hx)

pragma solidity ^0.6.0;

contract SimpleStorage {
    //this will get initialized as 0
    uint256 public favoriteNumber;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    //type visibility name
    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    People public person = People({favoriteNumber: 2, name: "Patrick"});

    function store(uint256 _favoriteNuber) public {
        favoriteNumber = _favoriteNuber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNuber) public {
        people.push(People(_favoriteNuber, _name));
        nameToFavoriteNumber[_name] = _favoriteNuber;
    }
}
