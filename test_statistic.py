from unittest import TestCase, main
from statistic.genextre import Gev

from statistic.exceptions import DataNotExist

class TestGev(TestCase):

    data = [1347,  857, 1626,  977, 1065,  997,  502, 1663,  992, 
            1487, 1041, 2251, 1110, 1553, 1090, 1268, 1113, 1358,  402]
    
    def test_mml(self):
        mml = (0.14684253029124203, 1023.9891165624797, 380.3053838205217)
        self.assertEquals(Gev(data=self.data).mml(), mml, 'Fit_MML: %s, %s, %s' % mml)

    def test_mvs(self):
        mvs = (-5.83785197466355, 403.3270953313672, 7.747500635081945)
        self.assertEquals(Gev(data=self.data).mvs(), mvs, 'Fit_MVS: %s, %s, %s' % mvs)

    def test_prob(self):
        prob_mml = 0.7781690064347855
        prob_mvs = 0.7287813740394129

        self.assertEquals(Gev(data=self.data).prob(1500, estimador='mml'), prob_mml, 'Prob: %s' % prob_mml)
        self.assertEquals(Gev(data=self.data).prob(1500, estimador='mvs'), prob_mvs, 'Prob: %s' % prob_mvs)

    def test_value(self):
        value_mml = 1456.9948303470273
        value_mvs = 2314.9143444142505
        
        self.assertEquals(Gev(data=self.data).value(0.75, estimador='mml'), value_mml, 'Value: %s' % value_mml)
        self.assertEquals(Gev(data=self.data).value(0.75, estimador='mvs'), value_mvs, 'Value: %s' % value_mvs)
    
    def test_interval(self):
        pass

if __name__ == "__main__":
    main()

    test_gev = TestGev()
    test_gev.test_mml()
    test_gev.test_mvs()

    print("Tudo certo!")