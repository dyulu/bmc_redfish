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
    'thermal_info'      : '/Chassis/Self/Thermal',
    'virtual_media'     : '/Managers/Self/VirtualMedia',                                               # GET
    'vm_cd1'            : '/Managers/Self/VirtualMedia/Oem/Ami/CD1',                                   # GET
    'set_vm_state'      : '/Managers/Self/Actions/Oem/Ami/VirtualMedia.EnableRMedia',                  # POST
    'config_cd_instance': '/Managers/Self/Actions/Oem/Ami/VirtualMedia.ConfigureCDInstance',           # POST
    'mount_cd'          : '/Managers/Self/VirtualMedia/CD1/Actions/Oem/Ami/VirtualMedia.InsertMedia',  # POST
    'unmount_cd'        : '/Managers/Self/VirtualMedia/CD1/Actions/Oem/Ami/VirtualMedia.EjectMedia',   # POST
    'reset_system'      : '/Systems/Self/Actions/ComputerSystem.Reset'                                 # POST
    }

    def __init__(self, bmc_ip, user, passwd):
        super().__init__(bmc_ip, user, passwd)

