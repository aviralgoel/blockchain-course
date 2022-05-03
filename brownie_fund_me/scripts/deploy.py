from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account


def deply_fund_me():
    account = get_account()
    if network.show_active() != "development":
        priceFeed_address = config["networks"][network.show.active()][
            "eth_usd_price_feed"
        ]

    else:
        print(f"The active network is {network.show_active()}")
        print("Deploying mocks...")
        mocks_aggregator = MockV3Aggregator.deploy(
            18, 2000000000000000000, {"from": account}
        )
        print("Mocks deployed")
        priceFeed_address = mocks_aggregator.address

        # fetch the account details (private key)

    fundme = FundMe.deploy(
        priceFeed_address,
        {"from": account},
        publish_source=True,
    )
    print(f"Contract Deployed to {fundme.address}")


def main():
    deply_fund_me()
