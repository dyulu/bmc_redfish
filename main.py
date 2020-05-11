#!/usr/bin/python3

import argparse
import pprint
from datetime import datetime

import redfish_client_1
import redfish_client_2
import redfish_client_3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bmc_ip', help='BMC ip addr', type=str)
    parser.add_argument('user', help='BMC username', type=str)
    parser.add_argument('passwd', help='BMC password', type=str)
    parser.add_argument('vendor', help='BMC vendor', type=str)
    args = parser.parse_args()
    args.vendor = args.vendor.lower()

    redfish_client = None
    if args.vendor == '1':
        redfish_client = redfish_client_1.RedfishClient1(args.bmc_ip, args.user, args.passwd)
    elif args.vendor == '2':
        redfish_client = redfish_client_2.RedfishClient2(args.bmc_ip, args.user, args.passwd)
    else:
        redfish_client = redfish_client_3.RedfishClient3(args.bmc_ip, args.user, args.passwd)

    pp = pprint.PrettyPrinter()
    pp.pprint(redfish_client.get_system_info())
    pp.pprint(redfish_client.get_manager_info())
    pp.pprint(redfish_client.get_chassis_info())
    pp.pprint(redfish_client.get_sel())
    pp.pprint(redfish_client.get_power_supply_status())
    pp.pprint(redfish_client.get_fan_status())
    # pp.pprint(redfish_client.get_temperature_status())
    # pp.pprint(redfish_client.clear_sel())

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = date_str.replace(" ", "_")
    date_str = date_str.replace(":", "_")
    temp_filename = "BMC_{}_temperature_{}.csv".format(args.bmc_ip, date_str)
    with open(temp_filename, "w") as temp_file:
        redfish_client.get_temperature_status(True, temp_file)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        pass

