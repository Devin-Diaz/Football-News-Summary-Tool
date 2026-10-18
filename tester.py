from gnews import GNews
from scripts.tools import resolve_source_url

g = GNews(max_results=10)

source_url = 'https://sports.yahoo.com/articles/guler-huijsen-start-4-2-195000503.html?guccounter=1&guce_referrer=aHR0cHM6Ly9uZXdzLmdvb2dsZS5jb20v&guce_referrer_sig=AQAAANPXw16hm-6f72mrCZDorrMgR1lUA9th-oGha4r9M7SY0SbxIbmbltwXGd3wsj7-3JGZVsmn4FWAL_p-KwLFBNRNne4j5HaNkB3hUoBYxCuiaDBYF4hDq5CwanjxsbO_ZSl2EEJQZKPqahd22JjtSv2s7uKiQH86kspbKLngzHsF'

print(resolve_source_url("https://news.google.com/rss/articles/CBMifEFVX3lxTE01OHN6NzV4bmg0aWU1aFBfLTBKVFZlZmp1T3RyamVuaFFfdndPNDRUbnlsbS1seGt3d0ZzUHJOZ2Iwakd3ZWJZdGYzbTI3bHNWWlF6UWhyc3c2MmhwQWdUUXF0d3N5Z2hLdF9hVm5uQXdkdGF2Ymx2NDJEbmY?oc=5&hl=en-US&gl=US&ceid=US:en"))