# backend/app/routers/orders.py
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from app.models.orders import (
    Order, OrderCreate, OrderUpdate, OrderFilter, OrderSummary, 
    ApiResponse, PaginatedResponse, OrderStatus, SalesChannel
)
from app.services.order_service import OrderService

logger = logging.getLogger(__name__)
router = APIRouter()

# Dependency to get order service
def get_order_service() -> OrderService:
    return OrderService()

@router.get("/", response_model=PaginatedResponse)
async def get_orders(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    status: Optional[List[OrderStatus]] = Query(None, description="Filter by order status"),
    channel: Optional[List[SalesChannel]] = Query(None, description="Filter by sales channel"),
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    date_from: Optional[datetime] = Query(None, description="Filter from date"),
    date_to: Optional[datetime] = Query(None, description="Filter to date"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum order amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum order amount"),
    search: Optional[str] = Query(None, description="Search in order details"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    order_service: OrderService = Depends(get_order_service)
):
    """
    Retrieve orders with advanced filtering, pagination and search
    
    ### Features:
    - **Pagination**: Efficient pagination with configurable page sizes
    - **Filtering**: Multiple filter options by status, channel, dates, amounts
    - **Search**: Full-text search across order details
    - **Sorting**: Flexible sorting by various fields
    """
    try:
        filters = OrderFilter(
            status=status,
            channel=channel, 
            customer_id=customer_id,
            date_from=date_from,
            date_to=date_to,
            min_amount=min_amount,
            max_amount=max_amount
        )
        
        result = await order_service.get_orders_paginated(
            filters=filters,
            page=page,
            size=size,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        logger.info(f"Retrieved {len(result.items)} orders (page {page})")
        return result
        
    except Exception as e:
        logger.error(f"Error retrieving orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve orders")

@router.get("/summary", response_model=OrderSummary)
async def get_orders_summary(
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    order_service: OrderService = Depends(get_order_service)
):
    """
    Get comprehensive order statistics and analytics
    
    Returns key business metrics including:
    - Total orders and revenue
    - Orders breakdown by status and channel
    - Average order value
    - Top performing products
    """
    try:
        summary = await order_service.get_order_summary(date_from, date_to)
        logger.info("Generated order summary")
        return summary
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate summary")

@router.get("/{order_id}", response_model=Order)
async def get_order_by_id(
    order_id: str,
    include_customer_history: bool = Query(False, description="Include customer order history"),
    order_service: OrderService = Depends(get_order_service)
):
    """
    Retrieve a specific order by ID with optional customer history
    """
    try:
        order = await order_service.get_order_by_id(order_id, include_customer_history)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        logger.info(f"Retrieved order {order_id}")
        return order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve order")

@router.post("/", response_model=ApiResponse)
async def create_order(
    order_data: OrderCreate,
    background_tasks: BackgroundTasks,
    validate_inventory: bool = Query(True, description="Validate inventory availability"),
    send_confirmation: bool = Query(True, description="Send order confirmation email"),
    order_service: OrderService = Depends(get_order_service)
):
    """
    Create a new order with comprehensive validation and background processing
    
    ### Features:
    - **Inventory Validation**: Real-time inventory checking
    - **Payment Processing**: Secure payment authorization
    - **Notifications**: Automated customer communications
    - **Analytics**: Order creation tracking
    """
    try:
        order = await order_service.create_order(
            order_data, 
            validate_inventory=validate_inventory
        )
        
        # Background tasks
        if send_confirmation:
            background_tasks.add_task(
                order_service.send_order_confirmation, 
                order.order_id
            )
        
        background_tasks.add_task(
            order_service.update_analytics, 
            order.order_id
        )
        
        logger.info(f"Created order {order.order_id}")
        
        return ApiResponse(
            message="Order created successfully",
            data={"order_id": order.order_id, "order_number": order.order_number}
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create order")

@router.put("/{order_id}", response_model=ApiResponse)
async def update_order(
    order_id: str,
    order_update: OrderUpdate,
    background_tasks: BackgroundTasks,
    order_service: OrderService = Depends(get_order_service)
):
    """Update an existing order status and metadata"""
    try:
        updated_order = await order_service.update_order(order_id, order_update)
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Background task for notifications
        background_tasks.add_task(
            order_service.notify_order_update,
            order_id, 
            order_update.status
        )
        
        logger.info(f"Updated order {order_id}")
        return ApiResponse(
            message="Order updated successfully",
            data={"order_id": order_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update order")

@router.delete("/{order_id}", response_model=ApiResponse)
async def cancel_order(
    order_id: str,
    reason: str = Query(..., description="Cancellation reason"),
    refund: bool = Query(True, description="Process refund"),
    order_service: OrderService = Depends(get_order_service)
):
    """Cancel an order with optional refund processing"""
    try:
        result = await order_service.cancel_order(order_id, reason, refund)
        if not result:
            raise HTTPException(status_code=404, detail="Order not found")
        
        logger.info(f"Cancelled order {order_id}")
        return ApiResponse(
            message="Order cancelled successfully",
            data={"order_id": order_id, "refund_processed": refund}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel order")

@router.get("/analytics/trends", response_model=Dict[str, Any])
async def get_order_trends(
    period: str = Query("30d", regex="^(7d|30d|90d|1y)$"),
    granularity: str = Query("day", regex="^(hour|day|week|month)$"),
    order_service: OrderService = Depends(get_order_service)
):
    """Get order trends and analytics over specified time periods"""
    try:
        trends = await order_service.get_order_trends(period, granularity)
        logger.info(f"Generated trends for {period}")
        return trends
    except Exception as e:
        logger.error(f"Error generating trends: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate trends")