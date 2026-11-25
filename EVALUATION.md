# Evaluation Report

We tested our transport AI project on 4 sample queries manually.

## Method
Sent queries using browser form and checked output JSON.

## Results
1 out of 4 queries worked properly. Other queries returned all rows or wrong columns.

## Trade-off
We used sqlite instead of postgres because it is faster to setup and we did not have time for langgraph or chroma.

## Known Failures
- Company data leaks across companies
- Aggregation and dates do not work
- Tests fail
