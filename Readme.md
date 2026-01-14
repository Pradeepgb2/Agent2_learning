For now the two tasks were implemented
Task 1:
code location: scrapers/utils/data_fetch_dataset.py
 For downloading the dataset from the third  party website using the API key, url and save the dataset in scrapers/data/raw location.

Task 2:
code location: ai/pipelines/agent2_comparator.py
 First read the two latest datasets from the location scrapers/data/raw and then by using the pandas library compare the both datasets for company and roles changes and save the report as employee_changes_report.csv in location ai/output.


