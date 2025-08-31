# VERSION: 1.0
# AUTHORS: AI Assistant (based on hemantapkh/1337x API)

try:
    from py1337x import Py1337x, category, sort
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
        self.torrents_api = Py1337x()

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
            
            # Search each category with both sorting methods
            for search_category in categories_to_search:
                # Get first page sorted by seeders (highest first)
                try:
                    results = self.torrents_api.search(
                        what, 
                        category=search_category, 
                        page=1, 
                        sort_by=sort.SEEDERS
                    )
                    if results and results.items:
                        for torrent in results.items:
                            torrent_id = getattr(torrent, 'torrent_id', torrent.url)
                            if torrent_id not in seen_ids:
                                all_torrents.append(torrent)
                                seen_ids.add(torrent_id)
                except Exception:
                    pass
                
                # Get first page sorted by size (largest first)
                try:
                    results = self.torrents_api.search(
                        what, 
                        category=search_category, 
                        page=1, 
                        sort_by=sort.SIZE
                    )
                    if results and results.items:
                        for torrent in results.items:
                            torrent_id = getattr(torrent, 'torrent_id', torrent.url)
                            if torrent_id not in seen_ids:
                                all_torrents.append(torrent)
                                seen_ids.add(torrent_id)
                except Exception:
                    pass
            
            # Create a mock results object to pass to parseResults
            if all_torrents:
                mock_results = type('MockResults', (), {'items': all_torrents})()
                self.parseResults(mock_results)
            
        except Exception:
            return