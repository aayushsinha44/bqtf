# BQTF - Biqquery Query Testing Framework

Automated testing framework for query of big query. 

## Problems with testing a query
When the query is simple and small, it doesnot requires any automated testing. It can be related to code for sum of 2 numbers, which doesnot requires any automated testing. But when the query is complex enough, the only testing we are left with is to test with existing data in the database. Now for some small changes to the query, we are required to test it again.

## How to test a query of bigquery?
<p>One of the way of testing a query is to create a dummy entry of the tables we are using in the query. <p/>

```
WITH customer AS (
  SELECT 1 AS id, 'aayush' as name UNION ALL
  SELECT 2 AS id, 'sinha' as name UNION ALL
)
SELECT count(*) FROM customer
```
Now with this construct we made some dummy data for customer and we can calculate the match the output with expected output. By this we can test query.

## Problems with above approach
1. Won't work we have tables inside dataset. e.g. common.customers
2. Won't worr if we have json object in schema. e.g. user.id

## BQTF Approach For Solution
BQTF automates the complete process of query testing and also solves the above problems. It requires YAML files as descriptive input of the generating query with dummy data and runs the query with the provide bigquery credentials. 

Sample .yml files can be found in examples folder.
