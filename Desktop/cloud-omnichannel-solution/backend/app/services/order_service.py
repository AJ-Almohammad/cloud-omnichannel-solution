# backend/app/services/order_service.py
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio
import logging
import random
import uuid
from math import ceil

from app.models.orders import (
    Order, OrderCreate, OrderUpdate, OrderFilter, OrderSummary,
    PaginatedResponse, OrderStatus, SalesChannel, ProductCategory,
    OrderItem, CustomerInfo, ShippingAddress, PaymentInfo, PaymentStatus
)

logger = logging.getLogger(__name__)

class OrderService:
    """Advanced order service with comprehensive business logic"""
    
    def __init__(self):
        # In-memory data storage for demo (replace with actual database)
        self._orders: List[Order] = []
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize sample orders for demonstration"""
        sample_orders = [
            self._create_sample_order("ORD-2024-001", SalesChannel.ONLINE, OrderStatus.DELIVERED),
            self._create_sample_order("ORD-2024-002", SalesChannel.IN_STORE, OrderStatus.PROCESSING),
            self._create_sample_order("ORD-2024-003", SalesChannel.MOBILE_APP, OrderStatus.SHIPPED),
            self._create_sample_order("ORD-2024-004", SalesChannel.ONLINE, OrderStatus.CONFIRMED),
            self._create_sample_order("ORD-2024-005", SalesChannel.PHONE, OrderStatus.PENDING),
            self._create_sample_order("ORD-2024-006", SalesChannel.SOCIAL_MEDIA, OrderStatus.DELIVERED),
            self._create_sample_order("ORD-2024-007", SalesChannel.ONLINE, OrderStatus.CANCELLED),
            self._create_sample_order("ORD-2024-008", SalesChannel.MOBILE_APP, OrderStatus.DELIVERED),
        ]
        self._orders.extend(sample_orders)
        logger.info(f"Initialized {len(sample_orders)} sample orders")
    
    def _create_sample_order(self, order_number: str, channel: SalesChannel, status: OrderStatus) -> Order:
        """Create a sample order for demonstration"""
        order_id = str(uuid.uuid4())
        created_at = datetime.utcnow() - timedelta(days=random.randint(1, 90))
        
        # Sample products
        products = [
            {"name": "AWS Cloud Architecture Book", "price": 45.99, "category": ProductCategory.BOOKS},
            {"name": "Wireless Bluetooth Headphones", "price": 129.99, "category": ProductCategory.ELECTRONICS},
            {"name": "Professional Laptop Stand", "price": 79.99, "category": ProductCategory.ELECTRONICS},
            {"name": "Cotton Polo Shirt", "price": 29.99, "category": ProductCategory.CLOTHING},
            {"name": "Ergonomic Office Chair", "price": 299.99, "category": ProductCategory.HOME_GARDEN},
            {"name": "Vitamin D Supplements", "price": 19.99, "category": ProductCategory.HEALTH_BEAUTY},
        ]
        
        # Random items for this order
        num_items = random.randint(1, 3)
        selected_products = random.sample(products, num_items)
        
        items = []
        subtotal = 0
        for i, product in enumerate(selected_products):
            quantity = random.randint(1, 3)
            unit_price = product["price"]
            total_price = quantity * unit_price
            subtotal += total_price
            
            items.append(OrderItem(
                product_id=f"PROD-{i+1:03d}",
                product_name=product["name"],
                sku=f"SKU-{random.randint(10000, 99999)}",
                category=product["category"],
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                discount_amount=0.0,
                tax_amount=round(total_price * 0.08, 2)  # 8% tax
            ))
        
        # Calculate totals
        tax_amount = round(subtotal * 0.08, 2)
        shipping_cost = 9.99 if subtotal < 50 else 0.0
        total_amount = subtotal + tax_amount + shipping_cost
        
        # Sample customer data
        customers = [
            {"first": "Alice", "last": "Johnson", "email": "alice.johnson@email.com"},
            {"first": "Bob", "last": "Smith", "email": "bob.smith@email.com"},
            {"first": "Carol", "last": "Williams", "email": "carol.williams@email.com"},
            {"first": "David", "last": "Brown", "email": "david.brown@email.com"},
            {"first": "Emma", "last": "Davis", "email": "emma.davis@email.com"},
        ]
        
        customer_data = random.choice(customers)
        customer = CustomerInfo(
            customer_id=f"CUST-{random.randint(1000, 9999)}",
            first_name=customer_data["first"],
            last_name=customer_data["last"],
            email=customer_data["email"],
            phone=f"+49-{random.randint(100, 999)}-{random.randint(1000000, 9999999)}",
            loyalty_tier=random.choice(["standard", "silver", "gold", "platinum"])
        )
        
        # Sample addresses
        addresses = [
            {"street": "123 Tech Street", "city": "Berlin", "state": "Berlin", "postal": "10115"},
            {"street": "456 Innovation Ave", "city": "Munich", "state": "Bavaria", "postal": "80331"},
            {"street": "789 Digital Boulevard", "city": "Hamburg", "state": "Hamburg", "postal": "20095"},
            {"street": "321 Cloud Lane", "city": "Frankfurt", "state": "Hesse", "postal": "60311"},
        ]
        
        address_data = random.choice(addresses)
        shipping_address = ShippingAddress(
            street_address=address_data["street"],
            city=address_data["city"],
            state=address_data["state"],
            postal_code=address_data["postal"],
            country="Germany",
            is_default=True
        )
        
        # Payment information
        payment = PaymentInfo(
            payment_method=random.choice(["credit_card", "paypal", "bank_transfer", "apple_pay"]),
            payment_status=PaymentStatus.CAPTURED if status in [OrderStatus.DELIVERED, OrderStatus.SHIPPED] else PaymentStatus.AUTHORIZED,
            transaction_id=f"TXN-{random.randint(100000, 999999)}",
            amount=total_amount,
            currency="EUR",
            processed_at=created_at + timedelta(minutes=random.randint(1, 30))
        )
        
        # Create order
        order = Order(
            order_id=order_id,
            order_number=order_number,
            status=status,
            channel=channel,
            customer=customer,
            shipping_address=shipping_address,
            items=items,
            subtotal=subtotal,
            tax_amount=tax_amount,
            shipping_cost=shipping_cost,
            discount_amount=0.0,
            total_amount=total_amount,
            payment=payment,
            created_at=created_at,
            updated_at=created_at,
            notes=f"Sample order created via {channel.value}",
            metadata={"sample": True, "demo_order": True}
        )
        
        return order
    
    async def get_orders_paginated(
        self,
        filters: OrderFilter,
        page: int = 1,
        size: int = 20,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> PaginatedResponse:
        """Get paginated orders with filtering and search"""
        
        # Apply filters
        filtered_orders = self._apply_filters(self._orders, filters)
        
        # Apply search
        if search:
            filtered_orders = self._apply_search(filtered_orders, search)
        
        # Apply sorting
        filtered_orders = self._apply_sorting(filtered_orders, sort_by, sort_order)
        
        # Calculate pagination
        total = len(filtered_orders)
        pages = ceil(total / size)
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        
        items = filtered_orders[start_idx:end_idx]
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )
    
    def _apply_filters(self, orders: List[Order], filters: OrderFilter) -> List[Order]:
        """Apply filters to order list"""
        filtered = orders
        
        if filters.status:
            filtered = [o for o in filtered if o.status in filters.status]
        
        if filters.channel:
            filtered = [o for o in filtered if o.channel in filters.channel]
        
        if filters.customer_id:
            filtered = [o for o in filtered if o.customer.customer_id == filters.customer_id]
        
        if filters.date_from:
            filtered = [o for o in filtered if o.created_at >= filters.date_from]
        
        if filters.date_to:
            filtered = [o for o in filtered if o.created_at <= filters.date_to]
        
        if filters.min_amount:
            filtered = [o for o in filtered if o.total_amount >= filters.min_amount]
        
        if filters.max_amount:
            filtered = [o for o in filtered if o.total_amount <= filters.max_amount]
        
        return filtered
    
    def _apply_search(self, orders: List[Order], search: str) -> List[Order]:
        """Apply search across order fields"""
        search_lower = search.lower()
        results = []
        
        for order in orders:
            # Search in order number, customer name, email, product names
            search_fields = [
                order.order_number,
                f"{order.customer.first_name} {order.customer.last_name}",
                order.customer.email,
                *[item.product_name for item in order.items],
                order.notes or ""
            ]
            
            if any(search_lower in field.lower() for field in search_fields):
                results.append(order)
        
        return results
    
    def _apply_sorting(self, orders: List[Order], sort_by: str, sort_order: str) -> List[Order]:
        """Apply sorting to order list"""
        reverse = sort_order == "desc"
        
        sort_functions = {
            "created_at": lambda o: o.created_at,
            "updated_at": lambda o: o.updated_at,
            "total_amount": lambda o: o.total_amount,
            "customer_name": lambda o: f"{o.customer.first_name} {o.customer.last_name}",
            "status": lambda o: o.status.value,
            "channel": lambda o: o.channel.value
        }
        
        if sort_by in sort_functions:
            return sorted(orders, key=sort_functions[sort_by], reverse=reverse)
        
        return orders
    
    async def get_order_by_id(self, order_id: str, include_history: bool = False) -> Optional[Order]:
        """Get order by ID with optional customer history"""
        for order in self._orders:
            if order.order_id == order_id:
                if include_history:
                    # Add customer order history to metadata
                    customer_orders = [
                        o.order_id for o in self._orders 
                        if o.customer.customer_id == order.customer.customer_id
                    ]
                    order.metadata["customer_order_history"] = customer_orders
                return order
        return None
    
    async def create_order(self, order_data: OrderCreate, validate_inventory: bool = True) -> Order:
        """Create a new order with validation"""
        
        # Validate inventory if requested
        if validate_inventory:
            await self._validate_inventory(order_data.items)
        
        # Generate order ID and number
        order_id = str(uuid.uuid4())
        order_number = f"ORD-{datetime.now().year}-{len(self._orders) + 1:03d}"
        
        # Calculate totals
        subtotal = sum(item.total_price for item in order_data.items)
        tax_amount = round(subtotal * 0.08, 2)  # 8% tax
        shipping_cost = 9.99 if subtotal < 50 else 0.0
        total_amount = subtotal + tax_amount + shipping_cost
        
        # Create payment info
        payment = PaymentInfo(
            payment_method=order_data.payment_method,
            payment_status=PaymentStatus.AUTHORIZED,
            transaction_id=f"TXN-{random.randint(100000, 999999)}",
            amount=total_amount,
            currency="EUR",
            processed_at=datetime.utcnow()
        )
        
        # Create order
        new_order = Order(
            order_id=order_id,
            order_number=order_number,
            status=OrderStatus.PENDING,
            channel=order_data.channel,
            customer=order_data.customer,
            shipping_address=order_data.shipping_address,
            billing_address=order_data.billing_address,
            items=order_data.items,
            subtotal=subtotal,
            tax_amount=tax_amount,
            shipping_cost=shipping_cost,
            discount_amount=0.0,
            total_amount=total_amount,
            payment=payment,
            notes=order_data.notes,
            metadata={"created_by": "api"}
        )
        
        self._orders.append(new_order)
        logger.info(f"Created new order: {order_number}")
        
        return new_order
    
    async def _validate_inventory(self, items: List[OrderItem]):
        """Validate inventory availability (mock implementation)"""
        # Simulate inventory check
        await asyncio.sleep(0.1)  # Simulate API call
        
        for item in items:
            # Mock inventory check - randomly fail for demo
            if random.random() < 0.05:  # 5% chance of inventory issue
                raise ValueError(f"Insufficient inventory for {item.product_name}")
    
    async def update_order(self, order_id: str, update_data: OrderUpdate) -> Optional[Order]:
        """Update an existing order"""
        for order in self._orders:
            if order.order_id == order_id:
                if update_data.status:
                    order.status = update_data.status
                if update_data.notes is not None:
                    order.notes = update_data.notes
                if update_data.metadata:
                    order.metadata.update(update_data.metadata)
                
                order.updated_at = datetime.utcnow()
                logger.info(f"Updated order {order_id}")
                return order
        return None
    
    async def cancel_order(self, order_id: str, reason: str, refund: bool = True) -> bool:
        """Cancel an order with optional refund"""
        for order in self._orders:
            if order.order_id == order_id:
                order.status = OrderStatus.CANCELLED
                order.notes = f"Cancelled: {reason}"
                order.updated_at = datetime.utcnow()
                
                if refund and order.payment.payment_status == PaymentStatus.CAPTURED:
                    order.payment.payment_status = PaymentStatus.REFUNDED
                    order.metadata["refund_processed"] = True
                
                logger.info(f"Cancelled order {order_id}")
                return True
        return False
    
    async def get_order_summary(self, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> OrderSummary:
        """Generate comprehensive order summary"""
        
        # Filter orders by date range
        orders = self._orders
        if date_from:
            orders = [o for o in orders if o.created_at >= date_from]
        if date_to:
            orders = [o for o in orders if o.created_at <= date_to]
        
        total_orders = len(orders)
        total_revenue = sum(o.total_amount for o in orders)
        average_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Orders by status
        orders_by_status = {}
        for status in OrderStatus:
            count = len([o for o in orders if o.status == status])
            if count > 0:
                orders_by_status[status.value] = count
        
        # Orders by channel
        orders_by_channel = {}
        for channel in SalesChannel:
            count = len([o for o in orders if o.channel == channel])
            if count > 0:
                orders_by_channel[channel.value] = count
        
        # Top products
        product_counts = {}
        for order in orders:
            for item in order.items:
                if item.product_name in product_counts:
                    product_counts[item.product_name] += item.quantity
                else:
                    product_counts[item.product_name] = item.quantity
        
        top_products = [
            {"product_name": name, "total_sold": count}
            for name, count in sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
        
        return OrderSummary(
            total_orders=total_orders,
            total_revenue=round(total_revenue, 2),
            orders_by_status=orders_by_status,
            orders_by_channel=orders_by_channel,
            average_order_value=round(average_order_value, 2),
            top_products=top_products
        )
    
    async def get_order_trends(self, period: str, granularity: str) -> Dict[str, Any]:
        """Generate order trends and analytics"""
        
        # Calculate date range based on period
        end_date = datetime.utcnow()
        if period == "7d":
            start_date = end_date - timedelta(days=7)
        elif period == "30d":
            start_date = end_date - timedelta(days=30)
        elif period == "90d":
            start_date = end_date - timedelta(days=90)
        else:  # 1y
            start_date = end_date - timedelta(days=365)
        
        # Filter orders in date range
        orders = [o for o in self._orders if start_date <= o.created_at <= end_date]
        
        # Generate trends (mock implementation)
        trends = {
            "period": period,
            "granularity": granularity,
            "total_orders": len(orders),
            "total_revenue": sum(o.total_amount for o in orders),
            "growth_rate": random.uniform(5.0, 25.0),  # Mock growth rate
            "conversion_rate": random.uniform(2.0, 8.0),  # Mock conversion rate
            "data_points": []
        }
        
        # Generate mock data points
        num_points = 7 if period == "7d" else 30 if period == "30d" else 90 if period == "90d" else 365
        for i in range(min(num_points, 20)):  # Limit to 20 points for demo
            point_date = start_date + timedelta(days=i * (num_points // 20))
            trends["data_points"].append({
                "date": point_date.isoformat(),
                "orders": random.randint(5, 50),
                "revenue": random.uniform(500, 5000)
            })
        
        return trends
    
    # Background task methods
    async def send_order_confirmation(self, order_id: str):
        """Send order confirmation email (mock implementation)"""
        await asyncio.sleep(1)  # Simulate email sending
        logger.info(f"Sent confirmation email for order {order_id}")
    
    async def update_analytics(self, order_id: str):
        """Update analytics after order creation (mock implementation)"""
        await asyncio.sleep(0.5)  # Simulate analytics update
        logger.info(f"Updated analytics for order {order_id}")
    
    async def notify_order_update(self, order_id: str, status: OrderStatus):
        """Notify customer of order status update (mock implementation)"""
        await asyncio.sleep(0.5)  # Simulate notification
        logger.info(f"Notified customer of status update for order {order_id}: {status.value}")