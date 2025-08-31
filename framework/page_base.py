"""Base page class for page object pattern."""

from typing import Optional
from playwright.async_api import Page


class PageBase:
    """
    Base page class for implementing page object pattern.
    
    Provides common page interaction methods.
    """

    def __init__(self, page: Page):
        self.page = page
        self.url = ""

    async def navigate(self, url: Optional[str] = None) -> None:
        """Navigate to the page URL."""
        target_url = url or self.url
        if not target_url:
            raise ValueError("No URL specified")
        
        await self.page.goto(target_url, wait_until="networkidle")

    async def click(self, selector: str) -> None:
        """Click an element."""
        await self.page.click(selector)

    async def type(self, selector: str, text: str) -> None:
        """Type text into an element."""
        await self.page.fill(selector, text)

    async def get_text(self, selector: str) -> str:
        """Get text from an element."""
        element = await self.page.query_selector(selector)
        if element:
            return await element.text_content() or ""
        return ""

    async def wait_for_element(self, selector: str, timeout: int = 30000) -> None:
        """Wait for element to be visible."""
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def is_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        try:
            element = await self.page.query_selector(selector)
            return element is not None and await element.is_visible()
        except:
            return False

    async def get_page_title(self) -> str:
        """Get page title."""
        return await self.page.title()

    async def get_current_url(self) -> str:
        """Get current URL."""
        return self.page.url
