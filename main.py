'''

TODO : 
* import DLL twincat automatically (consider the application on a computer with twincat not installed)

'''

# %% import library
from ConfigFile import get_routes_config
from Container import Container
from time import sleep


# %% testing
if __name__ == '__main__':
    configurations = get_routes_config()
    ctns=[]
    for key, configuration in configurations.items():
        if configuration["ACTIVE"]:
            ctn=Container()
            ctn.route_cfg.app.token.from_env("APP_TOKEN", default=configuration)
            ctns.append(ctn.PLC())
    sleep(20)
    # To stop monitoring, call stop_monitoring() on each PLC manager
    for ctn in ctns:
        ctn.close_all()
    

        