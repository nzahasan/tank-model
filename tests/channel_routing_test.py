import numpy as np
import tank_core.channel_routing as cr
import json 
from pathlib import Path


def get_test_data(data_path):
    test_data_file = Path.joinpath(Path(__file__).resolve().parent, Path(data_path))
    fb =  open(test_data_file, 'r')
    return json.load(fb)


def test_muskingum():

    test_data = get_test_data('test_data/channel_routing_muskingum.json')

    for i, (inpt, outp )in enumerate( zip(test_data['input'], test_data['output']) ):

        delT = inpt['parameters']['dt']
        K = inpt['parameters']['k']
        X = inpt['parameters']['x']

        inflow_data = np.array(np.array(inpt['inflow']))

        _outflow = cr.muskingum(inflow_data,delT,K,X)

        outflow_data = np.array( outp['outflow'] )

        np.testing.assert_almost_equal(_outflow, outflow_data, decimal=3)



