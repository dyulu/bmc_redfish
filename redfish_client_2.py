import redfish_client

class RedfishClient2(redfish_client.RedfishClient):
    resources = {
    'system'            : '/Systems/Self',
    'manager'           : '/Managers/Self',
    'chassis'           : '/Chassis/Self',
    'event_service'     : '/EventService/Subscriptions',
    'audit_log'         : '/Managers/Self/LogServices/AuditLog/Entries',
    'clear_audit_log'   : '/Managers/Self/LogServices/AuditLog/Actions/LogService.ClearLog',
    'events'            : '/Managers/Self/LogServices/EventLog/Entries',
    'clear_events'      : '/Managers/Self/LogServices/EventLog/Actions/LogService.ClearLog',
    'sel'               : '/Managers/Self/LogServices/SEL/Entries',
    'clear_sel'         : '/Managers/Self/LogServices/SEL/Actions/LogService.ClearLog',
    'power_supply_info' : '/Chassis/Self/Power',
    'thermal_info'      : '/Chassis/Self/Thermal'
    }

    def __init__(self, bmc_ip, user, passwd):
        super().__init__(bmc_ip, user, passwd)

