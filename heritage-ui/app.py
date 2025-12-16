"""
Main Streamlit application for Cultural Heritage Platform.
Provides a clean, user-friendly interface to explore cultural heritage content.
"""

import streamlit as st
import os
from pathlib import Path

# Configure page settings
st.set_page_config(
    page_title="Cultural Heritage Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .heritage-content {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Environment configuration
FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")

def main():
    """Main application entry point."""
    # Application header
    st.markdown('<h1 class="main-header">🏛️ Cultural Heritage Platform</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Preserving and sharing the rich cultural heritage of humanity</p>',
        unsafe_allow_html=True
    )

    # Sidebar navigation
    st.sidebar.title("Navigation")

    # Page selection
    pages = {
        "🏠 Home": "1_Home.py",
        "📂 Categories": "2_Categories.py",
        "🔍 Explore Heritage": "3_Explore.py"
    }

    selected_page = st.sidebar.radio("Go to", list(pages.keys()))

    # Load and display the selected page
    page_file = pages[selected_page]
    page_path = Path(__file__).parent / "pages" / page_file

    if page_path.exists():
        # Import and run the page module
        page_name = page_file.replace(".py", "")
        try:
            # Dynamic import of page modules
            import importlib.util
            spec = importlib.util.spec_from_file_location(page_name, page_path)
            page_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(page_module)

            # Call the main function if it exists
            if hasattr(page_module, 'main'):
                page_module.main()
            else:
                st.error(f"Page {page_file} does not have a main() function")

        except Exception as e:
            st.error(f"Error loading page {page_file}: {str(e)}")
    else:
        st.error(f"Page {page_file} not found")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("This platform preserves cultural heritage including history, traditions, leaders, places, and sayings.")
    st.sidebar.markdown(f"**API Status:** {'🟢 Connected' if check_api_connection() else '🔴 Disconnected'}")

def check_api_connection():
    """Check if the FastAPI backend is accessible."""
    try:
        import requests
        response = requests.get(f"{FASTAPI_BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    main()
