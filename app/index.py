import json
import logging
import re

import nltk
import txtai
from fast_autocomplete import AutoComplete
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)

video_emb = txtai.Embeddings()
logger.info('start loading video_index')
video_emb.load('./video_index')
logger.info('finished loading video_index')
config = video_emb.config.copy()
config.pop('ids', None)
logger.info(json.dumps(config, sort_keys=True, default=str, indent=2))

channel_emb = txtai.Embeddings()
logger.info('start loading channel_index')
channel_emb.load('./channel_index')
logger.info('finished loading channel_index')
config = channel_emb.config.copy()
config.pop('ids', None)
logger.info(json.dumps(config, sort_keys=True, default=str, indent=2))

logger.info('start loading autocomplete_quieries.json')
with open('./autocomplete_quieries.json') as json_file:
    autocomplete_titles = json.load(json_file)
autocomplete = AutoComplete(
    words=autocomplete_titles,
    valid_chars_for_string="абвгдеёжзийклмнопрстуфхцчшщьъыэюяabcdefghijklmnopqrstuvwxyz"
)
logger.info('finished loading autocomplete_quieries.json')

nltk.download('popular')


def clean_query(query: str):
    query = re.sub("[^а-яА-ЯЁё0-9a-zA-Z ]", "", query)
    query = re.sub(r'[^\w\s]', '', query.lower())
    tokens = nltk.word_tokenize(query)
    tokens = [word for word in tokens if word not in stopwords.words('russian')]
    result = ' '.join(tokens)
    logger.info(f'clean text: query={query}, result={result}')
    return result


def search_videos(query: str, limit: int = 10):
    query = clean_query(query)
    results = video_emb.search(
        f'select id, text, v_year_views, v_pub_datetime, score from txtai where similar("{query}") order by score desc, v_pub_datetime desc limit {limit}')
    logger.info(f'search videos: query={query}, limit={limit}, results={results}')
    return list(map(lambda r: {
        'id': r['id'],
        'title': r['text'],
        'publishedDateText': r['v_pub_datetime'],
        'viewCountText': r['v_year_views']
    }, results))


def search_channels(query: str, limit: int = 10):
    query = clean_query(query)
    results = channel_emb.search(
        f'select text, v_channel_type, score from txtai where similar("{query}") order by score desc limit {limit}'
    )
    logger.info(f'search channels: query={query}, limit={limit}, results={results}')
    return list(map(lambda r: {
        'title': r['text'],
        'type': r['v_channel_type']
    }, results))


def search_suggests(query: str, max_cost: int, limit: int):
    results = autocomplete.search(word=query, max_cost=max_cost, size=limit)
    logger.info(f'search suggests: query={query}, max_cost={max_cost}, limit={limit}, results={results}')
    return results
