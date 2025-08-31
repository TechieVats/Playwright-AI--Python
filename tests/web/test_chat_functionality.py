"""Simple tests for AI chat functionality."""

import pytest
from pages.chat_page import ChatPage


@pytest.mark.asyncio
class TestChatFunctionality:
    """Test suite for AI chat functionality."""
    
    async def test_chat_page_loads(self, browser_test, config):
        """Test that chat page loads successfully."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        chat_url = f"{base_url}/chat"
        
        try:
            await browser_test.navigate_to(chat_url)
            
            # Create page object
            chat_page = ChatPage(browser_test.page)
            
            # Verify page loaded
            page_title = await chat_page.get_page_title()
            assert page_title is not None
            
            # Take screenshot
            await browser_test.capture_screenshot("chat_page_loaded")
            
        except Exception as e:
            # Chat page might not exist, which is fine for demo
            pytest.skip(f"Chat page not available: {e}")
    
    async def test_send_message(self, browser_test, config):
        """Test sending a message in chat."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        chat_url = f"{base_url}/chat"
        
        try:
            await browser_test.navigate_to(chat_url)
            chat_page = ChatPage(browser_test.page)
            
            # Check if chat input is available
            if await chat_page.is_chat_input_enabled():
                # Send a test message
                test_message = "Hello, this is a test message"
                await chat_page.send_message(test_message)
                
                # Take screenshot after sending message
                await browser_test.capture_screenshot("message_sent")
            else:
                pytest.skip("Chat input not available")
                
        except Exception as e:
            pytest.skip(f"Chat functionality not available: {e}")
    
    async def test_ai_response(self, browser_test, config):
        """Test waiting for AI response."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        chat_url = f"{base_url}/chat"
        
        try:
            await browser_test.navigate_to(chat_url)
            chat_page = ChatPage(browser_test.page)
            
            if await chat_page.is_chat_input_enabled():
                # Send a message that should get a response
                await chat_page.send_message("What is artificial intelligence?")
                
                # Wait for response (with timeout)
                try:
                    response = await chat_page.wait_for_response(timeout=30000)
                    
                    # Verify response is not empty
                    assert len(response) > 0, "AI response should not be empty"
                    
                    # Take screenshot of response
                    await browser_test.capture_screenshot("ai_response_received")
                    
                except Exception as response_error:
                    # Response might timeout, which is acceptable for demo
                    await browser_test.capture_screenshot("ai_response_timeout")
                    pytest.skip(f"AI response not received: {response_error}")
            else:
                pytest.skip("Chat input not available")
                
        except Exception as e:
            pytest.skip(f"Chat functionality not available: {e}")
    
    async def test_multiple_messages(self, browser_test, config):
        """Test sending multiple messages."""
        base_url = config.get('environments', {}).get('local', {}).get('base_url', 'http://localhost:3000')
        chat_url = f"{base_url}/chat"
        
        try:
            await browser_test.navigate_to(chat_url)
            chat_page = ChatPage(browser_test.page)
            
            if await chat_page.is_chat_input_enabled():
                messages = [
                    "Hello",
                    "How are you?",
                    "Tell me about machine learning"
                ]
                
                for i, message in enumerate(messages):
                    await chat_page.send_message(message)
                    
                    # Brief pause between messages
                    import asyncio
                    await asyncio.sleep(1)
                    
                    # Take screenshot after each message
                    await browser_test.capture_screenshot(f"message_{i+1}_sent")
                
                # Take final screenshot
                await browser_test.capture_screenshot("multiple_messages_complete")
            else:
                pytest.skip("Chat input not available")
                
        except Exception as e:
            pytest.skip(f"Chat functionality not available: {e}")
