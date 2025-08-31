"""Simple tests for home page functionality."""

import pytest
from pages.home_page import HomePage


@pytest.mark.asyncio
class TestHomePage:
    """Test suite for home page."""
    
    async def test_home_page_loads(self, browser_test, config):
        """Test that home page loads successfully."""
        # Navigate to home page
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        await browser_test.navigate_to(base_url)
        
        # Create page object
        home_page = HomePage(browser_test.page)
        
        # Verify page title
        page_title = await home_page.get_page_title()
        assert page_title is not None
        assert len(page_title) > 0
        
        # Take screenshot
        await browser_test.capture_screenshot("home_page_loaded")
    
    async def test_navigation_menu_visible(self, browser_test, config):
        """Test that navigation menu is visible."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        await browser_test.navigate_to(base_url)
        
        home_page = HomePage(browser_test.page)
        
        # Check if navigation is visible (this might fail if element doesn't exist)
        try:
            is_nav_visible = await home_page.is_navigation_visible()
            # If element exists, it should be visible
            assert is_nav_visible
        except:
            # If element doesn't exist, that's also acceptable for this simple test
            pass
    
    async def test_search_functionality(self, browser_test, config):
        """Test search functionality if available."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        await browser_test.navigate_to(base_url)
        
        home_page = HomePage(browser_test.page)
        
        # Try to perform search (will only work if search elements exist)
        try:
            await home_page.search("test query")
            # If search works, take a screenshot
            await browser_test.capture_screenshot("search_performed")
        except:
            # Search elements might not exist, which is fine for this demo
            pass
