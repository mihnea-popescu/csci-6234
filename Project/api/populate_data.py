#!/usr/bin/env python3
"""
Populate auction house database with realistic dummy data
Bids table will remain empty for fresh auction start
"""

import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Add the API directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, User, Auction, AuctionItem, Bid

def populate_database():
    """Populate database with realistic auction house data"""
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Bid).delete()
        db.query(AuctionItem).delete()
        db.query(Auction).delete()
        db.query(User).delete()
        db.commit()
        
        print("🧹 Cleared existing data...")
        
        # Create Users
        managers = create_managers(db)
        customers = create_customers(db)
        print(f"👥 Created {len(managers)} managers and {len(customers)} customers")
        
        # Create Auctions
        active_auctions, ended_auctions = create_auctions(db, managers)
        print(f"🎪 Created {len(active_auctions)} active and {len(ended_auctions)} ended auctions")
        
        # Create Auction Items
        create_auction_items(db, active_auctions, ended_auctions)
        print(f"🎯 Created auction items (bids table kept empty)")
        
        db.commit()
        print("✅ Database populated successfully with realistic data!")
        
        # Print summary
        print_database_summary(db)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error populating database: {e}")
        raise
    finally:
        db.close()

def create_managers(db):
    """Create manager users"""
    managers_data = [
        {
            "name": "Margaret Hammond",
            "email": "margaret@hammond-gallery.com",
            "password": "hashed_password_manager_1",
            "role": "manager"
        },
        {
            "name": "James Chen", 
            "email": "james@chen-heritage.com",
            "password": "hashed_password_manager_2",
            "role": "manager"
        }
    ]
    
    managers = []
    for data in managers_data:
        manager = User(**data)
        db.add(manager)
        managers.append(manager)
    
    db.commit()
    return managers

def create_customers(db):
    """Create customer users"""
    customers_data = [
        {
            "name": "Alexandra Reynolds",
            "email": "alexandra.reynolds@email.com", 
            "password": "hashed_password_customer_1",
            "role": "customer"
        },
        {
            "name": "Marcus Williams",
            "email": "marcus.williams@email.com",
            "password": "hashed_password_customer_2", 
            "role": "customer"
        },
        {
            "name": "Sarah Chen",
            "email": "sarah.chen@email.com",
            "password": "hashed_password_customer_3",
            "role": "customer"
        },
        {
            "name": "David Martinez",
            "email": "david.martinez@email.com",
            "password": "hashed_password_customer_4",
            "role": "customer"
        },
        {
            "name": "Emily Thompson",
            "email": "emily.thompson@email.com",
            "password": "hashed_password_customer_5",
            "role": "customer"
        }
    ]
    
    customers = []
    for data in customers_data:
        customer = User(**data)
        db.add(customer)
        customers.append(customer)
    
    db.commit()
    return customers

def create_auctions(db, managers):
    """Create auctions"""
    now = datetime.utcnow()
    
    # Active auctions
    active_auctions_data = [
        {
            "name": "Spring Modern Art Collection",
            "created_by": managers[0].id,  # Margaret Hammond
            "created_at": now - timedelta(weeks=3),
            "ended_at": None,
            "status": "active"
        },
        {
            "name": "Vintage Photography & Prints", 
            "created_by": managers[1].id,  # James Chen
            "created_at": now - timedelta(weeks=1),
            "ended_at": None,
            "status": "active"
        },
        {
            "name": "Luxury Timepieces",
            "created_by": managers[0].id,  # Margaret Hammond
            "created_at": now - timedelta(weeks=2, days=5),
            "ended_at": now + timedelta(days=2),
            "status": "active"
        }
    ]
    
    # Ended auctions
    ended_auctions_data = [
        {
            "name": "Winter Antiques Showcase",
            "created_by": managers[1].id,  # James Chen
            "created_at": now - timedelta(weeks=6),
            "ended_at": now - timedelta(days=5),
            "status": "ended"
        },
        {
            "name": "Contemporary Sculptures",
            "created_by": managers[0].id,  # Margaret Hammond  
            "created_at": now - timedelta(weeks=4),
            "ended_at": now - timedelta(weeks=2),
            "status": "ended"
        }
    ]
    
    all_auctions = []
    
    for data in active_auctions_data:
        auction = Auction(**data)
        db.add(auction)
        all_auctions.append(auction)
    
    for data in ended_auctions_data:
        auction = Auction(**data)
        db.add(auction)
        all_auctions.append(auction)
    
    db.commit()
    
    active_auctions = all_auctions[:3]
    ended_auctions = all_auctions[3:]
    
    return active_auctions, ended_auctions

def create_auction_items(db, active_auctions, ended_auctions):
    """Create auction items with realistic data"""
    
    # Spring Modern Art Collection items (8 items)
    modern_art_items = [
        {"name": "Urban Sunrise Abstract", "opening_price": Decimal("1200.00")},
        {"name": "Geometric Dreams Canvas", "opening_price": Decimal("800.00")},
        {"name": "Color Study #7", "opening_price": Decimal("650.00")},
        {"name": "Minimalist Landscape", "opening_price": Decimal("450.00")},
        {"name": "Emotional Abstract", "opening_price": Decimal("900.00")},
        {"name": "Modern Sculpture Piece", "opening_price": Decimal("2200.00")},
        {"name": "Digital Art Print", "opening_price": Decimal("350.00")},
        {"name": "Watercolor Series", "opening_price": Decimal("550.00")}
    ]
    
    # Vintage Photography & Prints items (6 items)  
    photography_items = [
        {"name": "1940s Cityscape Black & White", "opening_price": Decimal("800.00")},
        {"name": "Portrait Series 1965", "opening_price": Decimal("600.00")},
        {"name": "Landscape Collection 3 prints", "opening_price": Decimal("450.00")},
        {"name": "Street Photography NYC", "opening_price": Decimal("350.00")},
        {"name": "Architectural Studies", "opening_price": Decimal("275.00")},
        {"name": "Vintage Camera Collection", "opening_price": Decimal("950.00")}
    ]
    
    # Luxury Timepieces items (2 items)
    timepiece_items = [
        {"name": "Omega Speedmaster Professional", "opening_price": Decimal("4500.00")},
        {"name": "Vintage Longines Watch", "opening_price": Decimal("1800.00")}
    ]
    
    # Winter Antiques Showcase items (2 items - ended)
    antiques_items = [
        {"name": "Victorian Writing Desk", "opening_price": Decimal("800.00")},
        {"name": "Antique Clock Collection", "opening_price": Decimal("1200.00")}
    ]
    
    # Contemporary Sculptures items (2 items - ended)
    sculpture_items = [
        {"name": "Bronze Abstract Sculpture", "opening_price": Decimal("3200.00")},
        {"name": "Metal Wire Art Piece", "opening_price": Decimal("950.00")}
    ]
    
    # Create items for each auction
    for item_data in modern_art_items:
        item = AuctionItem(
            auction_id=active_auctions[0].id,  # Spring Modern Art Collection
            **item_data,
            current_bid=item_data["opening_price"],
            closing_price=Decimal("0.00") if active_auctions[0].status == "active" else None
        )
        db.add(item)
    
    for item_data in photography_items:
        item = AuctionItem(
            auction_id=active_auctions[1].id,  # Vintage Photography & Prints
            **item_data,
            current_bid=item_data["opening_price"],
            closing_price=Decimal("0.00") if active_auctions[1].status == "active" else None
        )
        db.add(item)
    
    for item_data in timepiece_items:
        item = AuctionItem(
            auction_id=active_auctions[2].id,  # Luxury Timepieces
            **item_data,
            current_bid=item_data["opening_price"],
            closing_price=Decimal("0.00") if active_auctions[2].status == "active" else None
        )
        db.add(item)
    
    for item_data in antiques_items:
        item = AuctionItem(
            auction_id=ended_auctions[0].id,  # Winter Antiques Showcase
            **item_data,
            current_bid=item_data["opening_price"],
            closing_price=Decimal("0.00")  # No bids, so no closing price
        )
        db.add(item)
    
    for item_data in sculpture_items:
        item = AuctionItem(
            auction_id=ended_auctions[1].id,  # Contemporary Sculptures
            **item_data,
            current_bid=item_data["opening_price"],
            closing_price=Decimal("0.00")  # No bids, so no closing price
        )
        db.add(item)
    
    db.commit()

def print_database_summary(db):
    """Print summary of created data"""
    print("\n📊 Database Summary:")
    print(f"   Users: {db.query(User).count()}")
    print(f"   Managers: {db.query(User).filter(User.role == 'manager').count()}")
    print(f"   Customers: {db.query(User).filter(User.role == 'customer').count()}")
    print(f"   Auctions: {db.query(Auction).count()}")
    print(f"   Active Auctions: {db.query(Auction).filter(Auction.status == 'active').count()}")
    print(f"   Ended Auctions: {db.query(Auction).filter(Auction.status == 'ended').count()}")
    print(f"   Auction Items: {db.query(AuctionItem).count()}")
    print(f"   Bids: {db.query(Bid).count()} (intentionally empty)")
    
    print("\n🎪 Active Auctions:")
    active_auctions = db.query(Auction).filter(Auction.status == 'active').all()
    for auction in active_auctions:
        item_count = db.query(AuctionItem).filter(AuctionItem.auction_id == auction.id).count()
        print(f"   - {auction.name} ({item_count} items)")
    
    print("\n⏰ Ended Auctions:")
    ended_auctions = db.query(Auction).filter(Auction.status == 'ended').all()
    for auction in ended_auctions:
        item_count = db.query(AuctionItem).filter(AuctionItem.auction_id == auction.id).count()
        print(f"   - {auction.name} ({item_count} items)")

if __name__ == "__main__":
    populate_database()