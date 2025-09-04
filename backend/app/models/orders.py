# backend/app/models/orders.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed" 
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class SalesChannel(str, Enum):
    """Sales channel enumeration"""
    ONLINE = "online"
    IN_STORE = "in_store"
    MOBILE_APP = "mobile_app"
    PHONE = "phone"
    SOCIAL_MEDIA = "social_media"

class PaymentStatus(str, Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    FAILED = "failed"
    REFUNDED = "refunded"

class ProductCategory(str, Enum):
    """Product category enumeration"""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME_GARDEN = "home_garden"
    SPORTS_OUTDOORS = "sports_outdoors"
    HEALTH_BEAUTY = "health_beauty"
    AUTOMOTIVE = "automotive"
    FOOD_BEVERAGE = "food_beverage"

class OrderItem(BaseModel):
    """Individual order item model"""
    product_id: str = Field(..., description="Unique product identifier")
    product_name: str = Field(..., min_length=1, max_length=200)
    sku: str = Field(..., description="Stock keeping unit")
    category: ProductCategory
    quantity: int = Field(..., gt=0, description="Quantity must be positive")
    unit_price: float = Field(..., gt=0, description="Unit price must be positive")
    total_price: float = Field(..., description="Total price for this item")
    discount_amount: float = Field(0.0, ge=0)
    tax_amount: float = Field(0.0, ge=0)
    
    @validator('total_price')
    def validate_total_price(cls, v, values):
        if 'quantity' in values and 'unit_price' in values:
            expected = values['quantity'] * values['unit_price']
            if abs(v - expected) > 0.01:  # Allow small floating point differences
                raise ValueError('Total price must equal quantity * unit_price')
        return v

class CustomerInfo(BaseModel):
    """Customer information model"""
    customer_id: str = Field(..., description="Unique customer identifier")
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s\-\(\)]+$')
    loyalty_tier: str = Field("standard", description="Customer loyalty tier")

class ShippingAddress(BaseModel):
    """Shipping address model"""
    street_address: str = Field(..., min_length=5, max_length=200)
    city: str = Field(..., min_length=2, max_length=50)
    state: str = Field(..., min_length=2, max_length=50)
    postal_code: str = Field(..., min_length=3, max_length=20)
    country: str = Field(..., min_length=2, max_length=50)
    is_default: bool = Field(False)

class PaymentInfo(BaseModel):
    """Payment information model"""
    payment_method: str = Field(..., description="Payment method used")
    payment_status: PaymentStatus
    transaction_id: str = Field(..., description="Transaction identifier")
    amount: float = Field(..., gt=0)
    currency: str = Field("USD", min_length=3, max_length=3)
    processed_at: Optional[datetime] = None

class Order(BaseModel):
    """Complete order model"""
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_number: str = Field(..., description="Human-readable order number")
    status: OrderStatus = OrderStatus.PENDING
    channel: SalesChannel
    
    # Customer and shipping
    customer: CustomerInfo
    shipping_address: ShippingAddress
    billing_address: Optional[ShippingAddress] = None
    
    # Order items
    items: List[OrderItem] = Field(..., min_items=1)
    
    # Financial information
    subtotal: float = Field(..., ge=0)
    tax_amount: float = Field(0.0, ge=0)
    shipping_cost: float = Field(0.0, ge=0)
    discount_amount: float = Field(0.0, ge=0)
    total_amount: float = Field(..., gt=0)
    
    # Payment
    payment: PaymentInfo
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    
    # Additional metadata
    notes: Optional[str] = Field(None, max_length=500)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('total_amount')
    def validate_total_amount(cls, v, values):
        if all(key in values for key in ['subtotal', 'tax_amount', 'shipping_cost', 'discount_amount']):
            expected = values['subtotal'] + values['tax_amount'] + values['shipping_cost'] - values['discount_amount']
            if abs(v - expected) > 0.01:
                raise ValueError('Total amount calculation is incorrect')
        return v

class OrderCreate(BaseModel):
    """Order creation model"""
    channel: SalesChannel
    customer: CustomerInfo
    shipping_address: ShippingAddress
    billing_address: Optional[ShippingAddress] = None
    items: List[OrderItem] = Field(..., min_items=1)
    payment_method: str
    notes: Optional[str] = None

class OrderUpdate(BaseModel):
    """Order update model"""
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class OrderFilter(BaseModel):
    """Order filtering model"""
    status: Optional[List[OrderStatus]] = None
    channel: Optional[List[SalesChannel]] = None
    customer_id: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_amount: Optional[float] = Field(None, ge=0)
    max_amount: Optional[float] = Field(None, ge=0)

class OrderSummary(BaseModel):
    """Order summary statistics model"""
    total_orders: int
    total_revenue: float
    orders_by_status: Dict[str, int]
    orders_by_channel: Dict[str, int]
    average_order_value: float
    top_products: List[Dict[str, Any]]

class ApiResponse(BaseModel):
    """Generic API response model"""
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class PaginatedResponse(BaseModel):
    """Paginated response model"""
    items: List[Any]
    total: int
    page: int = Field(..., ge=1)
    size: int = Field(..., ge=1, le=100)
    pages: int
    has_next: bool
    has_prev: bool