# File format guideline  

- Input files may contain precipitation and evapotranspiration data in seperate file and should be mentioned in project json file.
- Unit of precipitation and evapotranspiration should be in milimeters(mm).  
- Files should contain a Time column and other column name should be basin names 
- Files should be in csv format and time in file should follow ISO-8601 specification(%Y-%m-%dT%H:%M:%S) 

|Time               |Basin-1|Basin-2| ..... |
|-------------------|-------|-------|-------|
|2021-12-01T12:00:00| 10.5  | 1.5   |       | 
|2021-12-01T13:00:00| 0.55  | 2.7   |       |
|2021-12-01T14:00:00| 12.5  | 8.1   |       | 