# File format guide  

- Input files may contain precipitation and evapotranspiration data in separate file and should linked in JSON formatted project file.
- Unit of precipitation and evapotranspiration should be in millimeters(mm). 
- All input files should be in `CSV` format. 
- CSV files should contain header row in uppercase characters. First column should be end-time (e.g. precipitation accumulation end time for a day) followed by data for each basin.
- Values in `TIME` column should follow  this specific format `%Y-%m-%dT%H:%M:%S.%f%z`

|Time                              | SB-1 | SB-2 | ... |
|----------------------------------|------|------|-----|
| 2021-12-01T12:00:00.000000+00:00 | 10.5 | 1.5  |     | 
| 2021-12-01T13:00:00.000000+00:00 | 0.55 | 2.7  |     |
| 2021-12-01T14:00:00.000000+00:00 | 12.5 | 8.1  |     | 