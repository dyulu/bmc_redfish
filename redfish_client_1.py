import redfish_client

class RedfishClient1(redfish_client.RedfishClient):
    resources = {
    'system'            : '/Systems/System.Embedded.{id}',
    'manager'           : '/Managers/iDRAC.Embedded.{id}',
    'chassis'           : '/Chassis/System.Embedded.{id}',
    'event_service'     : '/EventService/Subscriptions',
    'events'            : '/Managers/iDRAC.Embedded.{id}/Logs/Lclog',    # WrapsWhenFull
    'sel'               : '/Managers/iDRAC.Embedded.{id}/Logs/Sel',
    'clear_sel'         : '/Managers/iDRAC.Embedded.{id}/LogServices/Sel/Actions/LogService.ClearLog',
    'power_supply_info' : '/Chassis/System.Embedded.{id}/Power/',
    'thermal_info'      : '/Chassis/System.Embedded.{id}/Thermal'
    }

    def __init__(self, bmc_ip, user, passwd):
        super().__init__(bmc_ip, user, passwd)

