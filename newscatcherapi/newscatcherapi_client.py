from __future__ import unicode_literals

import requests
import os
import sys
import time

sys.path.append(os.getcwd())


from newscatcherapi import const, utils
from newscatcherapi.newscatcherapi_auth import NewsCatcherApiAuth
from newscatcherapi.newscatcherapi_exception import NewsCatcherApiException


class NewsCatcherApiClient(object):
    """The core client object used to fetch data from NewsCatcher News API endpoints.

    :param api_key: Your API key, a length-32 UUID string provided for your NewsCatcher News API account.
        You must `register <https://app.newscatcherapi.com/auth/register>`_ for a NewsCatcher News API key.
    :type api_key: str

    :param session: An optional :class:`requests.Session` instance from which to execute requests.
        **Note**: If you provide a ``session`` instance, :class:`NewsCatcherApiClient` will *not* close the session
        for you.  Remember to call ``session.close()``, or use the session as a context manager, to close
        the socket and free up resources.
    :type session: `requests.Session <https://2.python-requests.org/en/master/user/advanced/#session-objects>`_ or None
    """

    def __init__(self, x_api_key, base_url='https://api.newscatcherapi.com', session=None):
        self.auth = NewsCatcherApiAuth(x_api_key=x_api_key)
        self.base_url = base_url
        if session is None:
            self.request_method = requests
        else:
            self.request_method = session

    def get_latest_headlines(
            self,
            lang=None,
            not_lang=None,
            countries=None,
            not_countries=None,
            topic=None,
            sources=None,
            not_sources=None,
            when=None,
            ranked_only=None,
            page_size=None,
            page=None,
            proxies=None
    ):
        """Call the `/latest_headlines` endpoint.

        Fetch live top and breaking headlines.

        Get the latest headlines given any topic, country, or language. Articles are sorted by the earliest
        date published first.

        :param lang: Specifies the languages of the search. For example: `en`. The only accepted format is [ISO 639-1 — 2](https://en.wikipedia.org/wiki/ISO_639-1) letter code.
        :type lang: list or str or None

        :param not_lang: Inverse to the `lang` parameter
        :type not_lang: list or str or None

        :param countries: Countries where the news publisher is located. **Important**: This parameter is not responsible for the countries mentioned in the news article. One or multiple countries can be used in the search. The only acceptable format is [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) For example, `US,CA,MX` or just `US`
        :type countries: list or str or None

        :param not_countries: The inverse of the `countries` parameter.
        :type not_countries: list or str or None

        :param topic: Accepted values: `news`, `sport`, `tech`, `world`, `finance`, `politics`, `business`, `economics`, `entertainment`, `beauty`, `travel`, `music`, `food`, `science`, `gaming`, `energy`. The topic to which you want to restrict the articles of your choice. Not all news articles are assigned with a topic, therefore, we cannot guarantee that 100% of topics talking about technology will be assigned a tech label.
        :type topic: str or None

        :param sources: One or more news resources to filter your search. It should be the normal form of the URL, For example: `nytimes.com,theguardian.com`
        :type sources: list or str or None

        :param not_sources: One or more sources to be excluded from the search. Comma-separated list. For example: `nytimes.com,cnn.com,wsj.com`
        :type not_sources: list or str or None

        :param when: The time period you want to get the latest headlines for. Accepted forms: 7d => Dailly Form (last 7 days time period),  30d  (last 30 days time period) | 1h => Hourly Form (last hour), 24h (last 24 hours)
        :type when: str or None

        :param ranked_only: Default: `True` Limit the search only for the sources which are in the top 1 million online websites. Unranked sources are assigned a rank that equals `999999`
        :type ranked_only: bool or None

        :param page_size: `[1:100]` How many articles to return per page.
        :type page_size: int or None

        :param page: The number of the page. Use it to scroll through the results. This parameter is used to paginate: scroll through results because one API response cannot return more than 100 articles.
        :type page: int or None

        :param proxies: Dict of proxies if needed
        :type proxies: dict or None

        :return: JSON response as nested Python dictionary.
        :rtype: dict
        :raises NewsCatcherApiException: If the ``"status"`` value of the response is ``"error"`` rather than ``"ok"``.
        """

        payload = {}


        # Language
        if lang is not None:
            payload["lang"] = utils.validate_language(lang)

        if not_lang is not None:
            payload["not_lang"] = utils.validate_language(not_lang)

        # Countries
        if countries is not None:
            payload["countries"] = utils.validate_countries(countries, 'countries')

        if not_countries is not None:
            payload["not_countries"] = utils.validate_countries(not_countries, 'not_countries')

        # Topic
        if topic is not None:
            payload['topic'] = utils.validate_topic(topic)

        # Sources
        if sources is not None:
            payload["sources"] = utils.validate_sources(sources, 'sources')

        if not_sources is not None:
            payload["not_sources"] = utils.validate_sources(not_sources, 'not_sources')

        # When
        if when is not None:
            payload["when"] = utils.validate_when(when, 'when')

        # Ranks
        if ranked_only is not None:
            if utils.is_valid_boolean(ranked_only):
                payload['ranked_only'] = ranked_only
            else:
                raise TypeError("ranked_only parameter should be of type boolean")

        # Page and page sizes
        # Page Size
        if page_size is not None:
            if type(page_size) == int:
                if 0 <= page_size <= 100:
                    payload["page_size"] = page_size
                else:
                    raise ValueError("page_size param should be an int between 1 and 100")
            else:
                raise TypeError("page_size param should be an int")

        # Page
        if page is not None:
            if type(page) == int:
                if page > 0:
                    payload["page"] = page
                else:
                    raise ValueError("page param should be an int greater than 0")
            else:
                raise TypeError("page param should be an int")

        # Send Request
        r = self.request_method.get(self.base_url + const.LATEST_HEADLINES_URL, auth=self.auth, timeout=30, params=payload, proxies=proxies)

        # Check Status of Request
        if r.status_code != requests.codes.ok:
            raise NewsCatcherApiException(r.json())

        return r.json()

    def get_search(
        self,
        q=None,
        lang=None,
        not_lang=None,
        from_=None,
        to_=None,
        published_date_precision=None,
        search_in=None,
        countries=None,
        not_countries=None,
        topic=None,
        sources=None,
        not_sources=None,
        ranked_only=None,
        from_rank=None,
        to_rank=None,
        sort_by=None,
        page_size=None,
        page=None,
        proxies=None
    ):
        """Call the `/search` endpoint.

        Main endpoint that allows you to find news article by keyword, date, language, country, etc.

        :param q: Keyword/keywords you're searching for. This is the most important part of your query. Please, refer to the **Advanced Query Parameter** section below for more examples and explanations.  (required)
        :type q: str or None

        :param lang: Specifies the languages of the search. For example: `en`. The only accepted format is [ISO 639-1 — 2](https://en.wikipedia.org/wiki/ISO_639-1) letter code.
        :type lang: list or str or None

        :param not_lang: Inverse to the `lang` parameter
        :type not_lang: list or str or None

        :param from_: `YYYY/mm/dd` From which point in time to start the search. The default timezone is UTC. Defaults to the past week.
        :type from_: str or None

        :param to_: `YYYY/mm/dd` Until which point in time to search for. The default timezone is UTC.
        :type to_: str or None

        :param published_date_precision: There are 3 types of date precision we define: `full` — day and time of an article is correctly identified with the appropriate timezone `timezone unknown` — day and time of an article is correctly identified without timezone `date` — only the day is identified without an exact time
        :type published_date_precision: str or None

        :param search_in: By default, we search what you specified in the `q` parameter in both `title` and `summary` of the article. However, you can limit this to either `title` or `summary`
        :type search_in: str or None

        :param countries: Countries where the news publisher is located. **Important**: This parameter is not responsible for the countries mentioned in the news article. One or multiple countries can be used in the search. The only acceptable format is [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) For example, `US,CA,MX` or just `US`
        :type countries: list or str or None

        :param not_countries: The inverse of the `countries` parameter.
        :type not_countries: list or str or None

        :param topic: Accepted values: `news`, `sport`, `tech`, `world`, `finance`, `politics`, `business`, `economics`, `entertainment`, `beauty`, `travel`, `music`, `food`, `science`, `gaming`, `energy`. The topic to which you want to restrict the articles of your choice. Not all news articles are assigned with a topic, therefore, we cannot guarantee that 100% of topics talking about technology will be assigned a tech label.
        :type topic: str or None

        :param sources: One or more news resources to filter your search. It should be the normal form of the URL, For example: `nytimes.com,theguardian.com`
        :type sources: list or str or None

        :param not_sources: One or more sources to be excluded from the search. Comma-separated list. For example: `nytimes.com,cnn.com,wsj.com`
        :type not_sources: list or str or None

        :param ranked_only: Default: `True` Limit the search only for the sources which are in the top 1 million online websites. Unranked sources are assigned a rank that equals `999999`
        :type ranked_only: bool or None

        :param from_rank: `[0:999999]` The lowest boundary of the rank of a news website to filter by. Important: lower rank means that a source is more popular
        :type from_rank: int or None

        :param to_rank: `[0:999999]` The upper boundary of the rank of a news website to filter by.
        :type to_rank: int or None

        :param sort_by: `relevancy` (default value) — the most relevant results first `date` — the most recently published results first `rank` — the results from the highest-ranked sources first
        :type sort_by: str or None

        :param page_size: `[1:100]` How many articles to return per page.
        :type page_size: int or None

        :param page: The number of the page. Use it to scroll through the results. This parameter is used to paginate: scroll through results because one API response cannot return more than 100 articles.
        :type page: int or None

        :param proxies: Dict of proxies if needed
        :type proxies: dict or None


        :return: JSON response as nested Python dictionary.
        :rtype: dict
        :raises NewsCatcherApiException: If the ``"status"`` value of the response is ``"error"`` rather than ``"ok"``.
        """

        payload = {}

        # Q
        if q is not None:
            if utils.is_valid_string(q):
                payload["q"] = q
            else:
                raise TypeError("q parameter should be of type str")

        # Language
        if lang is not None:
            payload["lang"] = utils.validate_language(lang)

        if not_lang is not None:
            payload["not_lang"] = utils.validate_language(not_lang)

        # Time variables
        if from_ is not None:
            if utils.is_valid_string(from_):
                payload["from"] = from_
            else:
                raise TypeError("from_ parameter should be of type str")

        if to_ is not None:
            if utils.is_valid_string(to_):
                payload["to"] = to_
            else:
                raise TypeError("to_ parameter should be of type str")

        if published_date_precision is not None:
            if utils.is_valid_string(published_date_precision):
                if published_date_precision in const.allowed_precisions:
                    payload["published_date_precision"] = published_date_precision
                else:
                    raise ValueError(f'{published_date_precision} is not a valid date precision. '
                                     f'It should be one of the list: {str(const.allowed_precisions)}')
            else:
                raise TypeError("published_date_precision parameter should be of type str")

        # Search in
        if search_in is not None:
            if utils.is_valid_string(search_in):
                if search_in in const.allowed_search_ins:
                    payload["search_in"] = search_in
                else:
                    raise ValueError(f'{search_in} is not a valid place to search for keywords. '
                                     f'It should be one of the list: {str(const.allowed_search_ins)}')
            else:
                raise TypeError("search_in parameter should be of type str")

        # Countries
        if countries is not None:
            payload["countries"] = utils.validate_countries(countries, 'countries')

        if not_countries is not None:
            payload["not_countries"] = utils.validate_countries(not_countries, 'not_countries')

        # Topic
        if topic is not None:
            payload['topic'] = utils.validate_topic(topic)

        # Sources
        if sources is not None:
            payload["sources"] = utils.validate_sources(sources, 'sources')

        if not_sources is not None:
            payload["not_sources"] = utils.validate_sources(not_sources, 'not_sources')


        # Ranks
        if ranked_only is not None:
            if utils.is_valid_boolean(ranked_only):
                payload['ranked_only'] = ranked_only
            else:
                raise TypeError("ranked_only parameter should be of type boolean")

        if from_rank is not None:
            if utils.is_valid_num(from_rank):
                payload['from_rank'] = from_rank
            else:
                raise TypeError("from_rank parameter should be of type int")

        if to_rank is not None:
            if utils.is_valid_num(to_rank):
                payload['to_rank'] = to_rank
            else:
                raise TypeError("to_rank parameter should be of type int")

        # Sort by
        if sort_by is not None:
            if utils.is_valid_string(sort_by):
                if sort_by in const.allowed_sorts:
                    payload["sort_by"] = sort_by
                else:
                    raise ValueError(f'{sort_by} is not a valid sort by type. '
                                     f'It should be one of the list: {str(const.allowed_sorts)}')
            else:
                raise TypeError("sort_by parameter should be of type str")

        # Page and page sizes
        # Page Size
        if page_size is not None:
            if type(page_size) == int:
                if 0 <= page_size <= 100:
                    payload["page_size"] = page_size
                else:
                    raise ValueError("page_size param should be an int between 1 and 100")
            else:
                raise TypeError("page_size param should be an int")

        # Page
        if page is not None:
            if type(page) == int:
                if page > 0:
                    payload["page"] = page
                else:
                    raise ValueError("page param should be an int greater than 0")
            else:
                raise TypeError("page param should be an int")

        # Send Request
        r = self.request_method.get(self.base_url + const.SEARCH_URL, auth=self.auth, timeout=30, params=payload, proxies=proxies)

        # Check Status of Request
        if r.status_code != requests.codes.ok:
            raise NewsCatcherApiException(r.json())

        return r.json()

    def get_sources(self,
                    lang=None,
                    countries=None,
                    topic=None,
                    proxies=None):
        """Call the `/sources` endpoint.

        Returns a list of the top 100 supported news websites. Overall, we support over 60,000 websites. Using this endpoint, you may find the top 100 for your specific language, country, topic combination.

        :param lang: Specifies the languages of the search. For example: `en`. The only accepted format is [ISO 639-1 — 2](https://en.wikipedia.org/wiki/ISO_639-1) letter code.
        :type lang: list or str or None

        :param countries: Countries where the news publisher is located. **Important**: This parameter is not responsible for the countries mentioned in the news article. One or multiple countries can be used in the search. The only acceptable format is [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) For example, `US,CA,MX` or just `US`
        :type countries: list or str or None

        :param topic: Accepted values: `news`, `sport`, `tech`, `world`, `finance`, `politics`, `business`, `economics`, `entertainment`, `beauty`, `travel`, `music`, `food`, `science`, `gaming`, `energy`. The topic to which you want to restrict the articles of your choice. Not all news articles are assigned with a topic, therefore, we cannot guarantee that 100% of topics talking about technology will be assigned a tech label.
        :type topic: str or None

        :param proxies: Dict of proxies if needed
        :type proxies: dict or None

        :return: JSON response as nested Python dictionary.
        :rtype: dict
        :raises NewsCatcherApiException: If the ``"status"`` value of the response is ``"error"`` rather than ``"ok"``.

        """

        payload = {}

        # Language
        if lang is not None:
            payload["lang"] = utils.validate_language(lang)

        # Countries
        if countries is not None:
            payload["countries"] = utils.validate_countries(countries, 'countries')

        # Topic
        if topic is not None:
            payload['topic'] = utils.validate_topic(topic)

        # Send Request
        r = self.request_method.get(self.base_url + const.SOURCES_URL, auth=self.auth, timeout=30, params=payload, proxies=proxies)

        # Check Status of Request
        if r.status_code != requests.codes.ok:
            raise NewsCatcherApiException(r.json())

        return r.json()

    def get_latest_headlines_all_pages(
            self,
            lang=None,
            not_lang=None,
            countries=None,
            not_countries=None,
            topic=None,
            sources=None,
            not_sources=None,
            when=None,
            ranked_only=None,
            page_size=100,
            page=1,
            max_page=None,
            seconds_pause=1.0,
            proxies=None
    ):

        """Call the `/latest_headlines` endpoint the number of time sufficient to get all latest articles for a given search.

        Fetch live top and breaking headlines.

        Get the latest headlines given any topic, country, or language. Articles are sorted by the earliest
        date published first. All found articles will be extracted.

        :param lang: Specifies the languages of the search. For example: `en`. The only accepted format is [ISO 639-1 — 2](https://en.wikipedia.org/wiki/ISO_639-1) letter code.
        :type lang: list or str or None

        :param not_lang: Inverse to the `lang` parameter
        :type not_lang: list or str or None

        :param countries: Countries where the news publisher is located. **Important**: This parameter is not responsible for the countries mentioned in the news article. One or multiple countries can be used in the search. The only acceptable format is [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) For example, `US,CA,MX` or just `US`
        :type countries: list or str or None

        :param not_countries: The inverse of the `countries` parameter.
        :type not_countries: list or str or None

        :param topic: Accepted values: `news`, `sport`, `tech`, `world`, `finance`, `politics`, `business`, `economics`, `entertainment`, `beauty`, `travel`, `music`, `food`, `science`, `gaming`, `energy`. The topic to which you want to restrict the articles of your choice. Not all news articles are assigned with a topic, therefore, we cannot guarantee that 100% of topics talking about technology will be assigned a tech label.
        :type topic: str or None

        :param sources: One or more news resources to filter your search. It should be the normal form of the URL, For example: `nytimes.com,theguardian.com`
        :type sources: list or str or None

        :param not_sources: One or more sources to be excluded from the search. Comma-separated list. For example: `nytimes.com,cnn.com,wsj.com`
        :type not_sources: list or str or None

        :param when: The time period you want to get the latest headlines for. Accepted forms: 7d => Dailly Form (last 7 days time period),  30d  (last 30 days time period) | 1h => Hourly Form (last hour), 24h (last 24 hours)
        :type topic: str or None

        :param ranked_only: Default: `True` Limit the search only for the sources which are in the top 1 million online websites. Unranked sources are assigned a rank that equals `999999`
        :type ranked_only: bool or None

        :param page_size: `[1:100]` How many articles to return per page.
        :type page_size: int

        :param page: The number of the page. Use it to scroll through the results. This parameter is used to paginate: scroll through results because one API response cannot return more than 100 articles.
        :type page: int

        :param max_page: The last page number to extract. Use it to manage number of API calls and articles you are going to extract. For example, if you make a broad search with page_size=100 you will extract up to 10 000 articles and make 100 calls to do so.
        :type max_page: int or None

        :param seconds_pause: The number of seconds delay between each API call. For your subscription, you can have a rate limit on number of calls per second.
        :type seconds_pause: float

        :param proxies: Dict of proxies if needed
        :type proxies: dict or None

        :return: JSON response as nested Python dictionary.
        :rtype: dict
        :raises NewsCatcherApiException: If the ``"status"`` value of the response is ``"error"`` rather than ``"ok"``.
        """
        nb_pages = None
        if max_page is not None:
            if type(max_page) == int:
                if max_page >= page:
                    nb_pages = max_page
                else:
                    raise ValueError("max_page param should be greater than page param")
            else:
                raise TypeError("max_page param should be an int")

        all_articles = []
        print(f'{str(page)} page is going to be extracted')
        first_result = self.get_latest_headlines(
            lang=lang,
            not_lang=not_lang,
            countries=countries,
            not_countries=not_countries,
            topic=topic,
            sources=sources,
            not_sources=not_sources,
            when=when,
            ranked_only=ranked_only,
            page_size=page_size,
            page=page,
            proxies=proxies
        )

        time.sleep(seconds_pause)

        if 'articles' not in first_result.keys():
            return first_result

        all_articles.extend(first_result['articles'])

        print(f'Total number of found articles => {first_result["total_hits"]}.\n'
              f'Total number of pages {first_result["total_pages"]}.')

        current_page = page

        if not nb_pages or (max_page and max_page > first_result["total_pages"]):
            nb_pages = first_result["total_pages"]

        while current_page < nb_pages:

            current_page += 1

            print(f'{str(current_page)}/{str(nb_pages)} page is going to be extracted')

            try:
                one_call_results = self.get_latest_headlines(
                    lang=lang,
                    not_lang=not_lang,
                    countries=countries,
                    not_countries=not_countries,
                    topic=topic,
                    sources=sources,
                    not_sources=not_sources,
                    when=when,
                    ranked_only=ranked_only,
                    page_size=page_size,
                    page=current_page,
                    proxies=proxies
                )
                all_articles.extend(one_call_results['articles'])
            except NewsCatcherApiException as e:
                print(f'{current_page} has not been extracted due to an error')
                print(str(e))
                pass

            time.sleep(seconds_pause)


        final_results = first_result
        final_results['articles'] = all_articles

        return final_results

    def get_search_all_pages(
        self,
        q=None,
        lang=None,
        not_lang=None,
        from_=None,
        to_=None,
        published_date_precision=None,
        search_in=None,
        countries=None,
        not_countries=None,
        topic=None,
        sources=None,
        not_sources=None,
        ranked_only=None,
        from_rank=None,
        to_rank=None,
        sort_by=None,
        page_size=100,
        page=1,
        max_page=None,
        seconds_pause=1.0,
        proxies=None
    ):
        """Call the `/search` endpoint the number of time sufficient to get all latest articles for a given search.

        Main endpoint that allows you to find news article by keyword, date, language, country, etc.

        :param q: Keyword/keywords you're searching for. This is the most important part of your query. Please, refer to the **Advanced Query Parameter** section below for more examples and explanations.  (required)
        :type q: str or None

        :param lang: Specifies the languages of the search. For example: `en`. The only accepted format is [ISO 639-1 — 2](https://en.wikipedia.org/wiki/ISO_639-1) letter code.
        :type lang: list or str or None

        :param not_lang: Inverse to the `lang` parameter
        :type not_lang: list or str or None

        :param from_: `YYYY/mm/dd` From which point in time to start the search. The default timezone is UTC. Defaults to the past week.
        :type from_: str or None

        :param to_: `YYYY/mm/dd` Until which point in time to search for. The default timezone is UTC.
        :type to_: str or None

        :param published_date_precision: There are 3 types of date precision we define: `full` — day and time of an article is correctly identified with the appropriate timezone `timezone unknown` — day and time of an article is correctly identified without timezone `date` — only the day is identified without an exact time
        :type published_date_precision: str or None

        :param search_in: By default, we search what you specified in the `q` parameter in both `title` and `summary` of the article. However, you can limit this to either `title` or `summary`
        :type search_in: str or None

        :param countries: Countries where the news publisher is located. **Important**: This parameter is not responsible for the countries mentioned in the news article. One or multiple countries can be used in the search. The only acceptable format is [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) For example, `US,CA,MX` or just `US`
        :type countries: list or str or None

        :param not_countries: The inverse of the `countries` parameter.
        :type not_countries: list or str or None

        :param topic: Accepted values: `news`, `sport`, `tech`, `world`, `finance`, `politics`, `business`, `economics`, `entertainment`, `beauty`, `travel`, `music`, `food`, `science`, `gaming`, `energy`. The topic to which you want to restrict the articles of your choice. Not all news articles are assigned with a topic, therefore, we cannot guarantee that 100% of topics talking about technology will be assigned a tech label.
        :type topic: str or None

        :param sources: One or more news resources to filter your search. It should be the normal form of the URL, For example: `nytimes.com,theguardian.com`
        :type sources: list or str or None

        :param not_sources: One or more sources to be excluded from the search. Comma-separated list. For example: `nytimes.com,cnn.com,wsj.com`
        :type not_sources: list or str or None

        :param ranked_only: Default: `True` Limit the search only for the sources which are in the top 1 million online websites. Unranked sources are assigned a rank that equals `999999`
        :type ranked_only: bool or None

        :param from_rank: `[0:999999]` The lowest boundary of the rank of a news website to filter by. Important: lower rank means that a source is more popular
        :type from_rank: int or None

        :param to_rank: `[0:999999]` The upper boundary of the rank of a news website to filter by.
        :type to_rank: int or None

        :param sort_by: `relevancy` (default value) — the most relevant results first `date` — the most recently published results first `rank` — the results from the highest-ranked sources first
        :type sort_by: str or None

        :param page_size: `[1:100]` How many articles to return per page.
        :type page_size: int or None

        :param page: The number of the page. Use it to scroll through the results. This parameter is used to paginate: scroll through results because one API response cannot return more than 100 articles.
        :type page: int or None

        :param max_page: The last page number to extract. Use it to manage number of API calls and articles you are going to extract. For example, if you make a broad search with page_size=100 you will extract up to 10 000 articles and make 100 calls to do so.
        :type max_page: int or None

        :param seconds_pause: The number of seconds delay between each API call. For your subscription, you can have a rate limit on number of calls per second.
        :type seconds_pause: float

        :param proxies: Dict of proxies if needed
        :type proxies: dict or None

        :return: JSON response as nested Python dictionary.
        :rtype: dict
        :raises NewsCatcherApiException: If the ``"status"`` value of the response is ``"error"`` rather than ``"ok"``.
        """

        nb_pages = None
        if max_page is not None:
            if type(max_page) == int:
                if max_page >= page:
                    nb_pages = max_page
                else:
                    raise ValueError("max_page param should be greater than page param")
            else:
                raise TypeError("max_page param should be an int")

        all_articles = []
        print(f'{str(page)} page is going to be extracted')
        first_result = self.get_search(
            q=q,
            lang=lang,
            not_lang=not_lang,
            from_=from_,
            to_=to_,
            published_date_precision=published_date_precision,
            search_in=search_in,
            countries=countries,
            not_countries=not_countries,
            topic=topic,
            sources=sources,
            not_sources=not_sources,
            ranked_only=ranked_only,
            from_rank=from_rank,
            to_rank=to_rank,
            sort_by=sort_by,
            page_size=page_size,
            page=page,
            proxies=proxies
        )

        time.sleep(seconds_pause)

        if 'articles' not in first_result.keys():
            return first_result

        all_articles.extend(first_result['articles'])

        print(f'Total number of found articles => {first_result["total_hits"]}.\n'
              f'Total number of pages {first_result["total_pages"]}.')

        current_page = page

        if not nb_pages or (max_page and max_page > first_result["total_pages"]):
            nb_pages = first_result["total_pages"]

        while current_page < nb_pages:

            current_page += 1

            print(f'{str(current_page)}/{str(nb_pages)} page is going to be extracted')

            try:
                one_call_results = self.get_search(
                    q=q,
                    lang=lang,
                    not_lang=not_lang,
                    from_=from_,
                    to_=to_,
                    published_date_precision=published_date_precision,
                    search_in=search_in,
                    countries=countries,
                    not_countries=not_countries,
                    topic=topic,
                    sources=sources,
                    not_sources=not_sources,
                    ranked_only=ranked_only,
                    from_rank=from_rank,
                    to_rank=to_rank,
                    sort_by=sort_by,
                    page_size=page_size,
                    page=current_page,
                    proxies=proxies
                )
                all_articles.extend(one_call_results['articles'])
            except NewsCatcherApiException as e:
                print(f'{current_page} has not been extracted due to an error')
                print(str(e))
                pass

            time.sleep(seconds_pause)

        final_results = first_result
        final_results['articles'] = all_articles

        return final_results
