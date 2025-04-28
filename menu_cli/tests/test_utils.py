from unittest import TestCase
from utils import get_content_type
from pathlib import Path


class TestUtils(TestCase):
    def test_get_content_type(self):
        content_type = get_content_type(
            Path("/Users/pete.jeffryes/Desktop/recipes/Red Chimichurri.pdf")
        )
        self.assertEqual(content_type, "application/pdf")
