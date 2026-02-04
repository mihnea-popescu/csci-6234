import click
from commands.auth import register, login
from commands.customer import list_auctions, view_auction, place_bid, my_bids
from commands.manager import create_auction, add_item, end_auction

@click.group()
def cli():
    """Auction House CLI Application"""
    pass

# Authentication commands
cli.add_command(register)
cli.add_command(login)

# Customer commands
cli.add_command(list_auctions)
cli.add_command(view_auction)
cli.add_command(place_bid)
cli.add_command(my_bids)

# Manager commands
cli.add_command(create_auction)
cli.add_command(add_item)
cli.add_command(end_auction)

if __name__ == "__main__":
    cli()