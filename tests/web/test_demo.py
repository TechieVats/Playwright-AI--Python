"""Demo tests to verify the framework is working correctly."""

import pytest


@pytest.mark.asyncio
async def test_google_homepage(browser_test):
    """Test that we can navigate to Google and verify basic elements."""
    
    # Navigate to Google
    await browser_test.navigate_to("https://www.google.com")
    
    # Verify page title contains "Google"
    page_title = await browser_test.page.title()
    assert "Google" in page_title, f"Expected 'Google' in title, got: {page_title}"
    
    # Take a screenshot
    await browser_test.capture_screenshot("google_homepage")
    
    print(f"✅ Successfully loaded Google homepage with title: {page_title}")


@pytest.mark.asyncio
async def test_search_functionality(browser_test):
    """Test Google search functionality."""
    
    # Navigate to Google
    await browser_test.navigate_to("https://www.google.com")
    
    # Find search box and search for "Playwright"
    search_box = "textarea[name='q']"  # Google's search input
    
    # Wait for search box to be available
    await browser_test.wait_for_element(search_box)
    
    # Type search query
    await browser_test.type_text(search_box, "Playwright automation")
    
    # Press Enter to search
    await browser_test.page.keyboard.press("Enter")
    
    # Wait for results page to load
    await browser_test.page.wait_for_load_state("networkidle")
    
    # Verify we're on results page
    page_url = browser_test.page.url
    assert "search" in page_url, f"Should be on search results page, got: {page_url}"
    
    # Take screenshot of results
    await browser_test.capture_screenshot("google_search_results")
    
    print("✅ Successfully performed Google search")


@pytest.mark.asyncio
async def test_responsive_design(browser_test):
    """Test responsive design at different viewport sizes."""
    
    # Navigate to a responsive website
    await browser_test.navigate_to("https://example.com")
    
    # Test different viewport sizes
    viewports = [
        {"width": 1920, "height": 1080, "name": "desktop"},
        {"width": 768, "height": 1024, "name": "tablet"},
        {"width": 375, "height": 667, "name": "mobile"}
    ]
    
    for viewport in viewports:
        # Set viewport size
        await browser_test.page.set_viewport_size({
            "width": viewport["width"], 
            "height": viewport["height"]
        })
        
        # Wait a moment for layout to adjust
        import asyncio
        await asyncio.sleep(1)
        
        # Take screenshot at this viewport
        await browser_test.capture_screenshot(f"responsive_{viewport['name']}")
        
        # Verify page still has content
        body_content = await browser_test.get_text("body")
        assert len(body_content.strip()) > 0, f"Page should have content at {viewport['name']} size"
        
        print(f"✅ Tested {viewport['name']} viewport: {viewport['width']}x{viewport['height']}")


@pytest.mark.asyncio 
async def test_page_performance(browser_test):
    """Test basic page performance."""
    
    import time
    
    # Measure page load time
    start_time = time.time()
    await browser_test.navigate_to("https://httpbin.org/delay/1")  # Simple test endpoint with 1s delay
    load_time = time.time() - start_time
    
    # Page should load within reasonable time (10 seconds)
    assert load_time < 10, f"Page load time {load_time:.2f}s is too slow"
    
    # Take screenshot
    await browser_test.capture_screenshot("performance_test")
    
    print(f"✅ Page loaded in {load_time:.2f} seconds")


@pytest.mark.asyncio
async def test_framework_basics(browser_test):
    """Test basic framework functionality."""
    
    # Test navigation
    await browser_test.navigate_to("https://httpbin.org/html")
    
    # Test getting page title
    title = await browser_test.page.title()
    assert isinstance(title, str), "Title should be a string"
    
    # Test getting text from an element
    try:
        h1_text = await browser_test.get_text("h1")
        print(f"Found H1 text: {h1_text}")
    except:
        print("No H1 element found (that's okay)")
    
    # Test screenshot capture
    screenshot_path = await browser_test.capture_screenshot("framework_test")
    assert screenshot_path.endswith(".png"), "Screenshot should be a PNG file"
    
    # Test page URL
    current_url = browser_test.page.url
    assert "httpbin.org" in current_url, f"Should be on httpbin.org, got: {current_url}"
    
    print("✅ All framework basic functions working correctly")


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_simple_smoke_test(browser_test):
    """Simple smoke test to verify framework is working."""
    
    # Just navigate to a simple page and verify it loads
    await browser_test.navigate_to("https://httpbin.org/")
    
    # Check page loaded
    title = await browser_test.page.title()
    assert len(title) > 0, "Page should have a title"
    
    # Take screenshot
    await browser_test.capture_screenshot("smoke_test")
    
    print("✅ Smoke test passed - framework is working!")
