"""
Simple Playwright Test Framework for AI/ML Web Applications

A lightweight Python-based test automation framework built on Playwright
for testing web applications, especially those with AI/ML components.
"""

__version__ = "1.0.0"
__author__ = "AI Test Framework Team"

from .base_test import BaseTest
from .page_base import PageBase

__all__ = ["BaseTest", "PageBase"]