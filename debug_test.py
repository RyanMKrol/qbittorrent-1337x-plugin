#!/usr/bin/env python3

import asyncio
from py1337x import AsyncPy1337x, category, sort

async def debug_api():
    print("Testing 1337x API directly...")
    
    torrents = AsyncPy1337x()
    
    try:
        print("Searching for 'ubuntu' without category filter...")
        results = await torrents.search('ubuntu')
        
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
                        info = await torrents.info(link=torrent.url)
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
    asyncio.run(debug_api())