import os
import requests
from typing import Dict, List, Optional, Any
import streamlit as st

# Configuration
FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")

class APIError(Exception):
    """Custom exception for API errors."""
    pass

class CulturalHeritageAPI:
    """Service class for interacting with the Cultural Heritage API."""

    def __init__(self, base_url: str = FASTAPI_BASE_URL):
        """Initialize API client with base URL."""
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        # Set a reasonable timeout for all requests
        self.timeout = 10

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request to API with error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests

        Returns:
            Response data as dictionary

        Raises:
            APIError: If request fails or returns error status
        """
        url = f"{self.base_url}{endpoint}"

        try:
            # Add timeout if not specified
            kwargs.setdefault('timeout', self.timeout)

            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # Raise exception for bad status codes

            # Return JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            raise APIError(f"API request failed: {str(e)}")
        except ValueError as e:
            raise APIError(f"Invalid JSON response: {str(e)}")

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authorization headers if user is logged in."""
        if 'auth_token' in st.session_state and st.session_state.auth_token:
            return {"Authorization": f"Bearer {st.session_state.auth_token}"}
        return {}

    # Authentication endpoints
    def register_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user account."""
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        return self._make_request("POST", "/auth/register", json=data)

    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and get access token."""
        data = {
            "username": username,
            "password": password
        }
        return self._make_request("POST", "/auth/login-json", json=data)

    def get_current_user(self) -> Dict[str, Any]:
        """Get current authenticated user information."""
        headers = self._get_auth_headers()
        return self._make_request("GET", "/auth/me", headers=headers)

    # Categories endpoints
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all cultural heritage categories."""
        return self._make_request("GET", "/categories")

    def create_category(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new category (admin only)."""
        headers = self._get_auth_headers()
        data = {"name": name}
        if description:
            data["description"] = description
        return self._make_request("POST", "/categories", json=data, headers=headers)

    # Heritage entries endpoints
    def get_heritage_entries(
        self,
        page: int = 1,
        size: int = 10,
        search: Optional[str] = None,
        category_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get paginated heritage entries with optional filtering.

        Args:
            page: Page number (1-based)
            size: Number of items per page
            search: Search keyword for title/content
            category_id: Filter by category ID

        Returns:
            Paginated response with items, total, page, size, pages
        """
        params = {
            "page": page,
            "size": size
        }
        if search:
            params["search"] = search
        if category_id:
            params["category_id"] = category_id

        return self._make_request("GET", "/heritage", params=params)

    def get_heritage_entry(self, heritage_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific heritage entry."""
        return self._make_request("GET", f"/heritage/{heritage_id}")

    def create_heritage_entry(
        self,
        title: str,
        content: str,
        category_id: int
    ) -> Dict[str, Any]:
        """Create a new heritage entry (admin only)."""
        headers = self._get_auth_headers()
        data = {
            "title": title,
            "content": content,
            "category_id": category_id
        }
        return self._make_request("POST", "/heritage", json=data, headers=headers)

    # Utility methods
    def check_connection(self) -> bool:
        """Check if API is accessible."""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False

    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated."""
        return 'auth_token' in st.session_state and bool(st.session_state.auth_token)

    def logout(self):
        """Clear authentication token."""
        if 'auth_token' in st.session_state:
            del st.session_state.auth_token

# Global API instance
api_client = CulturalHeritageAPI()
