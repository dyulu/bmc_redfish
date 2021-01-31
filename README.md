curl --insecure --user <user>:<passwd> https://<ip>/redfish/v1/Managers/Self/LogServices/SEL/Entries | jq .
curl --insecure --user <user>:<passwd> -X POST -d '{"ClearType" : "ClearAll"}' -H "Content-Type: application/json" https://<ip>/redfish/v1/Managers/Self/LogServices/SEL/Actions/LogService.ClearLog

HTTP response status codes:
    Informational responses (100–199)
    Successful responses (200–299)
    Redirects (300–399)
    Client errors (400–499)
    Server errors (500–599)

ipmitool event
usage: event <num>
   Send generic test events
   1 : Temperature - Upper Critical - Going High
   2 : Voltage Threshold - Lower Critical - Going Low
   3 : Memory - Correctable ECC
usage: event file <filename>
   Read and generate events from file
   Use the 'sel save' command to generate from SEL
usage: event <sensorid> <state> [event_dir]
   sensorid  : Sensor ID string to use for event data
   state     : Sensor state, use 'list' to see possible states for sensor
   event_dir : assert, deassert [default=assert]

ipmitool -I lanplus -H bmc_ip -U user -P passwd ipmi_cmd:

chassis status:
chassis power on:
chassis power off:
chassis power cycle:
chassis power soft:

sdr list: get a list of all sensors in these servers and their status
sdr elist: also print sensor number, entity id and instance, and asserted discrete states
sdr elist -v: with detail on each sensor
    refine the output to see only specific sensors:
          all: All sensor records; All sensors
          full: Full sensor records; Temperature, voltage, and fan sensors
          compact: Compact sensor records; Digital Discrete: failure and presence sensors
          event: Event-only records; Sensors used only for matching with SEL records
          mcloc: MC locator records; Management Controller sensors
          generic: Generic locator records; Generic devices: LEDs
          fru: FRU locator records; FRU devices

sdr entity entity_id: get a list of all sensors related to an entity
sdr type sensor_type: get a list of a particular type of sensors, e.g., temperature, fan, power supply.
sdr info: query the BMC for SDR information

sensor list: list sensors and thresholds in a wide table format

sensor get sensor_id: get information for sensors specified by ID

fru: get built-in FRU and scan for  FRU  locators

sel info: query the BMC for information about the System Event Log (SEL) and its contents

sel list: view a minimal level of SEL detail
sel elist: view a detailed event output. The sel elist command cross-references event records with sensor
data records to produce descriptive event output. It takes longer to execute because it has to read from
both the SEL and the Static Data Repository (SDR). For increased speed, generate an SDR cache before using
the sel elist command.
sel elist -v: with details on each SEL event

sel get sel_record_id:  get more detailed information on a particular event

sel clear: clear the SEL

sdr dump cached_sdr_file: pre-cache the static data in the SDR so it can be fed back into IPMItool later

ipmitool -S cached_sdr_file sel elist: speed up sel elist command by using Sensor Data Repository (SDR) cache

user summary:
user list:

====

curl -X GET -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/Self' --user username:passwd

curl -X GET -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/Self/VirtualMedia' --user username:passwd

curl -X GET -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/Self/VirtualMedia/Oem/Ami/CD1' --user username:passwd

curl -X POST -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/Self/Actions/Oem/Ami/VirtualMedia.EnableRMedia' --data '{ "RMediaState" : "Disable" }' --user username:passwd

curl -X POST -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/Self/Actions/Oem/Ami/VirtualMedia.EnableRMedia' --data '{ "RMediaState" : "Enable" }' --user username:passwd

curl -X POST -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/Self/Actions/Oem/Ami/VirtualMedia.ConfigureCDInstance' --data '{ "CDInstance" : 1 }' --user username:passwd

curl -X POST -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/Self/VirtualMedia/CD1/Actions/Oem/Ami/VirtualMedia.InsertMedia' --data '{"Image" : "nfs://nfs_server_ip/mnt/nfs_share/CentOS-8.2.2004-x86_64-minimal.iso", "TransferProtocolType" : "NFS"}' --user username:passwd

curl -X POST -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/Self/VirtualMedia/CD1/Actions/Oem/Ami/VirtualMedia.EjectMedia' --data '{ }' --user username:passwd

curl -X POST -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Systems/Self/Actions/ComputerSystem.Reset' --data '{"ResetType": "ForceRestart"}' --user username:passwd    # On, ForceOff, GracefulShutdown, ForceRestart

====

curl -X GET -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/1/VM1' --user username:password

curl -X GET -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/1/VM1/CD1' --user username:password

curl -X GET -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/1/NetworkProtocol' --user username:password

curl -X PATCH -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/1/NetworkProtocol' --data '{"VirtualMedia": {"ProtocolEnabled": false}}' --user username:password

curl -X PATCH -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/1/NetworkProtocol' --data '{"VirtualMedia": {"ProtocolEnabled": true}}' --user username:password

curl -X PATCH -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/1/VM1/CfgCD' --data '{"Host" : "samba_server_ip", "Path" : "/cifs_share/CentOS-8.2.2004-x86_64-minimal.iso"}' --user username:password       # For Samba server allowing guest access

curl -X PATCH -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/1/VM1/CfgCD' --data '{"Host" : "samba_server_ip", "Path" : "/cifs_share/CentOS-8.2.2004-x86_64-minimal.iso", "Username" : "USERNAME", "Password" : "PASSWORD"}' --user username:password

curl -X GET -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/1/VM1/CfgCD' --user username:password

curl -X POST -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/1/VM1/CfgCD/Actions/IsoConfig.Mount' --data '{ }' --user username:password

curl -X POST -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Managers/1/VM1/CfgCD/Actions/IsoConfig.UnMount' --data '{ }' --user username:password

curl -X POST -k -H 'Content-Type:  application/json' -i 'https://bmc_ip/redfish/v1/Systems/Self/Actions/ComputerSystem.Reset' --data '{"ResetType": "GracefulRestart"}' --user username:password    # On, GracefulShutdown, GracefulRestart
