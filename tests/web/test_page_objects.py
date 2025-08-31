"""Test using page objects pattern."""

import pytest
from pages.google_page import GooglePage


@pytest.mark.asyncio
async def test_google_search_with_page_object(browser_test):
    """Test Google search using page object pattern."""
    
    # Create page object
    google_page = GooglePage(browser_test.page)
    
    # Navigate to Google
    await google_page.navigate()
    
    # Verify search box is visible
    is_visible = await google_page.is_search_box_visible()
    assert is_visible, "Search box should be visible"
    
    # Perform search
    search_query = "Playwright Python automation"
    await google_page.search(search_query)
    
    # Verify we got results
    current_url = await google_page.get_current_url()
    assert "search" in current_url, f"Should be on search results page, got: {current_url}"
    
    # Try to get results count (may not always be available)
    results_text = await google_page.get_search_results_count()
    print(f"Search results info: {results_text}")
    
    # Take screenshot
    await browser_test.capture_screenshot("page_object_search")
    
    print(f"✅ Successfully searched for '{search_query}' using page object")


@pytest.mark.asyncio
async def test_multiple_searches(browser_test):
    """Test multiple searches using page object."""
    
    google_page = GooglePage(browser_test.page)
    await google_page.navigate()
    
    search_queries = [
        "Python testing",
        "Web automation",
        "Playwright framework"
    ]
    
    for i, query in enumerate(search_queries):
        # Go back to Google homepage for each search
        if i > 0:
            await google_page.navigate()
        
        # Perform search
        await google_page.search(query)
        
        # Verify results page
        current_url = await google_page.get_current_url()
        assert "search" in current_url, f"Search {i+1} should show results"
        
        # Take screenshot
        await browser_test.capture_screenshot(f"search_{i+1}_{query.replace(' ', '_')}")
        
        print(f"✅ Search {i+1}: '{query}' completed")
    
    print("✅ All multiple searches completed successfully")
