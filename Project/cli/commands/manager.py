import click
from api_client import APIClient

@click.command()
@click.argument('name')
def create_auction(name):
    """Create a new auction"""
    # Placeholder: Call API to create auction
    client = APIClient()
    result = client.create_auction(name)
    click.echo(f"Auction created: {result}")

@click.command()
@click.argument('auction_id')
@click.argument('name')
@click.argument('opening_price', type=float)
def add_item(auction_id, name, opening_price):
    """Add item to auction"""
    # Placeholder: Call API to add item
    client = APIClient()
    result = client.add_item(auction_id, name, opening_price)
    click.echo(f"Item added: {result}")

@click.command()
@click.argument('auction_id')
def end_auction(auction_id):
    """End an auction and process results"""
    # Placeholder: Call API to end auction
    client = APIClient()
    result = client.end_auction(auction_id)
    click.echo(f"Auction ended: {result}")