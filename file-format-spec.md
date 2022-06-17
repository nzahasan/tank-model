# File format guide  

- Input files may contain precipitation and evapotranspiration data in seperate file and should linked in JSON formatted project file.
- Unit of precipitation and evapotranspiration should be in milimeters(mm). 
- All input files should be in `CSV` format. 
- CSV files should contain header row in uppercase characters. First column should be end-time (e.g. precipitaiton accumulation end time for a day) followed by data for each basin.
- Values in `TIME` column should follow `ISO-8601` specification and all values should be in UTC+00 time.

|TIME                         |SUBBASIN-1|SUBBASIN-2| ..... |
|-----------------------------|----------|----------|-------|
| 2021-12-01T12:00:00.000000Z |   10.5   |   1.5    |       | 
| 2021-12-01T13:00:00.000000Z |   0.55   |   2.7    |       |
| 2021-12-01T14:00:00.000000Z |   12.5   |   8.1    |       | 