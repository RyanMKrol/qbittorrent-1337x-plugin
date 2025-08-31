#!/usr/bin/env python3

from py1337x import Py1337x

def test_sync_api():
    print("Testing synchronous 1337x API...")
    
    torrents = Py1337x()
    
    try:
        print("Searching for 'ubuntu' with sync API...")
        results = torrents.search('ubuntu')
        
        if results:
            print(f"Found {len(results.items) if hasattr(results, 'items') and results.items else 0} results")
            
            if hasattr(results, 'items') and results.items:
                for i, torrent in enumerate(results.items[:3]):  # Show first 3
                    print(f"\nTorrent {i+1}:")
                    print(f"  Name: {getattr(torrent, 'name', 'No name')}")
                    print(f"  URL: {getattr(torrent, 'url', 'No URL')}")
                    print(f"  Seeders: {getattr(torrent, 'seeders', 'No seeders')}")
                    print(f"  Size: {getattr(torrent, 'size', 'No size')}")
                    
                    # Try to get detailed info
                    try:
                        print("  Getting detailed info...")
                        info = torrents.info(link=torrent.url)
                        if info:
                            print(f"  Magnet: {getattr(info, 'magnet', 'No magnet')[:100]}...")
                        else:
                            print("  No detailed info returned")
                    except Exception as e:
                        print(f"  Error getting detailed info: {e}")
            else:
                print("No items in results")
        else:
            print("No results returned")
            
    except Exception as e:
        print(f"Error during search: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sync_api()