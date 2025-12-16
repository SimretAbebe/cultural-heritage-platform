import streamlit as st
from services.api import api_client

def main():
    """Render the home page content."""

    # Welcome section
    st.markdown("""
    ## 🌟 Welcome to Cultural Heritage Platform

    Discover, explore, and preserve the rich tapestry of human cultural heritage.
    Our platform serves as a digital repository for historical knowledge, traditional wisdom,
    and cultural treasures that define our shared human experience.
    """)

    # Platform features
    st.markdown("### 🎯 What We Preserve")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        #### 📚 History
        Ancient civilizations, significant events, and historical narratives that shaped our world.
        """)

    with col2:
        st.markdown("""
        #### 🎭 Traditions
        Cultural practices, rituals, festivals, and customs passed down through generations.
        """)

    with col3:
        st.markdown("""
        #### 👥 Leaders
        Influential figures, visionaries, and cultural icons who inspired change and progress.
        """)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        #### 🗺️ Places
        Sacred sites, historical landmarks, and geographical locations of cultural significance.
        """)

    with col5:
        st.markdown("""
        #### 💬 Sayings
        Proverbs, wisdom, philosophical insights, and linguistic treasures from diverse cultures.
        """)

    with col6:
        st.markdown("""
        #### 🎨 Arts & Culture
        Traditional arts, crafts, music, dance, and other forms of cultural expression.
        """)

    st.markdown("---")

   
    if api_client.check_connection():
        try:
            # Get categories count
            categories = api_client.get_categories()
            categories_count = len(categories)

            # Get heritage entries count (first page)
            heritage_data = api_client.get_heritage_entries(page=1, size=1)
            total_entries = heritage_data.get('total', 0)

            # Display stats
            st.markdown("### 📊 Platform Statistics")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Cultural Categories", categories_count)

            with col2:
                st.metric("Heritage Entries", total_entries)

            with col3:
                st.metric("Cultures Represented", "Multiple")

        except Exception as e:
            st.warning("Unable to load platform statistics at this time.")
    else:
        st.warning("🔌 Backend API is currently unavailable. Some features may not work.")

    st.markdown("---")

    # How to use the platform
    st.markdown("### 🚀 How to Explore")

    st.markdown("""
    #### 1. **Browse Categories** 📂
    Visit the Categories page to explore different cultural domains and see what's available.

    #### 2. **Discover Heritage** 🔍
    Use the Explore Heritage page to search through our collection with powerful filtering options.

    #### 3. **Contribute** (Admin Only) ✍️
    Cultural custodians can add new entries to preserve important heritage content.
    """)

    # Call to action
    st.markdown("---")

    st.markdown("""
    ### 🎉 Start Your Cultural Journey

    Choose a page from the sidebar to begin exploring the rich heritage of humanity.
    Each entry tells a story, preserves a tradition, or honors a legacy that connects us all.
    """)

    # Inspirational quote
    st.markdown("""
    > *"The heritage of the past is the seed that brings forth the harvest of the future."*
    >
    > — Sterling W. Sill
    """)

if __name__ == "__main__":
    main()
