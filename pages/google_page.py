"""Google search page object for demonstration."""

from framework.page_base import PageBase


class GooglePage(PageBase):
    """Google search page object."""
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://www.google.com"
        
        # Locators for Google page elements
        self.search_input = "textarea[name='q']"
        self.search_button = "input[name='btnK']"
        self.lucky_button = "input[name='btnI']"
        self.results_stats = "#result-stats"
    
    async def search(self, query: str) -> None:
        """Perform a search on Google."""
        await self.wait_for_element(self.search_input)
        await self.type(self.search_input, query)
        await self.page.keyboard.press("Enter")
        await self.page.wait_for_load_state("networkidle")
    
    async def get_search_results_count(self) -> str:
        """Get the search results statistics text."""
        try:
            await self.wait_for_element(self.results_stats, timeout=10000)
            return await self.get_text(self.results_stats)
        except:
            return "Results count not found"
    
    async def is_search_box_visible(self) -> bool:
        """Check if the search box is visible."""
        return await self.is_visible(self.search_input)
