import redfish_client

class RedfishClient3(redfish_client.RedfishClient):
    resources = {
    'system'            : '/Systems/{id}',
    'manager'           : '/Managers/{id}',
    'chassis'           : '/Chassis/{id}',
    'event_service'     : '/EventService/Subscriptions',
    'events'            : '/Systems/{id}/LogServices/Log1/Entries',
    'clear_events'      : '/Systems/{id}/LogServices/Log1/Actions/LogService.ClearLog',
    'sel'               : '/Managers/{id}/LogServices/Log1/Entries',
    'clear_sel'         : '/Managers/{id}/LogServices/Log1/Actions/LogService.ClearLog',
    'power_supply_info' : '/Chassis/{id}/Power',
    'thermal_info'      : '/Chassis/{id}/Thermal'
    }

    def __init__(self, bmc_ip, user, passwd):
        super().__init__(bmc_ip, user, passwd)

