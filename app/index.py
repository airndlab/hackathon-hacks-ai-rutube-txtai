import json
import logging

import txtai

logger = logging.getLogger(__name__)

embeddings = txtai.Embeddings()
logger.info('start loading')
embeddings.load('./index')
logger.info('finished loading')
config = embeddings.config.copy()
config.pop("ids", None)
logger.info(json.dumps(config, sort_keys=True, default=str, indent=2))


def search(query: str, limit: int = 10):
    results = embeddings.search(
        f'select id, text, v_year_views, v_pub_datetime, score from txtai where similar("{query}") order by score desc, v_pub_datetime desc limit {limit}')
    return list(map(lambda r: {
        'id': r['id'],
        'title': r['text'],
        'publishedDateText': r['v_pub_datetime'],
        'viewCountText': r['v_year_views']
    }, results))
