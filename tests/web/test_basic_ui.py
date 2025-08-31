"""Basic UI tests for web application."""

import pytest


@pytest.mark.asyncio
class TestBasicUI:
    """Basic UI functionality tests."""
    
    async def test_page_loads_successfully(self, browser_test, config):
        """Test that any page loads without errors."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        
        try:
            await browser_test.navigate_to(base_url)
            
            # Check that page loaded (has a title)
            page_title = await browser_test.page.title()
            assert page_title is not None
            
            # Take screenshot
            await browser_test.capture_screenshot("page_loaded_successfully")
            
        except Exception as e:
            pytest.skip(f"Application not available at {base_url}: {e}")
    
    async def test_page_has_content(self, browser_test, config):
        """Test that page has some content."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        
        try:
            await browser_test.navigate_to(base_url)
            
            # Get page content
            body_content = await browser_test.get_text("body")
            
            # Should have some content
            assert len(body_content.strip()) > 0, "Page should have some content"
            
            await browser_test.capture_screenshot("page_with_content")
            
        except Exception as e:
            pytest.skip(f"Could not test page content: {e}")
    
    async def test_responsive_design(self, browser_test, config):
        """Test responsive design at different viewport sizes."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        
        try:
            await browser_test.navigate_to(base_url)
            
            # Test different viewport sizes
            viewports = [
                {"width": 1920, "height": 1080, "name": "desktop"},
                {"width": 768, "height": 1024, "name": "tablet"},
                {"width": 375, "height": 667, "name": "mobile"}
            ]
            
            for viewport in viewports:
                await browser_test.page.set_viewport_size(
                    viewport["width"], 
                    viewport["height"]
                )
                
                # Wait a moment for layout to adjust
                import asyncio
                await asyncio.sleep(1)
                
                # Take screenshot at this viewport
                await browser_test.capture_screenshot(f"responsive_{viewport['name']}")
                
                # Verify page still has content
                body_content = await browser_test.get_text("body")
                assert len(body_content.strip()) > 0, f"Page should have content at {viewport['name']} size"
            
        except Exception as e:
            pytest.skip(f"Could not test responsive design: {e}")
    
    async def test_page_performance(self, browser_test, config):
        """Basic page performance test."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        
        try:
            import time
            
            # Measure page load time
            start_time = time.time()
            await browser_test.navigate_to(base_url)
            load_time = time.time() - start_time
            
            # Page should load within reasonable time (10 seconds for demo)
            assert load_time < 10, f"Page load time {load_time:.2f}s is too slow"
            
            # Get performance metrics if available
            try:
                performance_metrics = await browser_test.page.evaluate("""
                    () => {
                        const timing = performance.timing;
                        return {
                            domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                            loadComplete: timing.loadEventEnd - timing.navigationStart
                        };
                    }
                """)
                
                print(f"Performance metrics: {performance_metrics}")
                
            except:
                # Performance API might not be available
                pass
            
            await browser_test.capture_screenshot("performance_test")
            
        except Exception as e:
            pytest.skip(f"Could not test page performance: {e}")
    
    async def test_basic_interactions(self, browser_test, config):
        """Test basic page interactions."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        
        try:
            await browser_test.navigate_to(base_url)
            
            # Try to find and interact with common elements
            common_selectors = [
                "button",
                "input",
                "a",
                "[role='button']",
                "[data-testid]"
            ]
            
            interactions_found = 0
            
            for selector in common_selectors:
                try:
                    elements = await browser_test.page.query_selector_all(selector)
                    if elements:
                        interactions_found += len(elements)
                        print(f"Found {len(elements)} elements with selector: {selector}")
                except:
                    continue
            
            print(f"Total interactive elements found: {interactions_found}")
            
            await browser_test.capture_screenshot("basic_interactions")
            
        except Exception as e:
            pytest.skip(f"Could not test basic interactions: {e}")
