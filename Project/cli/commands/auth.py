import click
from api_client import APIClient

@click.command()
@click.option('--name', prompt='Name', help='User name')
@click.option('--email', prompt='Email', help='User email')
@click.option('--password', prompt='Password', hide_input=True, confirmation_prompt=True, help='User password')
@click.option('--role', prompt='Role', type=click.Choice(['customer', 'manager']), help='User role')
def register(name, email, password, role):
    """Register a new user"""
    # Placeholder: Call API to register user
    client = APIClient()
    result = client.register(name, email, password, role)
    click.echo(f"User registered: {result}")

@click.command()
@click.option('--email', prompt='Email', help='User email')
@click.option('--password', prompt='Password', hide_input=True, help='User password')
def login(email, password):
    """Login to user account"""
    # Placeholder: Call API to login
    client = APIClient()
    result = client.login(email, password)
    click.echo(f"Login successful: {result}")