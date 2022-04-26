// SPDX-License-Identifier: MIT
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
