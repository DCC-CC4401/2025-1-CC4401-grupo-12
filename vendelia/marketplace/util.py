# Helper function to generate number of pages in a search
def get_pagination_pages(current_page, total_pages, left=2, right=2):
    pages = []

    if total_pages <= 1:
        return [1]

    # Always include first page
    pages.append(1)

    # Calculate left and right window boundaries
    start = max(current_page - left, 2)
    end = min(current_page + right, total_pages - 1)

    # Add ellipsis after first page if needed
    if start > 2:
        pages.append('...')

    # Add pages in the window
    pages.extend(range(start, end + 1))

    # Add ellipsis before last page if needed
    if end < total_pages - 1:
        pages.append('...')

    # Always include last page if > 1
    if total_pages > 1:
        pages.append(total_pages)

    return pages

