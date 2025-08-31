"""Simple pytest configuration and fixtures."""

import pytest
import pytest_asyncio
import yaml
from pathlib import Path
from typing import AsyncGenerator

from framework.base_test import BaseTest


def load_config():
    """Load configuration from YAML file."""
    config_path = Path("config/config.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


@pytest.fixture(scope="session")
def config():
    """Provide configuration for tests."""
    return load_config()


@pytest_asyncio.fixture(scope="function")
async def browser_test(config) -> AsyncGenerator[BaseTest, None]:
    """
    Provide BaseTest instance with browser setup and cleanup.
    """
    test = BaseTest()
    
    # Get browser configuration
    browser_config = config.get('browser', {})
    
    try:
        # Setup browser
        await test.setup_browser(
            browser_name=browser_config.get('name', 'chromium'),
            headless=browser_config.get('headless', True),
            viewport=browser_config.get('viewport')
        )
        
        yield test
        
    finally:
        # Cleanup browser
        await test.cleanup_browser()


@pytest.fixture(autouse=True)
def setup_test_directories():
    """Create necessary test directories."""
    directories = [
        "reports",
        "reports/screenshots"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)