
from argparse import ArgumentParser
import csv
import logging
from ttp import ttp
from pprint import pprint
from pathlib import Path
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

script_path = Path(__file__).resolve().parent

ttp_interface_template = """
<group>
interface {{ interface }}
 description {{ description | re(".*") }}
 ip address {{ ipv4 }} {{ mask_v4 }}
 shutdown {{ disabled | set(True) }}
 mtu {{ mtu }}
 encapsulation dot1Q {{ dot1q }}
 encapsulation dot1q {{ dot1q }}
! {{ _end_ }}
</group>
"""


def get_inteface_params(config_data, template = ttp_interface_template):
    # create parser object and parse data using template:
    parser = ttp(data=config_data, template=template)
    parser.parse()
    all_interface_data = parser.result()[0][0]
    pprint(all_interface_data)
    # csv_results = parser.result(format='csv')[0]
    # pprint(csv_results)
    return all_interface_data


def main():
    """
    summary:
        
    """
    logging.basicConfig(level=logging.INFO,format= "%(asctime)s::%(name)s::-%(module)s::-: %(funcName)s -  %(levelname)s :: - %(message)s")
    # parse command line args
    parser = ArgumentParser()
    # positinal args ( Mandatory args)
    parser.add_argument(
       "input_config", type=str, help=" show run | sec interface "
    )
    
    # setting up logging to DEBUG level
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="set logging:  DEBUG ",
    )
    # set logging to DEBUG based on CMD line args
    cmd_args = parser.parse_args()
    if cmd_args.verbose:
        logger.setLevel(logging.DEBUG)
        # set level for all handles
        for hdler in logger.handlers:
            hdler.setLevel(logging.DEBUG)
        logger.debug("Loggig set to DEBUG")
        logger.warning("Logging set to DEBUG")
    
    input_config = cmd_args.input_config
    with open(input_config,'r') as fp_config:
        config_data = fp_config.read()
    
    interface_data = get_inteface_params(config_data)
   
    # use dict to csv writer    
    fieldnames = ["interface", "ipv4", "mask_v4","mtu", "description"]
    with open('output.csv','w',newline='') as fp_out:
        dict_writer = csv.DictWriter(fp_out, fieldnames=fieldnames,extrasaction='ignore')
        dict_writer.writeheader()
        for interface in interface_data:
            if interface['interface'] == 'Loopback0':
                pprint(interface)
                dict_writer.writerow(interface)
            elif interface.get("ipv4"):
                pprint(interface)
                dict_writer.writerow(interface)
        
    
    
if __name__ == "__main__":
    main()