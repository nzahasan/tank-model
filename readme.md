# Tank Hydrologic Model  
Python implementation of Tank Hydrologic Model, a conceptual rainfall-runoff model proposed by Sugawara and Funiyuki (1956)


<p align="center">
<img align="center" height="500px"  src="https://raw.githubusercontent.com/nzahasan/tank-model/master/assets/tank-model-schamatic.svg" >
</p>

### Installation

Tank-Model can be installed as a python package from PyPI

```bash
$ pip install tank-model
```

Alternatively, it can be installed directly from git

```bash
$ pip install https://github.com/nzahasan/tank-model/zipball/main
```

after successful installation `tank_cmd.py` should be available which can be used for setting up new project, optimizing the project and computation.

```bash
# get help text command line utility
$ tank_cmd.py --help

# get help text of subcommand
$ tank_cmd.py new-project --help
```

### Setting up a new model:

New project can be created using the following command. This command creates a folder in working directory with a json formatted project definition inside it.
```bash
$ tank_cmd.py new-project project_name
```

A sample project definition looks like this
```json
{
  "interval": 24.0,
  "basin": "sample_project.basin.json",
  "precipitation": "sample_project.pr.csv",
  "evapotranspiration": "sample_project.et.csv",
  "discharge": "sample_project.q.csv",
  "result": "sample_project.result.csv",
  "statistics": "sample_project.stats.json",
  "start": "2020-01-01T00:00:00",
  "end": "2020-12-31T00:00:00"
}
```
here `interval` is the time step of simulation in hours. The other attributes are file locations; `precipitation`, `evapotranspiration` and `discharge` are CSV files containing time-series data. These files should be formatted according to the file format mentioned here <a href="file-format-spec.md">file-format-spec.md</a>

`start` and `end` are optional and restrict `compute`, `optimize` and `plot-result` to the given date range (format `%Y-%m-%dT%H:%M:%S`, matching the time-series files). If omitted, the full period available in the input files is simulated; either one can be given on its own, in which case the other side of the range is left unbounded.

`precipitation` & `evapotranspiration` serve as input data for the model simulation and resulting output is stored in the `result` file following the time-series CSV format mentioned earlier. Data in the `discharge` is used for model calibration. And performance matrices are stored in the `statistics` file.



### Converting HEC-HMS basin to tank model basin

```bash
$ tank_cmd.py hms2tank -bf hechms_basin_file -of output_tank_basin_file_path
```

### Computing tank model

```bash
$ tank_cmd.py compute -pf project_name.project.json
```

### Automatic optimization of tank model

```bash
$ tank_cmd.py optimize -pf project_name.project.json
```

### Known Limitions

  - Currently there is no way to optimize for multiple root node 

### References:  
    1. Paik K., Kim J. H., Kim H. S., Lee D. R. (2005) A conceptual rainfall-runoff model considering seasonal variation.
    2. Aguilar C., Polo M. J. (2011) Generating reference evapotranspiration surfaces from the Hargreaves equation at watershed scale.
    3. Taib A. T. M., Tahir W., Ramli S., Mohtar I. S. A. (2022) Hydro-Meteorological Flood Forecasting Using Tank Model With Satellite-Based Rainfall Input For Kemaman River Catchment.
    4. D. N. Moriasi, J. G. Arnold, M. W. Van Liew, R. L. Bingner, R. D. Harmel, T. L. Veith (2007) Model Evaluation Guidelines For Systematic Quantification Of Accuracy In Watershed Simulations.
