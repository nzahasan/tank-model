from tank_core import global_parameters as gp

# define default parameters
basin_default = 0.5 * (gp.tank_lb + gp.tank_ub)
channel_default = 0.5 * (gp.muskingum_lb + gp.muskingum_ub)