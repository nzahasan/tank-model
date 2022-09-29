# Tank Hydrologic Model  
Python implementation of Tank Hydrologic Model, a conceptual rainfall-runoff model proposed by Sugawara and Funiyuki (1956)


<p align="center">
<img align="center" height="600px"  src="https://raw.githubusercontent.com/nzahasan/tank-model/master/assets/tank-model-schamatic.svg" >
</p>

### Installation

Tank-Model can be installed as a python package using the following commands

```bash
$ git clone https://github.com/nzahasan/tank-model.git
$ cd tank-model
$ python3 setup.py install
```


### Setting up a new model:

New project can be created using the following command. This creates a folder with a project defination inside it.
```bash
$ tank_cmd.py new_project project_name
```

### Converting HEC-HMS basin to tank model basin

```bash
$ tank_cmd.py hms2tank -bf hechms_basin_file -of output_tank_basin_file_path
```

### References:  
    1. Paik K., Kim J. H., Kim H. S., Lee D. R. (2005) A conceptual rainfall-runoff model considering seasonal variation.
    2. Aguilar C., Polo M. J. (2011) Generating reference evapotranspiration surfaces from the Hargreaves equation at watershed scale.
    3. Taib A. T. M., Tahir W., Ramli S., Mohtar I. S. A. (2022) Hydro-Meteorological Flood Forecasting Using Tank Model With Satellite-Based Rainfall Input For Kemaman River Catchment.
    4. D. N. Moriasi, J. G. Arnold, M. W. Van Liew, R. L. Bingner, R. D. Harmel, T. L. Veith (2007) Model Evaluation Guidelines For Systematic Quantification Of Accuracy In Watershed Simulations.
