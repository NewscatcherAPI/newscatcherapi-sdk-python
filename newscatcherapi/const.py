"""Constants and allowed parameter values specified in the NewsCatcher News API."""

LATEST_HEADLINES_URL = "/v2/latest_headlines"
SEARCH_URL = "/v2/search"
SOURCES_URL = "/v2/sources"

#: The 2-letter ISO-639-1 code of the language you want to get articles for.
allowed_languages = 'af,ar,bg,bn,ca,cs,cy,cn,da,de,el,en,es,et,fa,fi,fr,gu,he,hi,hr,hu,id,it,ja,kn,ko,lt,lv,mk,ml,mr,ne,nl,no,pa,pl,pt,ro,ru,sk,sl,so,sq,sv,sw,ta,te,th,tl,tr,tw,uk,ur,vi'.split(',')

#: The topic you want to get articles for.
allowed_topics = 'news,sport,tech,world,finance,politics,business,economics,entertainment,beauty,travel,music,food,science,gaming,energy'.split(',')

# Date precisions
allowed_precisions = 'timezone unknown,full,date'.split(',')

# Search In
allowed_search_ins = ['title', 'summary', 'title,summary']

#: The order to sort article results in.  If not specified, the default is ``"relevancy"``.
allowed_sorts = ['relevancy', 'date', 'rank']
