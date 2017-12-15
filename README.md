# Hands on Elasticsearch
Elasticsearch is a good fulltext search engine.

- Wikipedia search is powered by Elasticsearch.
- The Guardian joins access log data with social network data using Elasticsearch to give editors an idea of how public is reponding to articles.
- StackOverflow fulltext search is powered by Elasticsearch. They use the _more like this_ feature to find similar answers.
- GitHub uses Elasticsearch to query 130 billion lines of code

## Prerequisites
Docker and Python 2.7 with pip or easy_istall and internet access.

0. Get code. ```git clone git@github.com:josalmi/es-movies.git```
1. Fire up elasticsearch. ```docker-compose up```
2. Open shell in client container: ```docker-compose run client /bin/bash```
3. Load data. ```./init.sh```
4. Profit

## Excercises
We are using [UCI Movies Dataset](https://archive.ics.uci.edu/ml/datasets/Movie) of over 10k films. The titles are from late 1800's to 1999.

### [URI Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-uri-request.html)
Find all the Academy Awards winners in the database. _AA_ stands for winning an Academy Award.

Find the film _Elmer Gantry_ in the raw data. Did it win an Academy Award?

### [Boolean Query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)

1. Find all the Academny Award winners excluding those who were just nominated (AAN).
2. Try to filter all those movies which contain the word 'Vampire'. How many are there? What's up with the score.

### [Funtion Score Query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html)
1. The Best films are not in any particular order. Let's see if we can use a function score to order the results after matches have been made. Perhaps the field_value_factor or the decay functions can help us order our movies.

2. Something isn't right. Let's look at what our index looks like. ```curl http://localhost:9200/movies```. What's the problem?

### Creating an index mapping.
Tuning relevance in Elasticsearch is a dance between the index and the query. Let's add some mappings! In order to change the mappings, we will create a new index named 1. There are some ready made mappings. But is there something we should change to make the function score work?

```./et create index 1```
```./et reindex 0 1```
```./et index alias movies 1 0```

### Find academy award winners in drama category?

### It's a long way from V to Vampire
Once you start typing into the typeahead field the experience isn't very satisfying. Let's create a typeahead index.

### Let's add language analyzers into the mix

### They have inherent weaknesses, so let's add the original field to the side of the analyzed one.

### Bigrams

### Exact phrase matching

### Fuzzy query and minimum should match
