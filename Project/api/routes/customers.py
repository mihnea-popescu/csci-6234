from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from database import get_db, User, Auction, AuctionItem, Bid
from schemas import BidResponse, AuctionResponse
from services.auction import ensure_auction_closed_if_ended
import auth

router = APIRouter()

@router.get("/auctions/active", response_model=List[AuctionResponse])
async def list_active_auctions(
    current_user: User = Depends(auth.get_current_customer),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Auction)
        .options(joinedload(Auction.creator))
        .filter(Auction.status == "active")
        .order_by(Auction.created_at.desc())
    )
    auctions = query.all()
    for a in auctions:
        ensure_auction_closed_if_ended(db, a)
    return [a for a in auctions if a.status == "active"]

@router.get("/auctions/mine", response_model=List[AuctionResponse])
async def get_my_auctions(
    current_user: User = Depends(auth.get_current_customer),
    db: Session = Depends(get_db),
):
    subq = db.query(Bid.item_id).filter(Bid.bidder_id == current_user.id).distinct()
    auction_ids = (
        db.query(AuctionItem.auction_id)
        .filter(AuctionItem.id.in_(subq))
        .distinct()
        .all()
    )
    aid_list = [r[0] for r in auction_ids]
    if not aid_list:
        return []
    query = (
        db.query(Auction)
        .options(joinedload(Auction.creator))
        .filter(Auction.id.in_(aid_list))
        .order_by(Auction.created_at.desc())
    )
    auctions = query.all()
    for a in auctions:
        ensure_auction_closed_if_ended(db, a)
    return auctions

@router.get("/auctions", response_model=List[AuctionResponse])
async def get_auctions(
    current_user: User = Depends(auth.get_current_customer),
    db: Session = Depends(get_db),
    status_filter: Optional[str] = Query(None, alias="status"),
):
    query = (
        db.query(Auction)
        .options(joinedload(Auction.creator))
        .order_by(Auction.created_at.desc())
    )
    if status_filter and status_filter in ("active", "ended", "cancelled"):
        query = query.filter(Auction.status == status_filter)
    auctions = query.all()
    for a in auctions:
        ensure_auction_closed_if_ended(db, a)
    return auctions

@router.get("/bids", response_model=List[BidResponse])
async def get_user_bids(
    current_user: User = Depends(auth.get_current_customer),
    db: Session = Depends(get_db),
):
    bids = (
        db.query(Bid)
        .options(
            joinedload(Bid.item).joinedload(AuctionItem.auction).joinedload(Auction.creator),
            joinedload(Bid.bidder),
        )
        .filter(Bid.bidder_id == current_user.id)
        .order_by(Bid.created_at.desc())
        .all()
    )
    return bids