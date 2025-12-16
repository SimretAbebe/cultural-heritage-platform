import streamlit as st
from services.api import api_client

def main():
    """Render the categories page content."""
    st.markdown("## 📂 Cultural Categories")

    st.markdown("""
    Explore different domains of cultural heritage. Each category represents a unique aspect
    of human cultural expression and historical significance.
    """)

    # Check API connection
    if not api_client.check_connection():
        st.error("🔌 Unable to connect to the backend API. Please check your connection.")
        return

    try:
        # Fetch categories from API
        with st.spinner("Loading categories..."):
            categories = api_client.get_categories()

        if not categories:
            st.info("No categories available yet. Check back later!")
            return

        # Display categories in a grid
        st.markdown(f"### Found {len(categories)} Categories")

        # Create columns for better layout
        cols = st.columns(2)

        for i, category in enumerate(categories):
            col = cols[i % 2]

            with col:
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    # Category header
                    st.markdown(f"### {category['name']}")

                    # Category description
                    if category.get('description'):
                        st.write(category['description'])
                    else:
                        st.write("*No description available*")

                    # Quick stats for this category
                    try:
                        # Get count of entries in this category
                        heritage_data = api_client.get_heritage_entries(
                            category_id=category['id'],
                            page=1,
                            size=1
                        )
                        entry_count = heritage_data.get('total', 0)

                        st.metric("Heritage Entries", entry_count)

                    except Exception:
                        st.write("📚 Heritage entries available")

                    # Navigation button
                    if st.button(
                        f"Explore {category['name']} →",
                        key=f"explore_{category['id']}",
                        help=f"Browse heritage entries in {category['name']}"
                    ):
                        # Store selected category in session state for Explore page
                        st.session_state.selected_category = category
                        st.success(f"Selected {category['name']}. Go to Explore Heritage page to browse entries!")

                    st.markdown('</div>', unsafe_allow_html=True)

        # Summary section
        st.markdown("---")
        st.markdown("### 📊 Category Overview")

        # Create a summary table
        category_summary = []
        for category in categories:
            try:
                heritage_data = api_client.get_heritage_entries(
                    category_id=category['id'],
                    page=1,
                    size=1
                )
                entry_count = heritage_data.get('total', 0)
            except:
                entry_count = 0

            category_summary.append({
                "Category": category['name'],
                "Description": category.get('description', 'N/A')[:50] + '...' if category.get('description') and len(category.get('description', '')) > 50 else category.get('description', 'N/A'),
                "Entries": entry_count
            })

        if category_summary:
            import pandas as pd
            df = pd.DataFrame(category_summary)
            st.dataframe(df, use_container_width=True)

        # Tips section
        st.markdown("---")
        st.markdown("### 💡 Navigation Tips")

        st.markdown("""
        - **Click "Explore [Category]"** to filter the Explore Heritage page by that category
        - **Visit the Explore page** to search and browse heritage entries within categories
        - **Admin users** can create new categories through the API
        """)

    except Exception as e:
        st.error(f"Error loading categories: {str(e)}")
        st.info("Please try refreshing the page or check your internet connection.")

if __name__ == "__main__":
    main()
