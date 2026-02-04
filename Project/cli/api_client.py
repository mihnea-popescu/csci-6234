import requests
import json
from typing import Dict, List, Any

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make HTTP request to API"""
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
            
        if data:
            headers["Content-Type"] = "application/json"
            
        # Placeholder: Implement actual HTTP requests
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
        return response.json()
    
    # Authentication methods
    def register(self, name: str, email: str, password: str, role: str) -> Dict:
        """Register new user"""
        data = {"name": name, "email": email, "password": password, "role": role}
        return self._make_request("POST", "/auth/register", data)
    
    def login(self, email: str, password: str) -> Dict:
        """Login user"""
        data = {"email": email, "password": password}
        response = self._make_request("POST", "/auth/login", data)
        self.token = response.get("access_token")
        return response
    
    # Auction methods
    def get_auctions(self) -> List[Dict]:
        """Get all auctions"""
        return self._make_request("GET", "/auctions/")
    
    def get_auction(self, auction_id: int) -> Dict:
        """Get specific auction"""
        return self._make_request("GET", f"/auctions/{auction_id}")
    
    def create_auction(self, name: str) -> Dict:
        """Create new auction"""
        data = {"name": name}
        return self._make_request("POST", "/managers/auctions", data)
    
    def end_auction(self, auction_id: int) -> Dict:
        """End auction"""
        return self._make_request("POST", f"/managers/auctions/{auction_id}/end")
    
    # Item methods
    def add_item(self, auction_id: int, name: str, opening_price: float) -> Dict:
        """Add item to auction"""
        data = {"name": name, "opening_price": opening_price, "auction_id": auction_id}
        return self._make_request("POST", f"/managers/auctions/{auction_id}/items", data)
    
    # Bid methods
    def place_bid(self, item_id: int, amount: float) -> Dict:
        """Place bid on item"""
        data = {"item_id": item_id, "amount": amount}
        return self._make_request("POST", "/customers/bid", data)
    
    def get_user_bids(self) -> List[Dict]:
        """Get current user's bids"""
        return self._make_request("GET", "/customers/bids")