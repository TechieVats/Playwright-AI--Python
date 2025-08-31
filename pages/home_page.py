"""Home page object."""

from framework.page_base import PageBase


class HomePage(PageBase):
    """Home page of the application."""
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "/"
        
        # Locators
        self.title_selector = "h1"
        self.navigation_menu = "[data-testid='nav-menu']"
        self.search_input = "[data-testid='search-input']"
        self.search_button = "[data-testid='search-button']"
        self.login_button = "[data-testid='login-button']"
    
    async def get_page_title_text(self) -> str:
        """Get the main title text."""
        return await self.get_text(self.title_selector)
    
    async def search(self, query: str) -> None:
        """Perform a search."""
        await self.type(self.search_input, query)
        await self.click(self.search_button)
    
    async def click_login(self) -> None:
        """Click the login button."""
        await self.click(self.login_button)
    
    async def is_navigation_visible(self) -> bool:
        """Check if navigation menu is visible."""
        return await self.is_visible(self.navigation_menu)
