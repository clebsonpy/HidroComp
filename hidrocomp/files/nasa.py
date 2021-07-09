"""
Created on 21 de mar de 2018

@author: clebson
"""
from hidrocomp.files.fileRead import FileRead


class Nasa(FileRead):
    """
    class files read: National Aeronautics and
                    Space Administration - NASA
    """
    source = "NASA"
    extension = "hdf5"
    
    def __init__(self, params):
        pass
