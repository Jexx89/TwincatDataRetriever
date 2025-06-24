'''

TODO : 
* import DLL twincat automatically (consider the application on a computer with twincat not installed)
)) only to initiate the branch "dev"
'''

# %% import library

from time import sleep
from PLC_Manager import PLC_Manager as PLC

def main():
    manager = PLC()
    manager.start()
    manager.record()

    sleep(30)

    manager.close()
    


# %% testing
if __name__ == '__main__':
    main()