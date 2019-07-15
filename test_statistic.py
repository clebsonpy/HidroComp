from unittest import TestCase, main
from statistic.genextre import Gev

from statistic.exceptions import DataNotExist

class TestGev(TestCase):

    data = [1347,  857, 1626,  977, 1065,  997,  502, 1663,  992, 
            1487, 1041, 2251, 1110, 1553, 1090, 1268, 1113, 1358,  402]
    dist = Gev(data=data)
    
    def test_dist(self):
        name = 'GEV'
        self.assertEquals(self.dist.name, name, 'Name: GEV')

    def test_mml(self):
        mml = (0.14684253029124203, 1023.9891165624797, 380.3053838205217)
        self.assertEquals([self.dist.mml(), self.dist.estimador], [mml, 'MML'], 'Fit_MML: %s, %s, %s' % mml)

    def test_mvs(self):
        mvs = (-5.83785197466355, 403.3270953313672, 7.747500635081945)
        self.assertEquals([self.dist.mvs(), self.dist.estimador], [mvs, 'MVS'], 'Fit_MVS: %s, %s, %s' % mvs)

    def test_prob(self):
        prob_mml = 0.7781690064347855
        prob_mvs = 0.7287813740394129
        self.dist.mml()
        self.assertEquals(self.dist.probs(1500), prob_mml, 'Prob: %s' % prob_mml)
        self.dist.mvs()
        self.assertEquals(self.dist.probs(1500), prob_mvs, 'Prob: %s' % prob_mvs)

    def test_value(self):
        value_mml = 1456.9948303470273
        value_mvs = 2314.9143444142505
        self.dist.mml()
        self.assertEquals(self.dist.values(0.75), value_mml, 'Value: %s' % value_mml)
        self.dist.mvs()
        self.assertEquals(self.dist.values(0.75), value_mvs, 'Value: %s' % value_mvs)
    
    def test_values(self):
        value_mvs = [2314.9143444142505, 413.27574336098405]
        value_mml = [1456.9948303470273, 1159.6914703217076]
        self.dist.mml()
        self.assertEquals(self.dist.values([0.75, 0.5]), value_mml, 'Value: %s' % value_mml)
        self.dist.mvs()
        self.assertEquals(self.dist.values([0.75, 0.5]), value_mvs, 'Value: %s' % value_mvs)

    def test_probs(self):
        prob_mml = [0.7781690064347855, 0.34479635611222237]
        prob_mvs = [0.7287813740394129, 0.7039216570017871]
        self.dist.mml()
        self.assertEquals(self.dist.probs([1500, 1000]), prob_mml, 'Prob: %s' % prob_mml)
        self.dist.mvs()
        self.assertEquals(self.dist.probs([1500, 1000]), prob_mvs, 'Prob: %s' % prob_mvs)

    def test_interval(self):
        ic_mvs = (402.00217396627875, 45018159.2649536)
        ic_mml = (571.2282612439494, 1939.4616813678326)
        self.dist.mml()
        self.assertEquals(self.dist.interval(0.9), ic_mml, 'Value: (%s, %s)' % ic_mml)
        self.dist.mvs()
        self.assertEquals(self.dist.interval(0.9), ic_mvs, 'Value: (%s, %s)' % ic_mvs)



if __name__ == "__main__":
    main()

    test_gev = TestGev()
    test_gev.test_mml()
    test_gev.test_mvs()
    test_gev.test_prob()
    test_gev.test_value()
    test_gev.test_interval()

    print("Tudo certo!")