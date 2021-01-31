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
    'thermal_info'      : '/Chassis/{id}/Thermal',
    'virtual_media'     : '/Managers/{id}/VM1',                                  # GET
    'vm_cd1'            : '/Managers/{id}/VM1/CD1',                              # GET
    'set_vm_state'      : '/Managers/{id}/NetworkProtocol',                      # GET, PATCH
    'config_cd_instance': '/Managers/{id}/VM1/CfgCD',                            # GET, PATCH
    'mount_cd'          : '/Managers/{id}/VM1/CfgCD/Actions/IsoConfig.Mount',    # POST
    'unmount_cd'        : '/Managers/{id}/VM1/CfgCD/Actions/IsoConfig.UnMount',  # POST
    'reset_system'      : '/Systems/{id}/Actions/ComputerSystem.Reset'           # POST
    }

    def __init__(self, bmc_ip, user, passwd):
        super().__init__(bmc_ip, user, passwd)

