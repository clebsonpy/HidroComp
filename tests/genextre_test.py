from unittest import TestCase
from statistic.genextre import Gev

class TestGev(TestCase):

    data = [1347,  857, 1626,  977, 1065,  997,  502, 1663,  992, 
            1487, 1041, 2251, 1110, 1553, 1090, 1268, 1113, 1358,  402]
    
    mml = (0.24684253029124203, 1023.9891165624797, 380.3053838205217)
    mvs = (-5.83785197466355, 403.3270953313672, 7.747500635081945)

    def test(self):
        self.assertEquals(Gev(data=self.data).mml(), self.mml)
