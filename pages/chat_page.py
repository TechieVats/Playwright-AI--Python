"""Chat page object for AI chatbot testing."""

from framework.page_base import PageBase


class ChatPage(PageBase):
    """AI Chat page for testing chatbot functionality."""
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "/chat"
        
        # Locators
        self.chat_input = "[data-testid='chat-input']"
        self.send_button = "[data-testid='send-button']"
        self.chat_messages = "[data-testid='chat-messages']"
        self.latest_message = "[data-testid='chat-messages'] .message:last-child"
        self.typing_indicator = "[data-testid='typing-indicator']"
        self.clear_chat_button = "[data-testid='clear-chat']"
    
    async def send_message(self, message: str) -> None:
        """Send a message in the chat."""
        await self.type(self.chat_input, message)
        await self.click(self.send_button)
    
    async def get_latest_message(self) -> str:
        """Get the latest message in the chat."""
        await self.wait_for_element(self.latest_message)
        return await self.get_text(self.latest_message)
    
    async def wait_for_response(self, timeout: int = 30000) -> str:
        """Wait for AI response and return it."""
        # Wait for typing indicator to appear (optional)
        try:
            await self.wait_for_element(self.typing_indicator, timeout=5000)
        except:
            pass  # Typing indicator might not appear
        
        # Wait for new message
        await self.wait_for_element(self.latest_message, timeout=timeout)
        
        # Wait for content to stabilize (AI responses may stream)
        import asyncio
        await asyncio.sleep(2)
        
        return await self.get_latest_message()
    
    async def clear_chat(self) -> None:
        """Clear the chat history."""
        if await self.is_visible(self.clear_chat_button):
            await self.click(self.clear_chat_button)
    
    async def is_chat_input_enabled(self) -> bool:
        """Check if chat input is enabled."""
        element = await self.page.query_selector(self.chat_input)
        return element is not None and await element.is_enabled()
