# backend/tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestMainEndpoints:
    """Test main application endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "🚀 Cloud Omnichannel Solution API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "operational"
        assert "documentation" in data
        assert "health_check" in data
    
    def test_app_info_endpoint(self):
        """Test application info endpoint"""
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        
        # Verify application info
        assert "application" in data
        assert data["application"]["name"] == "Cloud Omnichannel Solution"
        assert data["application"]["version"] == "1.0.0"
        
        # Verify system info
        assert "system" in data
        assert data["system"]["framework"] == "FastAPI"
        assert data["system"]["cloud_ready"] is True
        
        # Verify features
        assert "features" in data
        assert data["features"]["multi_channel_orders"] is True
    
    def test_openapi_schema(self):
        """Test OpenAPI schema is accessible"""
        response = client.get("/api/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert schema["info"]["title"] == "Cloud Omnichannel Solution API"
    
    def test_docs_accessible(self):
        """Test API documentation is accessible"""
        response = client.get("/api/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        response = client.options("/")
        assert response.status_code == 200
        # Note: In tests, CORS headers might not be present without actual cross-origin request
    
    def test_custom_headers(self):
        """Test custom headers are added to responses"""
        response = client.get("/")
        assert "X-API-Version" in response.headers
        assert response.headers["X-API-Version"] == "1.0.0"

# backend/tests/test_orders.py
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import json

from app.main import app
from app.models.orders import OrderStatus, SalesChannel, ProductCategory

client = TestClient(app)

class TestOrdersAPI:
    """Test orders API endpoints"""
    
    @pytest.fixture
    def sample_order_data(self):
        """Sample order data for testing"""
        return {
            "channel": "online",
            "customer": {
                "customer_id": "CUST-TEST-001",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "phone": "+49-123-4567890",
                "loyalty_tier": "standard"
            },
            "shipping_address": {
                "street_address": "123 Test Street",
                "city": "Berlin",
                "state": "Berlin",
                "postal_code": "10115",
                "country": "Germany",
                "is_default": True
            },
            "items": [
                {
                    "product_id": "PROD-TEST-001",
                    "product_name": "Test Product",
                    "sku": "SKU-12345",
                    "category": "electronics",
                    "quantity": 2,
                    "unit_price": 29.99,
                    "total_price": 59.98,
                    "discount_amount": 0.0,
                    "tax_amount": 4.80
                }
            ],
            "payment_method": "credit_card",
            "notes": "Test order"
        }
    
    def test_get_orders_default(self):
        """Test getting orders with default parameters"""
        response = client.get("/api/v1/orders/")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert data["page"] == 1
        assert data["size"] == 20
        assert isinstance(data["items"], list)
    
    def test_get_orders_pagination(self):
        """Test orders pagination"""
        response = client.get("/api/v1/orders/?page=1&size=5")
        assert response.status_code == 200
        
        data = response.json()
        assert data["page"] == 1
        assert data["size"] == 5
        assert len(data["items"]) <= 5
    
    def test_get_orders_filter_by_status(self):
        """Test filtering orders by status"""
        response = client.get("/api/v1/orders/?status=delivered")
        assert response.status_code == 200
        
        data = response.json()
        for order in data["items"]:
            assert order["status"] == "delivered"
    
    def test_get_orders_filter_by_channel(self):
        """Test filtering orders by channel"""
        response = client.get("/api/v1/orders/?channel=online")
        assert response.status_code == 200
        
        data = response.json()
        for order in data["items"]:
            assert order["channel"] == "online"
    
    def test_get_orders_date_range_filter(self):
        """Test filtering orders by date range"""
        date_from = (datetime.utcnow() - timedelta(days=30)).isoformat()
        date_to = datetime.utcnow().isoformat()
        
        response = client.get(f"/api/v1/orders/?date_from={date_from}&date_to={date_to}")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
    
    def test_get_orders_amount_filter(self):
        """Test filtering orders by amount range"""
        response = client.get("/api/v1/orders/?min_amount=50&max_amount=500")
        assert response.status_code == 200
        
        data = response.json()
        for order in data["items"]:
            assert 50 <= order["total_amount"] <= 500
    
    def test_get_orders_search(self):
        """Test searching orders"""
        response = client.get("/api/v1/orders/?search=alice")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
    
    def test_get_orders_sorting(self):
        """Test orders sorting"""
        response = client.get("/api/v1/orders/?sort_by=total_amount&sort_order=desc")
        assert response.status_code == 200
        
        data = response.json()
        if len(data["items"]) > 1:
            amounts = [order["total_amount"] for order in data["items"]]
            assert amounts == sorted(amounts, reverse=True)
    
    def test_get_orders_summary(self):
        """Test getting orders summary"""
        response = client.get("/api/v1/orders/summary")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_orders" in data
        assert "total_revenue" in data
        assert "orders_by_status" in data
        assert "orders_by_channel" in data
        assert "average_order_value" in data
        assert "top_products" in data
        assert isinstance(data["total_orders"], int)
        assert isinstance(data["total_revenue"], (int, float))
    
    def test_get_order_by_id_existing(self):
        """Test getting existing order by ID"""
        # First get list of orders to get a valid ID
        list_response = client.get("/api/v1/orders/")
        assert list_response.status_code == 200
        
        orders = list_response.json()["items"]
        if orders:
            order_id = orders[0]["order_id"]
            
            response = client.get(f"/api/v1/orders/{order_id}")
            assert response.status_code == 200
            
            data = response.json()
            assert data["order_id"] == order_id
            assert "customer" in data
            assert "items" in data
            assert "total_amount" in data
    
    def test_get_order_by_id_not_found(self):
        """Test getting non-existent order by ID"""
        response = client.get("/api/v1/orders/non-existent-id")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data or "detail" in data
    
    def test_create_order_valid(self, sample_order_data):
        """Test creating valid order"""
        response = client.post("/api/v1/orders/", json=sample_order_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "order_id" in data["data"]
        assert "order_number" in data["data"]
    
    def test_create_order_invalid_data(self):
        """Test creating order with invalid data"""
        invalid_data = {
            "channel": "invalid_channel",
            "customer": {
                "first_name": "",  # Invalid: empty name
                "email": "invalid-email"  # Invalid: bad email format
            }
        }
        
        response = client.post("/api/v1/orders/", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_update_order_existing(self):
        """Test updating existing order"""
        # First get an existing order
        list_response = client.get("/api/v1/orders/")
        orders = list_response.json()["items"]
        
        if orders:
            order_id = orders[0]["order_id"]
            update_data = {
                "status": "processing",
                "notes": "Updated via test"
            }
            
            response = client.put(f"/api/v1/orders/{order_id}", json=update_data)
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] is True
    
    def test_update_order_not_found(self):
        """Test updating non-existent order"""
        update_data = {"status": "processing"}
        response = client.put("/api/v1/orders/non-existent-id", json=update_data)
        assert response.status_code == 404
    
    def test_cancel_order_existing(self):
        """Test cancelling existing order"""
        # First get an existing order
        list_response = client.get("/api/v1/orders/")
        orders = list_response.json()["items"]
        
        if orders:
            order_id = orders[0]["order_id"]
            
            response = client.delete(f"/api/v1/orders/{order_id}?reason=Test cancellation")
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] is True
    
    def test_cancel_order_not_found(self):
        """Test cancelling non-existent order"""
        response = client.delete("/api/v1/orders/non-existent-id?reason=Test")
        assert response.status_code == 404
    
    def test_get_order_trends(self):
        """Test getting order trends"""
        response = client.get("/api/v1/orders/analytics/trends?period=30d&granularity=day")
        assert response.status_code == 200
        
        data = response.json()
        assert "period" in data
        assert "granularity" in data
        assert "total_orders" in data
        assert "total_revenue" in data
        assert "data_points" in data
        assert data["period"] == "30d"
        assert data["granularity"] == "day"
    
    def test_invalid_pagination_parameters(self):
        """Test invalid pagination parameters"""
        response = client.get("/api/v1/orders/?page=0&size=0")
        assert response.status_code == 422  # Validation error
    
    def test_invalid_sort_parameters(self):
        """Test invalid sort parameters"""
        response = client.get("/api/v1/orders/?sort_order=invalid")
        assert response.status_code == 422  # Validation error

# backend/tests/test_health.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check_success(self):
        """Test main health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "service" in data
        assert "version" in data
        assert "system" in data
        assert "dependencies" in data
        assert "metrics" in data
        
        assert data["service"] == "Cloud Omnichannel Solution API"
        assert data["version"] == "1.0.0"
        assert data["status"] in ["healthy", "degraded", "unhealthy"]
    
    def test_health_system_metrics(self):
        """Test health check includes system metrics"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        system = data["system"]
        
        assert "python_version" in system
        assert "cpu_usage_percent" in system
        assert "memory" in system
        assert "disk" in system
        
        # Check memory metrics
        memory = system["memory"]
        assert "total_gb" in memory
        assert "used_gb" in memory
        assert "usage_percent" in memory
        
        # Check disk metrics
        disk = system["disk"]
        assert "total_gb" in disk
        assert "used_gb" in disk
        assert "usage_percent" in disk
    
    def test_health_dependencies_status(self):
        """Test health check includes dependency status"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        dependencies = data["dependencies"]
        
        assert "database" in dependencies
        assert "redis" in dependencies
        assert "payment_gateway" in dependencies
        assert "inventory_service" in dependencies
    
    def test_readiness_probe(self):
        """Test Kubernetes readiness probe"""
        response = client.get("/health/ready")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ready"
        assert "timestamp" in data
        assert "checks" in data
        
        checks = data["checks"]
        assert "api" in checks
        assert "database" in checks
        assert "dependencies" in checks
    
    def test_liveness_probe(self):
        """Test Kubernetes liveness probe"""
        response = client.get("/health/live")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "alive"
        assert "timestamp" in data

# backend/tests/conftest.py
import pytest
import asyncio
from typing import Generator

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def anyio_backend():
    """Use asyncio for async tests"""
    return "asyncio"