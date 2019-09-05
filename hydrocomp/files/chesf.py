"""
Created on 21 de mar de 2018

@author: clebson
"""

from hydrocomp.files.fileRead import FileRead


class Chesf(FileRead):

    extension = "xls"
    source = "CHESF"

    def __init__(self):
        pass
