import click
from functools import wraps
from api_client import APIClient

def require_auth(f):
    """Decorator to require authentication for CLI commands"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        client = APIClient()
        if not client.token:
            click.echo("Error: Not logged in. Run 'auction-cli login' first.")
            return
        return f(*args, **kwargs)
    return wrapper

@click.command()
@click.option('--name', prompt='Name', help='User name')
@click.option('--email', prompt='Email', help='User email')
@click.option('--password', prompt='Password', hide_input=True, confirmation_prompt=True, help='User password')
@click.option('--role', prompt='Role', type=click.Choice(['customer', 'manager']), help='User role')
@click.pass_context
def register(ctx, name, email, password, role):
    """Register a new user"""
    client = APIClient()
    result = client.register(name, email, password, role)
    if result:
        click.echo(f"✅ User registered successfully!")
        click.echo(f"   Name: {name}")
        click.echo(f"   Email: {email}")
        click.echo(f"   Role: {role}")
    else:
        click.echo("❌ Registration failed. Please try again.")

def register_entry(standalone_mode=True):
    """Alternative entry point for register"""
    if standalone_mode:
        # When called from interactive mode, invoke the original command
        register.main(standalone_mode=False)

@click.command()
def logout():
    """Logout and clear stored credentials"""
    client = APIClient()
    client.logout()
    click.echo("✅ Logged out successfully!")
    click.echo("Token cleared from local storage.")

def logout_main(standalone_mode=True):
    """Alternative entry point for logout"""
    if standalone_mode:
        # When called from interactive mode, invoke the original command
        logout.main(standalone_mode=False)

@click.command()
def whoami():
    """Show current logged-in user"""
    client = APIClient()
    if not client.token:
        click.echo("Not logged in.")
        return
        
    user_info = client.get_current_user()
    if user_info:
        click.echo(f"📋 Current User:")
        click.echo(f"   Name: {user_info.get('name', 'Unknown')}")
        click.echo(f"   Email: {user_info.get('email', 'Unknown')}")
        click.echo(f"   Role: {user_info.get('role', 'Unknown')}")
    else:
        click.echo("❌ Unable to fetch user information.")

@click.command()
def login():
    """Login and store credentials"""
    email = click.prompt('Email')
    password = click.prompt('Password', hide_input=True)
    
    client = APIClient()
    token = client.login(email, password)
    if token:
        click.echo("✅ Logged in successfully!")
        click.echo(f"Token stored for future requests.")
    else:
        click.echo("❌ Login failed. Please check your credentials.")

def login_main(standalone_mode=True):
    """Alternative entry point for login"""
    if standalone_mode:
        # When called from interactive mode, invoke the original command
        login.main(standalone_mode=False)

def whoami_main(standalone_mode=True):
    """Alternative entry point for whoami"""
    if standalone_mode:
        # When called from interactive mode, invoke the original command
        whoami.main(standalone_mode=False)

def register_main(standalone_mode=True):
    """Alternative entry point for register"""
    if standalone_mode:
        # When called from interactive mode, invoke the original command
        register.main(standalone_mode=False)