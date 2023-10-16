# Input File format guide  

- All input files should be in `CSV` format. 
- All CSV files should contain a header row. 
- For precipitation and evapotranspiration, first column header should be `Time` and other column's header should correspond to the subbasin name in the basin definition file.
- Values in `Time` column should follow `ISO 8601` date format.
- Unit of precipitation and evapotranspiration should be in millimeters(mm). 

|Time                              | SB-1 | SB-2 | ... |
|----------------------------------|------|------|-----|
| 2021-12-01T12:00:00.000000+00:00 | 10.5 | 1.5  |     | 
| 2021-12-01T13:00:00.000000+00:00 | 0.55 | 2.7  |     |
| 2021-12-01T14:00:00.000000+00:00 | 12.5 | 8.1  |     | 