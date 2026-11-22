# Input File Format Guide

## General Rules

- All input files must be in **CSV** format.
- Every CSV file must contain a header row.
- The first column header must be `Time`.
- Values in the `Time` column must use the `%Y-%m-%dT%H:%M:%S` date format (e.g. `2021-12-01T12:00:00`).

## Precipitation and Evapotranspiration

- Each column after `Time` corresponds to a subbasin. Its header must match the subbasin name in the basin definition file.
- Values must be in millimeters (mm).

**Sample:**

| Time                | SB-1 | SB-2 | ... | SB-n |
|---------------------|------|------|-----|------|
| 2021-12-01T12:00:00 | 10.5 | 1.5  |     |      |
| 2021-12-01T13:00:00 | 0.55 | 2.7  |     |      |
| 2021-12-01T14:00:00 | 12.5 | 8.1  |     |      |

## Error Correction

- `OBS` holds the observed discharge.
- `SIM_T1` to `SIM_Tn` hold the forecast discharge for each timestep (`T1` is the first timestep, `T2` the second, and so on).
- Values must be in cubic meters per second (m³/s).

**Sample:**

| Time                | OBS  | SIM_T1 | SIM_T2 | ... | SIM_Tn |
|---------------------|------|--------|--------|-----|--------|
| 2021-12-01T12:00:00 | 10.5 | 1.5    |        |     |        |
| 2021-12-01T13:00:00 | 0.55 | 2.7    |        |     |        |
| 2021-12-01T14:00:00 | 12.5 | 8.1    |        |     |        |
