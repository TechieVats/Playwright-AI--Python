# Playwright AI Test Framework

A simple test automation framework for testing web applications and AI chatbots using Python and Playwright.

## What is this?

This framework helps you automatically test websites and web applications, especially those with AI features like chatbots. Instead of manually clicking through your website every time you make changes, you can write automated tests that do it for you.

## What can it do?

- Test web pages automatically
- Test AI chatbots and their responses
- Take screenshots when tests fail
- Test on different screen sizes (mobile, tablet, desktop)
- Generate test reports
- Work with different browsers (Chrome, Firefox, Safari)

## Prerequisites

Before you start, make sure you have:
- Python 3.8 or newer installed on your computer
- Basic knowledge of Python
- A web application to test (or you can test any public website)

## Getting Started

### Step 1: Download and Setup

1. Download or clone this project to your computer
2. Open a terminal/command prompt and navigate to the project folder
3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Install the browsers for testing:

```bash
playwright install
```

### Step 2: Configure Your Tests

1. Open the `config/config.yaml` file
2. Change the `base_url` to point to your website:

```yaml
environments:
  local:
    base_url: "http://your-website.com"  # Change this to your website
```

### Step 3: Run Your First Test

Run all tests:
```bash
pytest
```

Run tests and see the browser (not hidden):
```bash
pytest --headless=false
```

Generate a report:
```bash
pytest --html=reports/report.html
```

## Understanding the Project Structure

```
Playwright-AI--Python/
├── framework/          # The main testing code (you usually don't need to change this)
├── pages/             # Page objects - represents different pages of your website
├── tests/             # Your actual test files
├── config/            # Settings and configuration
├── reports/           # Test results and screenshots
└── requirements.txt   # List of required Python packages
```

## Writing Your First Test

### Simple Example

Create a new file in the `tests/web/` folder called `test_my_website.py`:

```python
import pytest

@pytest.mark.asyncio
async def test_website_loads(browser_test, config):
    """Test that the website loads successfully"""
    
    # Go to your website
    base_url = config['environments']['local']['base_url']
    await browser_test.navigate_to(base_url)
    
    # Check that the page has a title
    page_title = await browser_test.page.title()
    assert len(page_title) > 0, "Page should have a title"
    
    # Take a screenshot
    await browser_test.capture_screenshot("website_loaded")
    
    print(f"Success! Website loaded with title: {page_title}")
```

### Testing a Chatbot

If your website has a chatbot, create `test_chatbot.py`:

```python
import pytest
from pages.chat_page import ChatPage

@pytest.mark.asyncio
async def test_chatbot_responds(browser_test, config):
    """Test that the chatbot responds to messages"""
    
    # Go to the chat page
    base_url = config['environments']['local']['base_url']
    await browser_test.navigate_to(f"{base_url}/chat")
    
    # Create a chat page object
    chat_page = ChatPage(browser_test.page)
    
    # Send a message
    await chat_page.send_message("Hello!")
    
    # Wait for response
    response = await chat_page.wait_for_response()
    
    # Check that we got a response
    assert len(response) > 0, "Chatbot should respond"
    
    print(f"Chatbot responded: {response}")
```

## Creating Page Objects

Page objects help organize your tests. They represent different pages of your website.

Create a new file in `pages/` folder:

```python
from framework.page_base import PageBase

class LoginPage(PageBase):
    def __init__(self, page):
        super().__init__(page)
        self.url = "/login"
        
        # Define the elements on this page
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_button = "#login-btn"
    
    async def login(self, username, password):
        """Log in with username and password"""
        await self.type(self.username_input, username)
        await self.type(self.password_input, password)
        await self.click(self.login_button)
```

Then use it in your tests:

```python
from pages.login_page import LoginPage

@pytest.mark.asyncio
async def test_login(browser_test, config):
    base_url = config['environments']['local']['base_url']
    await browser_test.navigate_to(base_url)
    
    login_page = LoginPage(browser_test.page)
    await login_page.navigate()
    await login_page.login("testuser", "testpass")
```

## Running Different Types of Tests

### Run specific test files:
```bash
pytest tests/web/test_my_website.py
```

### Run tests with specific tags:
```bash
pytest -m smoke    # Run only smoke tests
pytest -m web      # Run only web tests
pytest -m chat     # Run only chat tests
```

### Run tests and see what's happening:
```bash
pytest -v -s      # Verbose output with print statements
```

## Understanding Test Results

After running tests, you'll see:
- **Green dots (.)**: Tests passed
- **Red F**: Tests failed
- **Yellow s**: Tests skipped

Screenshots are saved in `reports/screenshots/` folder.

## Common Issues and Solutions

### "Browser not found" error
```bash
playwright install
```

### Tests are too slow
Edit `config/config.yaml` and increase the timeout:
```yaml
test_settings:
  timeout: 60000  # 60 seconds
```

### Want to see the browser while testing
Edit `config/config.yaml`:
```yaml
browser:
  headless: false
```

### Tests fail because elements are not found
- Check that your website is running
- Verify the element selectors in your page objects
- Use browser developer tools (F12) to find the correct selectors

## Tips for Beginners

1. **Start small**: Begin with simple tests that just check if pages load
2. **Use screenshots**: Add `await browser_test.capture_screenshot("test_name")` to see what's happening
3. **Run one test at a time**: Use `pytest tests/web/test_specific_file.py::test_specific_function`
4. **Check the reports folder**: Look at screenshots when tests fail
5. **Use print statements**: Add `print("Got here!")` to debug your tests

## Getting Help

1. Check the `reports/` folder for screenshots and HTML reports
2. Run tests with `-v -s` flags to see detailed output
3. Make sure your website is accessible at the URL in config
4. Verify that the HTML elements exist on your page using browser developer tools

## Next Steps

Once you're comfortable with basic tests:
1. Add more page objects for different pages
2. Create test data files for different scenarios
3. Set up different environments (staging, production)
4. Add performance tests
5. Integrate with CI/CD pipelines

## Example Commands Cheat Sheet

```bash
# Install everything
pip install -r requirements.txt
playwright install

# Run tests
pytest                                    # All tests
pytest -v                                # Verbose output
pytest --html=reports/report.html        # With HTML report
pytest tests/web/test_home_page.py       # Specific file
pytest -m smoke                          # Only smoke tests

# Debug tests
pytest -v -s                             # See print statements
pytest --headless=false                  # See browser
pytest --pdb                             # Debug with Python debugger
```

This framework makes web testing easier and more reliable. Start with simple tests and gradually add more complex scenarios as you learn!