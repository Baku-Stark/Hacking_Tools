"""
    Profile 
    ---------- 
    Author : Baku - Stark 
    Info   : Application colors. 
"""

import os
from platform import *
from datetime import datetime
  
class Colors:
    BLACK =     '\033[1;30m'
    RED =       '\033[31m'
    GREEN =     '\033[32m'
    YELLOW =    '\033[33m'
    BLUE =      '\033[34m'
    PURPLE =    '\033[35m'
    CYAN =      '\033[36m'
    WHITE =     '\033[37m'
    GRAY =      '\033[90m'
  
    BACK_RED =       '\033[1;41m'
    BACK_GREEN =     '\033[1;42m'
    BACK_YELLOW =    '\033[1;43m'
    BACK_BLUE =      '\033[1;44m'
    BACK_PURPLE =    '\033[1;45m'
    BACK_CYAN =      '\033[1;46m'
    BACK_WHITE =     '\033[1;47m'
    BACK_GRAY =      '\033[1;40m'
  
    END =       '\033[m'

class OperationalSys:
    @staticmethod
    def clean_console():
        if system() == "Linux":
            os.system("clear")

        else:
            os.system("cls")

class CurrentTime:
    @staticmethod
    def created_at() -> str:
        _data_atual = datetime.now().strftime("%d/%m/%y")
        _hora_atual = datetime.now().strftime("%H:%M")
        return f"{_data_atual} - {_hora_atual}"
