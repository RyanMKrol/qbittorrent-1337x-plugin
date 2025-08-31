# VERSION: 1.0
# AUTHORS: Ryan Krol (based on hemantapkh/1337x API)
# LICENSE: MIT License

try:
    from py1337x import AsyncPy1337x, category, sort
    import asyncio
except ImportError:
    import sys
    print("py1337x module not found. Install with: pip install 1337x", file=sys.stderr)
    sys.exit(1)

from novaprinter import prettyPrinter


class leetx(object):
    url = 'https://1337x.to/'
    name = '1337x'
    supported_categories = {
        'all': '0'
    }

    def __init__(self):
        self.torrents_api = AsyncPy1337x()

    async def parseResults(self, results):
        if not results or not hasattr(results, 'items') or not results.items:
            return
        
        # Create tasks to get magnet links concurrently
        magnet_tasks = []
        for torrent in results.items:
            magnet_tasks.append(self._get_magnet_link(torrent))
        
        # Get all magnet links concurrently
        magnet_results = await asyncio.gather(*magnet_tasks, return_exceptions=True)
        
        # Process results
        for torrent, magnet_result in zip(results.items, magnet_results):
            try:
                # Skip if magnet link fetch failed
                if isinstance(magnet_result, Exception) or not magnet_result:
                    continue
                
                data = {
                    'link': magnet_result,
                    'name': torrent.name,
                    'size': str(torrent.size),
                    'seeds': str(torrent.seeders),
                    'leech': str(torrent.leechers),
                    'engine_url': self.url,
                    'desc_link': torrent.url,
                    'pub_date': "-1"
                }
                prettyPrinter(data)
            except Exception:
                continue
    
    async def _get_magnet_link(self, torrent):
        try:
            # Try using torrent_id first, fallback to link
            torrent_info = None
            if hasattr(torrent, 'torrent_id'):
                torrent_info = await self.torrents_api.info(torrent_id=torrent.torrent_id)
            else:
                torrent_info = await self.torrents_api.info(link=torrent.url)
            
            # The magnet link property might be 'magnet' or 'magnet_link'
            if torrent_info:
                return (getattr(torrent_info, 'magnet', None) or 
                       getattr(torrent_info, 'magnet_link', None))
            return None
        except Exception as e:
            print(f"Error getting magnet for {getattr(torrent, 'name', 'unknown')}: {e}")
            return None

    def search(self, what, cat='all'):
        try:
            asyncio.run(self._async_search(what, cat))
        except Exception:
            return
    
    async def _async_search(self, what, cat='all'):
        try:
            # Define all categories to search
            categories_to_search = [
                category.MOVIES,
                category.TV,
                category.GAMES,
                category.MUSIC,
                category.APPS,
                category.ANIME
            ]
            
            all_torrents = []
            seen_ids = set()
            
            # Create tasks for concurrent searching
            search_tasks = []
            
            for search_category in categories_to_search:
                # Add task for searching by seeders
                search_tasks.append(
                    self._search_category(what, search_category, sort.SEEDERS)
                )
                # Add task for searching by size
                search_tasks.append(
                    self._search_category(what, search_category, sort.SIZE)
                )
            
            # Execute all searches concurrently
            results_list = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            # Process results
            for results in results_list:
                if isinstance(results, Exception):
                    continue
                if results and results.items:
                    for torrent in results.items:
                        torrent_id = getattr(torrent, 'torrent_id', torrent.url)
                        if torrent_id not in seen_ids:
                            all_torrents.append(torrent)
                            seen_ids.add(torrent_id)
            
            # Create a mock results object to pass to parseResults
            if all_torrents:
                mock_results = type('MockResults', (), {'items': all_torrents})()
                await self.parseResults(mock_results)
                
        except Exception:
            return
    
    async def _search_category(self, what, search_category, sort_by):
        try:
            return await self.torrents_api.search(
                what, 
                category=search_category, 
                page=1, 
                sort_by=sort_by
            )
        except Exception:
            return None