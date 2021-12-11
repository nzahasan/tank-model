import numpy as np
import pandas as pd 


def read_input_file(file_path:str)-> tuple:
    '''
        reads model input file (precip, et)
        returns tuple(dataframe, del_time[seconds])
    '''

    # read file as pandas dataframe
    df = pd.read_csv(
        file_path,
        index_col=['Time'],
        parse_dates=['Time'],
        infer_datetime_format=True
    )

    # sort by index
    df.sort_index(inplace=True)

    # check if missing date
    t_diff = np.diff(df.index.values, n=1)

    if not np.all(t_diff==t_diff[0]):
        raise Exception('Time difference is not equal, possible missing values')

    return (df , t_diff[0]/np.timedelta64(1,'s') )


def write_output_file(df:pd.DataFrame,file_path:str)->int:

    df.to_csv(
        file_path,
        float_format='%.3f',
        date_format='%Y-%m-%dT%H:%M:%S'
    )

    return 0





