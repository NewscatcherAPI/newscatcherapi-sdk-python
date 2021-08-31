# NewsCatcher News API V2 SDK for Python

The official Python client library to manipulate [NewsCatcher News API V2](https://newscatcherapi.com/news-api) from your Python application.

Documentation is identical with the API documentation. The same parameters and filters are available. 
And the same response structure. You can have a look at [docs.newscatcherapi.com](https://docs.newscatcherapi.com).

## Authentication

The Authentication is done via the `x_api_key` variable.

Receive your API key by registering at [app.newscatcherapi.com](https://app.newscatcherapi.com).

## Installation
```pip install newscatcherapi```

## Quick Start
Import installed package.

`````from newscatcherapi import NewsCatcherApiClient`````

Init the instance with an API key given after registration.

````newscatcherapi = NewsCatcherApiClient(x_api_key='YOUR_API_KEY') ````

## Endpoints
An instance of `NewsCatcherApiClient` has three main methods that correspond to three endpoints available for NewsCatcher News API.

### Get News (/v2/search)
Main method that allows you to find news article by keyword, date, language, country, etc.

```
all_articles = newscatcherapi.get_search(q='Elon Musk',
                                         lang='en',
                                         country='CA',
                                         page_size=100)
```

### Get Latest Headlines (/v2/latest_headlines)
Get the latest headlines given any topic, country, sources, or language.

```
top_headlines = newscatcherapi.get_latest_headlines(lang='en',
                                                    countries='us',
                                                    topic='business')
 ```

### Get Sources (/v2/sources)
Returns a list of the top 100 supported news websites. Overall, we support over 60,000 websites. Using this method, you may find the top 100 for your specific language, country, topic combination.

```
sources = newscatcherapi.get_sources(topic='business',
                                     lang='en',
                                     countries='US')
 ```


### Use *from_* and *to_* instead of *from* and *to* like in NewsCatcher News API
In Python, we are not allowed to reserve variable names *from* and *to*. If you try to use them, you will get a syntax error:

```SyntaxError: invalid syntax``` 

So, here is an example on how to use time variables *from_* and *to_* in *get_search* method.

```
all_articles = newscatcherapi.get_search(q='Elon Musk',
                                         lang='en',
                                         countries='CA,US',
                                         from_='2021/08/20',
                                         to_='2021/08/31')
```

## Feedback

Feel free to contact us if you have spot a bug or have any suggestion at maksym`[at]`newscatcherapi.com