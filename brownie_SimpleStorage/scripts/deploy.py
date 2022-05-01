from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    # fetch the account details (private key)
    account = get_account()
    # use that account to create, sign, send a deploy the transaction on the blockchain
    simple_storage = SimpleStorage.deploy({"from": account})
    # call a function (view)
    stored_value = simple_storage.retrieve()
    print(stored_value)
    # make a state change on the blockchain
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
