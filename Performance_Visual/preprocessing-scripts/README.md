Visualiation data generation
----------------------------

We extract only necessary information for the visualization from the processed event data csv file:
```
python processEvents.py processed_logs.csv
```
The script removes duplicate events that come after another withing each user. Comment out the corresponding part of the script to disable such feature.

Check user data consistency between database data and event data:
```
python checkUsersQuality.py database_data_dir extracted_processed_events.csv
```

We then combine event data and demographic data to generate one table as input to analysis module:
```python joinTables.py database_data_dir xAPI_event_data.csv
```
This will generate grade.csv.

Filter for users whose grades > 0.0:
```
python filter.py grade.csv > grade_not_0.csv
```



