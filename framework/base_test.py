"""Base test class for all test cases."""

import asyncio
import os
from typing import Optional
from pathlib import Path

from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright


class BaseTest:
    """
    Simple base test class providing common functionality.
    
    Features:
    - Browser management
    - Page navigation
    - Screenshot capture
    - Basic waiting utilities
    """

    def __init__(self):
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def setup_browser(
        self,
        browser_name: str = "chromium",
        headless: bool = True,
        viewport: Optional[dict] = None
    ) -> None:
        """
        Set up browser instance.
        
        Args:
            browser_name: Browser to use (chromium, firefox, webkit)
            headless: Whether to run in headless mode
            viewport: Browser viewport size
        """
        self.playwright = await async_playwright().start()
        
        # Launch browser
        if browser_name.lower() == "chromium":
            self.browser = await self.playwright.chromium.launch(headless=headless)
        elif browser_name.lower() == "firefox":
            self.browser = await self.playwright.firefox.launch(headless=headless)
        elif browser_name.lower() == "webkit":
            self.browser = await self.playwright.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        # Create context and page
        context_options = {}
        if viewport:
            context_options["viewport"] = viewport
        
        self.context = await self.browser.new_context(**context_options)
        self.page = await self.context.new_page()

    async def navigate_to(self, url: str) -> None:
        """Navigate to a URL."""
        if not self.page:
            raise RuntimeError("Browser not initialized. Call setup_browser() first.")
        
        await self.page.goto(url, wait_until="networkidle")

    async def capture_screenshot(self, name: str = "screenshot") -> str:
        """
        Capture screenshot.
        
        Args:
            name: Screenshot name
            
        Returns:
            Path to captured screenshot
        """
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        # Ensure screenshots directory exists
        screenshots_dir = Path("reports/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        screenshot_path = screenshots_dir / f"{name}.png"
        await self.page.screenshot(path=str(screenshot_path), full_page=True)
        
        return str(screenshot_path)

    async def wait_for_element(self, selector: str, timeout: int = 30000) -> None:
        """Wait for element to be visible."""
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def click_element(self, selector: str) -> None:
        """Click an element."""
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        await self.page.click(selector)

    async def type_text(self, selector: str, text: str) -> None:
        """Type text into an element."""
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        await self.page.fill(selector, text)

    async def get_text(self, selector: str) -> str:
        """Get text content from an element."""
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        element = await self.page.query_selector(selector)
        if element:
            return await element.text_content() or ""
        return ""

    async def wait_for_ai_response(
        self, 
        response_selector: str, 
        timeout: int = 30000
    ) -> str:
        """
        Wait for AI response with content stabilization.
        
        Args:
            response_selector: CSS selector for response element
            timeout: Maximum wait time in milliseconds
            
        Returns:
            Response content
        """
        if not self.page:
            raise RuntimeError("Page not initialized")
        
        # Wait for element to appear
        await self.page.wait_for_selector(response_selector, timeout=timeout)
        
        # Wait for content to stabilize (AI responses may stream)
        await self._wait_for_content_stabilization(response_selector)
        
        return await self.get_text(response_selector)

    async def _wait_for_content_stabilization(
        self, 
        selector: str, 
        stable_duration: float = 2.0,
        max_wait: float = 30.0
    ) -> None:
        """Wait for element content to stabilize."""
        import time
        
        start_time = time.time()
        last_content = ""
        stable_start = None
        
        while time.time() - start_time < max_wait:
            current_content = await self.get_text(selector)
            
            if current_content == last_content:
                if stable_start is None:
                    stable_start = time.time()
                elif time.time() - stable_start >= stable_duration:
                    break
            else:
                stable_start = None
                last_content = current_content
            
            await asyncio.sleep(0.5)

    async def cleanup_browser(self) -> None:
        """Clean up browser resources."""
        try:
            if self.page and not self.page.is_closed():
                await self.page.close()
        except:
            pass
        
        try:
            if self.context:
                await self.context.close()
        except:
            pass
        
        try:
            if self.browser:
                await self.browser.close()
        except:
            pass
        
        try:
            if self.playwright:
                await self.playwright.stop()
        except:
            pass
        
        # Reset all references
        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup_browser()
