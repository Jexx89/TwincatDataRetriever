'''
TODO : make it so we can choose between SQL or Excel saving


'''
from dependency_injector import containers, providers
from ADS_route import ADS_route
from Excel_recording import Excel_recording
from PLCConnectionManager import PLCConnectionManager


class Container(containers.DeclarativeContainer):
    route_cfg = providers.Configuration()
    ads_route = providers.Singleton(ADS_route, route_cfg=route_cfg.app.token)
    excel_recording = providers.Singleton(Excel_recording,route_cfg=route_cfg.app.token)
    PLC = providers.Factory(PLCConnectionManager, ads_route=ads_route, excel_recording=excel_recording,route_cfg=route_cfg.app.token)
