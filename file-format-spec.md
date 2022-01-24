# File format guide  

- Input files may contain precipitation and evapotranspiration data in seperate file and should be mentioned in project json file.
- Unit of precipitation and evapotranspiration should be in milimeters(mm). 
- All input files should be in `CSV` format. 
- CSV files should contain header row in uppercase characters. First column should be end-time (e.g. precipitaiton accumulation end time for a day) followed by data for each basin.
- Values in `TIME` column should follow `ISO-8601` specification(%Y-%m-%dT%H:%M:%S) 

|TIME               |SUBBASIN-1|SUBBASIN-2| ..... |
|-------------------|----------|----------|-------|
|2021-12-01T12:00:00|   10.5   |   1.5    |       | 
|2021-12-01T13:00:00|   0.55   |   2.7    |       |
|2021-12-01T14:00:00|   12.5   |   8.1    |       | 