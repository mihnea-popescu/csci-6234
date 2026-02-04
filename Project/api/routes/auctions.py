from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db, Auction, User
from schemas import AuctionResponse, AuctionDetailResponse, AuctionCreate
import auth

router = APIRouter()

@router.get("/", response_model=List[AuctionResponse])
async def get_auctions(db: Session = Depends(get_db)):
    return (
        db.query(Auction)
        .options(joinedload(Auction.creator))
        .order_by(Auction.created_at.desc())
        .all()
    )

@router.get("/{auction_id}", response_model=AuctionDetailResponse)
async def get_auction(auction_id: int, db: Session = Depends(get_db)):
    # Placeholder: Get specific auction with items
    return {"id": auction_id, "name": "Sample Auction", "items": []}

@router.post("/", response_model=AuctionResponse)
async def create_auction(
    auction: AuctionCreate,
    current_user: User = Depends(auth.get_current_manager),
    db: Session = Depends(get_db),
):
    db_auction = Auction(
        name=auction.name,
        ended_at=auction.ended_at,
        created_by=current_user.id,
        status="active",
    )
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    db_auction.creator = current_user
    return db_auction

@router.put("/{auction_id}", response_model=AuctionResponse)
async def update_auction(auction_id: int, db: Session = Depends(get_db)):
    # Placeholder: Update auction details
    return {"id": auction_id, "name": "Updated Auction", "status": "active"}

@router.post("/{auction_id}/end", response_model=AuctionResponse)
async def end_auction(auction_id: int, db: Session = Depends(get_db)):
    # Placeholder: End auction and finalize sales
    return {"id": auction_id, "name": "Ended Auction", "status": "ended"}