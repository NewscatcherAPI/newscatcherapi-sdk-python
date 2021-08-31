import os
import unittest

from newscatcherapi.newscatcherapi_client import NewsCatcherApiClient


class NewsCatcherApiTest(unittest.TestCase):
    def setUp(self):
        key = os.environ.get("newscatcher_api_secret")
        self.api = NewsCatcherApiClient(key)

    def test_api_latest_headlines(self):
        # Raise TypeError if lang is not of type str
        lang = 1
        with self.assertRaises(TypeError):
            self.api.get_latest_headlines(lang=lang)

        # Raise ValueError if lang is not in list
        lang = 'aer'
        with self.assertRaises(ValueError):
            self.api.get_latest_headlines(lang=lang)

        # Raise TypeError if not_lang is not of type str
        not_lang = 1
        with self.assertRaises(TypeError):
            self.api.get_latest_headlines(not_lang=not_lang)

        # Raise ValueError if lang is not in list
        not_lang = 'aer'
        with self.assertRaises(ValueError):
            self.api.get_latest_headlines(not_lang=not_lang)

        # Raise TypeError if sources param is not of type str
        sources = 0
        with self.assertRaises(TypeError):
            self.api.get_latest_headlines(sources=sources)

        # Raise TypeError if country param is not of type str
        countries = 0
        with self.assertRaises(TypeError):
            self.api.get_latest_headlines(countries=countries)

        # Raises TypeError if topic param is not of type str
        topic = 0
        with self.assertRaises(TypeError):
            self.api.get_latest_headlines(topic=topic)

        # Raises ValueError if category param is invalid
        topic = "dogcoin"
        with self.assertRaises(ValueError):
            self.api.get_latest_headlines(topic=topic)

        # Raises TypeError if page_size param is not an int
        page_size = "1"
        with self.assertRaises(TypeError):
            self.api.get_latest_headlines(page_size=page_size)

        # Raises ValueError if page_size param is less than zero(0) or greater than 100
        page_size = -1
        with self.assertRaises(ValueError):
            self.api.get_latest_headlines(page_size=page_size)

        page_size = 1000
        with self.assertRaises(ValueError):
            self.api.get_latest_headlines(page_size=page_size)

        # Raises a TypeError is page param is not an int
        page = "1"
        with self.assertRaises(TypeError):
            self.api.get_latest_headlines(page=page)

        # Raises a ValueError if page param is less than zero(0)
        page = -1
        with self.assertRaises(ValueError):
            self.api.get_latest_headlines(page=page)

    def test_api_get_search(self):
        # Raise TypeError if q param is None
        q = 0
        with self.assertRaises(TypeError):
            self.api.get_search(q=q)

        # Raise TypeError if lang is not of type str
        lang = 1
        with self.assertRaises(TypeError):
            self.api.get_search(lang=lang)

        # Raise ValueError if lang is not in list
        lang = 'aer'
        with self.assertRaises(ValueError):
            self.api.get_search(lang=lang)

        # Raise TypeError if not_lang is not of type str
        not_lang = 1
        with self.assertRaises(TypeError):
            self.api.get_search(not_lang=not_lang)

        # Raise ValueError if lang is not in list
        not_lang = 'aer'
        with self.assertRaises(ValueError):
            self.api.get_search(not_lang=not_lang)

        # Raise TypeError if sources param is not of type str
        sources = 0
        with self.assertRaises(TypeError):
            self.api.get_search(sources=sources)

        # Raise TypeError if country param is not of type str
        countries = 0
        with self.assertRaises(TypeError):
            self.api.get_search(countries=countries)

        # Raise TypeError if not_countries param is not of type str
        not_countries = 0
        with self.assertRaises(TypeError):
            self.api.get_search(not_countries=not_countries)

        # Raises TypeError if topic param is not of type str
        topic = 0
        with self.assertRaises(TypeError):
            self.api.get_search(topic=topic)

        # Raises ValueError if category param is invalid
        topic = "dogcoin"
        with self.assertRaises(ValueError):
            self.api.get_search(topic=topic)

        # Raises TypeError if page_size param is not an int
        page_size = "1"
        with self.assertRaises(TypeError):
            self.api.get_search(page_size=page_size)

        # Raises ValueError if page_size param is less than zero(0) or greater than 100
        page_size = -1
        with self.assertRaises(ValueError):
            self.api.get_search(page_size=page_size)

        page_size = 1000
        with self.assertRaises(ValueError):
            self.api.get_search(page_size=page_size)

        # Raises a TypeError is page param is not an int
        page = "1"
        with self.assertRaises(TypeError):
            self.api.get_search(page=page)

        # Raises a ValueError if page param is less than zero(0)
        page = -1
        with self.assertRaises(ValueError):
            self.api.get_search(page=page)

        # Raise TypeError is sort_by param is not of type str
        sort_by = 1
        with self.assertRaises(TypeError):
            self.api.get_search(sort_by=sort_by)

        # Raise ValueError if soft_by param is invalid
        sort_by = "sort"
        with self.assertRaises(ValueError):
            self.api.get_search(sort_by=sort_by)


        # Raise ValueError if soft_by param is invalid
        published_date_precision = "score"
        with self.assertRaises(ValueError):
            self.api.get_search(published_date_precision=published_date_precision)

        # Raise ValueError if soft_by param is invalid
        search_in = "published_date"
        with self.assertRaises(ValueError):
            self.api.get_search(search_in=search_in)


        # Raises a TypeError is from_rank param is not an int
        from_rank = "1"
        with self.assertRaises(TypeError):
            self.api.get_search(from_rank=from_rank)

        # Raises a TypeError is from_rank param is not an int
        to_rank = "1"
        with self.assertRaises(TypeError):
            self.api.get_search(to_rank=to_rank)

    def test_api_get_sources(self):
        # Raise TypeError if not_countries param is not of type str
        not_countries = 0
        with self.assertRaises(TypeError):
            self.api.get_search(not_countries=not_countries)

        # Raises TypeError if topic param is not of type str
        topic = 0
        with self.assertRaises(TypeError):
            self.api.get_search(topic=topic)

        # Raises ValueError if category param is invalid
        topic = "dogcoin"
        with self.assertRaises(ValueError):
            self.api.get_search(topic=topic)
