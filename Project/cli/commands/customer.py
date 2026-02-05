import click
from commands.auth import require_auth
from api_client import APIClient

def main(standalone_mode=True):
    """Alternative entry point for standalone mode"""
    if standalone_mode:
        # When called from interactive mode, invoke the original command
        pass  # Will be handled by calling the decorated function directly

@click.command()
def list_auctions():
    """List all active auctions"""
    client = APIClient()
    auctions = client.get_auctions()
    if auctions:
        click.echo("🏛️  Active Auctions:")
        for auction in auctions:
            click.echo(f"   📋 {auction['name']} (ID: {auction['id']})")
    else:
        click.echo("No active auctions found.")

@click.command()
@click.argument('auction_id')
def view_auction(auction_id):
    """View auction details"""
    client = APIClient()
    auction = client.get_auction(auction_id)
    if auction and 'id' in auction:
        click.echo(f"🏛️  Auction Details:")
        click.echo(f"   ID: {auction['id']}")
        click.echo(f"   Name: {auction['name']}")
        click.echo(f"   Status: {auction['status']}")
        click.echo(f"   Created: {auction.get('created_at', 'Unknown')}")
        if 'items' in auction and auction['items']:
            click.echo(f"   Items: {len(auction['items'])}")
            for item in auction['items']:
                click.echo(f"     🎯 {item['name']} - ${item.get('current_bid', 0)}")
    else:
        click.echo(f"❌ Auction not found with ID: {auction_id}")

@click.command()
@click.argument('item_id')
@click.argument('amount', type=float)
@require_auth
def place_bid(item_id, amount):
    """Place a bid on an item"""
    client = APIClient()
    result = client.place_bid(item_id, amount)
    if result and 'id' in result:
        click.echo(f"✅ Bid placed successfully!")
        click.echo(f"   Bid ID: {result['id']}")
        click.echo(f"   Item ID: {result['item_id']}")
        click.echo(f"   Amount: ${result['amount']}")
    else:
        click.echo("❌ Failed to place bid.")

@click.command()
@require_auth
def my_bids():
    """View user's bidding history"""
    client = APIClient()
    bids = client.get_user_bids()
    if bids:
        click.echo("💰 Your Bids:")
        for bid in bids:
            click.echo(f"   🎯 Item {bid['item_id']}: ${bid['amount']}")
    else:
        click.echo("No bids found.")