from brownie import FundMe
from scripts.helpful_scripts import get_account


def deploy_simple_storage():
    # fetch the account details (private key)
    account = get_account()
    fundme = FundMe.deploy({"from": account})
    print(f"Contract Deployed to {fundme.address}")


def main():
    deploy_simple_storage()
