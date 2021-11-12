# NetSurf RSS

Giving [an awesome browser's news feed][news] the RSS feed it always deserved.

Steals code from:
- https://github.com/SuperSonicHub1/CRManga-RSS

## Install
```bash
poetry install
# For the lazy...
python3 main.py 
# For the more upstanding
gunicorn 'netsurf_rss:create_app()'
```

[news]: https://www.netsurf-browser.org/about/news.html
