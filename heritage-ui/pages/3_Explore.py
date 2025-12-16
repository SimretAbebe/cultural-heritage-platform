import streamlit as st
from services.api import api_client

def main():
    """Render the explore heritage page content."""
    st.markdown("## 🔍 Explore Cultural Heritage")

    st.markdown("""
    Discover amazing cultural heritage content through our comprehensive collection.
    Use the search and filter options below to find exactly what you're looking for.
    """)

    # Check API connection
    if not api_client.check_connection():
        st.error("🔌 Unable to connect to the backend API. Please check your connection.")
        return

    try:
        # Get categories for filtering
        categories = api_client.get_categories()
        category_options = {cat['name']: cat['id'] for cat in categories}
        category_options["All Categories"] = None

        # Search and filter controls
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            search_query = st.text_input(
                "🔍 Search heritage content",
                placeholder="Enter keywords to search in titles and content...",
                help="Search across heritage entry titles and content"
            )

        with col2:
            selected_category_name = st.selectbox(
                "📂 Filter by Category",
                options=list(category_options.keys()),
                help="Narrow down results to a specific cultural category"
            )

        with col3:
            page_size = st.selectbox(
                "📄 Items per page",
                options=[10, 20, 50],
                help="Number of entries to display per page"
            )

        # Get selected category ID
        selected_category_id = category_options[selected_category_name]

        # Initialize session state for pagination
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1

        # Check if category was selected from Categories page
        if 'selected_category' in st.session_state:
            selected_category = st.session_state.selected_category
            st.info(f"📂 Showing results for category: **{selected_category['name']}**")
            selected_category_id = selected_category['id']
            selected_category_name = selected_category['name']
            # Clear the selection after using it
            del st.session_state.selected_category

        # Search button
        if st.button("🔍 Search", type="primary"):
            st.session_state.current_page = 1  # Reset to first page on new search

        # Fetch heritage entries
        with st.spinner("Searching cultural heritage..."):
            heritage_data = api_client.get_heritage_entries(
                page=st.session_state.current_page,
                size=page_size,
                search=search_query if search_query else None,
                category_id=selected_category_id
            )

        # Display results
        total_results = heritage_data.get('total', 0)
        current_page = heritage_data.get('page', 1)
        total_pages = heritage_data.get('pages', 1)
        items = heritage_data.get('items', [])

        # Results header
        st.markdown("---")
        st.markdown(f"### Results ({total_results} entries found)")

        if total_results == 0:
            st.info("No heritage entries found matching your criteria. Try adjusting your search or filters.")
        else:
            # Display entries
            for item in items:
                with st.container():
                    st.markdown('<div class="heritage-content">', unsafe_allow_html=True)

                    # Title and metadata
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.markdown(f"### {item['title']}")

                    with col2:
                        st.markdown(f"**Category:** {item.get('category_name', 'Unknown')}")
                        st.markdown(f"**Created:** {item['created_at'][:10]}")
                        if item.get('creator_username'):
                            st.markdown(f"**By:** {item['creator_username']}")

                    # Content preview (truncated for readability)
                    content = item['content']
                    if len(content) > 500:
                        content = content[:500] + "..."
                        show_full = st.button(f"Read more about '{item['title']}'", key=f"read_more_{item['id']}")
                        if show_full:
                            st.markdown("**Full Content:**")
                            st.write(item['content'])
                        else:
                            st.write(content)
                    else:
                        st.write(content)

                    st.markdown('</div>', unsafe_allow_html=True)

            # Pagination controls
            st.markdown("---")

            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                if current_page > 1:
                    if st.button("⬅️ Previous", key="prev_page"):
                        st.session_state.current_page -= 1
                        st.rerun()

            with col2:
                st.markdown(f"**Page {current_page} of {total_pages}**")

            with col3:
                if current_page < total_pages:
                    if st.button("Next ➡️", key="next_page"):
                        st.session_state.current_page += 1
                        st.rerun()

            # Page size selector for pagination
            if total_pages > 1:
                st.markdown("**Quick Navigation:**")
                page_options = list(range(1, min(total_pages + 1, 11)))  # Show first 10 pages
                if total_pages > 10:
                    page_options.append(total_pages)  # Add last page

                selected_page = st.selectbox(
                    "Go to page:",
                    options=page_options,
                    index=current_page-1 if current_page <= 10 else 0
                )

                if selected_page != current_page:
                    st.session_state.current_page = selected_page
                    st.rerun()

        # Search tips
        st.markdown("---")
        st.markdown("### 💡 Search Tips")

        tips_col1, tips_col2 = st.columns(2)

        with tips_col1:
            st.markdown("""
            **Search Features:**
            - Search works in both titles and content
            - Partial matches are supported
            - Case-insensitive search
            - Multiple keywords separated by spaces
            """)

        with tips_col2:
            st.markdown("""
            **Category Filtering:**
            - Browse by cultural domain
            - Combine search with category filters
            - All Categories shows everything
            - Categories help organize content
            """)

        # Quick stats
        if total_results > 0:
            st.markdown("---")
            st.markdown("### 📊 Search Summary")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Results", total_results)

            with col2:
                st.metric("Current Page", f"{current_page}/{total_pages}")

            with col3:
                st.metric("Items/Page", page_size)

            with col4:
                st.metric("Categories", len(categories))

    except Exception as e:
        st.error(f"Error exploring heritage content: {str(e)}")
        st.info("Please try refreshing the page or contact support if the problem persists.")

if __name__ == "__main__":
    main()
