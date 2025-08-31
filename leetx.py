# VERSION: 1.0
# AUTHORS: AI Assistant (based on hemantapkh/1337x API)

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

    def parseResults(self, results):
        if not results or not hasattr(results, 'items') or not results.items:
            return
        
        for torrent in results.items:
            try:
                data = {
                    'link': torrent.url,
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
                self.parseResults(mock_results)
                
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