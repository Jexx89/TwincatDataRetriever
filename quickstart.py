import os
os.environ['Path'] += ';C:\\TwinCAT\\AdsApi\\TcAdsDll\\'
import pyads


# create some constants for connection
CLIENT_NETID = "192.168.1.10.1.1"
CLIENT_IP = "10.171.108.11"
TARGET_IP = "10.171.108.11"
TARGET_USERNAME = "Administrator"
TARGET_PASSWORD = ""
ROUTE_NAME = "SN_Quality"

# add a new route to the target plc
pyads.add_route_to_plc(
    CLIENT_NETID, CLIENT_IP, TARGET_IP, TARGET_USERNAME, TARGET_PASSWORD,
    route_name=ROUTE_NAME
)
print("import dll")


# connect to plc and open connection using TwinCAT3.
# route is added automatically to client on Linux, on Windows use the TwinCAT router
print("start connection")
plc = pyads.Connection(CLIENT_IP, pyads.PORT_TC3PLC1)
print("start connection : open")
plc.open()

# check the connection state
print("connected : state")
plc_stat = plc.read_state()
print("start connection : state\n", plc_stat)
#(0, 5)
i:str
# read int value by name
print("connected : read")
address = "Global_Variables.TIME_NOW"
i = plc.read_by_name(address,pyads.PLCTYPE_STRING)
print(f"Value {address} : {i}")
# write int value by name
# plc.write_by_name("GVL.real_val", 42.0)

# create a symbol that automatically updates to the plc value
# real_val = plc.get_symbol("GVL.real_val", auto_update=True)
# print(real_val.value)
# #42.0
# real_val.value = 5.0
# print(plc.read_by_name("GVL.real_val"))
# #5.0

# close connection
plc.close()