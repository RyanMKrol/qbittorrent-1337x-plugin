#!/usr/bin/env python3

# Mock novaprinter for testing
class MockNovaPrinter:
    @staticmethod
    def prettyPrinter(data):
        print(f"TORRENT RESULT:")
        print(f"  Name: {data.get('name', 'Unknown')}")
        print(f"  Link: {data.get('link', 'No link')[:100]}...")
        print(f"  Size: {data.get('size', 'Unknown')}")
        print(f"  Seeds: {data.get('seeds', '0')}")
        print(f"  Leech: {data.get('leech', '0')}")
        print(f"  Engine URL: {data.get('engine_url', 'Unknown')}")
        print(f"  Description Link: {data.get('desc_link', 'No link')}")
        print("-" * 50)

# Replace the novaprinter import in our plugin
import sys
sys.modules['novaprinter'] = MockNovaPrinter()

# Now import our plugin
from leetx import leetx

def test_search():
    print("Testing qBittorrent 1337x Plugin")
    print("=" * 50)
    
    plugin = leetx()
    
    # Test with a simple search query
    print("Searching for 'ubuntu'...")
    plugin.search('ubuntu')
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_search()