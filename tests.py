import unittest

import numpy as np
from errors import E
import operator

np.set_printoptions(linewidth=120)

class HistTest(unittest.TestCase):

    def setUp(self):
        self.v1 = E(10.0,1.0)
        self.v2 = E(10.0,1.0) # same as v2
        self.v3 = E(10.0,2.0)
        self.v4 = E(20.0,1.0)


    def test_instantiation(self):
        ve = E(10)
        v,e = E(10) # can unpack as a 2-tuple
        self.assertEqual(ve[0], v) # and also by index
        self.assertEqual(ve[1], e)

        self.assertEqual(v, 10.0)
        self.assertEqual(e, 10**0.5) # poisson uncertainty by default
        self.assertEqual(ve, E(v,e))
        self.assertEqual(E(10,1.0)[1], 1.0)

    def test_equality(self):
        v1, v2, v3, v4 = self.v1, self.v2, self.v3, self.v4

        self.assertEqual(v1, v2)
        self.assertEqual(1.0*v1, v1)
        self.assertEqual(v1*1.0, v1)
        self.assertEqual(0.0+v1, v1)
        self.assertEqual(v1+0.0, v1)

    def test_addition_subtraction(self):
        v1, v2, v3, v4 = self.v1, self.v2, self.v3, self.v4

        self.assertEqual(v1+E(100,0.0)-E(100,0.0), v1) # add and subtract a 0-error number

        for sign in [1,-1]:

            v,e = v3+sign*v1
            self.assertEqual(v, v3[0]+sign*v1[0])
            self.assertEqual(e, (v3[1]**2.+v1[1]**2.)**0.5) # add errors in quadrature

            v,e = v1+sign*v3
            self.assertEqual(v, v1[0]+sign*v3[0])
            self.assertEqual(e, (v1[1]**2.+v3[1]**2.)**0.5) # add errors in quadrature

            v,e = v1+sign*5
            self.assertEqual(v, v1[0]+sign*5)
            self.assertEqual(e, v1[1])

            v,e = 5+sign*v1
            self.assertEqual(v, 5+sign*v1[0])
            self.assertEqual(e, v1[1])

    def test_multiplication_division(self):
        v1, v2, v3, v4 = self.v1, self.v2, self.v3, self.v4

        self.assertEqual(v1*E(100,0.0)/E(100,0.0), v1) # multiply and divide a 0-error number

        for op in [operator.__mul__, operator.__div__]:

            v,e = op(v3,v4)
            self.assertEqual(v, op(v3[0],v4[0]))
            rel_err = (((v3[1]/v3[0])**2.0 + (v4[1]/v4[0])**2.0))**0.5
            self.assertAlmostEqual(e, v*rel_err)

            v,e = op(v4,v3)
            self.assertEqual(v, op(v4[0],v3[0]))
            rel_err = (((v3[1]/v3[0])**2.0 + (v4[1]/v4[0])**2.0))**0.5
            self.assertAlmostEqual(e, v*rel_err)

            v,e = op(2,v4)
            self.assertEqual(v, op(2,v4[0]))
            rel_err = v4[1]/v4[0]
            self.assertAlmostEqual(e, v*rel_err)

    def test_power(self):
        v = E(10)
        self.assertAlmostEqual((v**E(2,0))[1],63.2455532034)
        self.assertAlmostEqual((v**2)[1],63.2455532034)
        self.assertAlmostEqual((v**E(2,0.001))[1],63.24597235382744)

    def test_broken_correlation(self):
        # correlation is broken and we want to make sure
        # that the universe didn't magically fix it somehow
        # e.g., beware of things like v1+v1-v1, which do not return v1 (error is inflated)
        v1 = self.v1
        self.assertEqual((v1+v1-v1)[0]==v1[0], True)
        self.assertEqual((v1+v1-v1)[1]>v1[1], True)
        self.assertEqual((v1*v1/v1)[0]==v1[0], True)
        self.assertEqual((v1*v1/v1)[1]>v1[1], True)

    def test_sorting(self):
        vs = [E(5),E(10),E(1),E(-3)]
        self.assertEqual([v[0] for v in vs], [5,10,1,-3])
        vs = sorted(vs)
        self.assertEqual([v[0] for v in vs], [-3,1,5,10])

    def test_summing(self):
        vs = [E(5),E(10),E(1),E(-3)]
        self.assertEqual(sum(vs)[0],sum([v[0] for v in vs]))

    def test_repr(self):
        v1 = E(10)
        
        self.assertEqual(v1.__str__(use_ascii=True).split()[1], "+-")
        self.assertEqual(v1.__repr__(use_ascii=True).split()[1], "+-")

        parts = str(v1).split()
        self.assertEqual(float(parts[0]), v1[0])
        self.assertAlmostEqual(float(parts[-1]), v1[1])

        # now round to 2 decimal places
        parts = str(v1.round(2)).split()
        self.assertEqual(parts[-1],"3.16")

    def test_numpy(self):
        import numpy as np
        counts = np.histogram(np.random.normal(0,1,100),bins=np.linspace(-4,4,8))[0]
        va = E(counts)
        # when putting in a numpy array, the val and err members
        # are themselves numpy arrays, and since math operations
        # are overloaded to be vectorized, error propagation works
        # mostly transparently (e.g., va+2 will do a vectorized
        # addition)
        self.assertEqual(len(va[0]),7) # 8-1=7 bins
        self.assertEqual(sum(va[0]),100) # 100 entries total
        self.assertEqual(len(va.val),7) # another way to access values
        self.assertEqual(len(va.err),7) # another way to access errors
        # however, we can't do sum(va), because va is a single element
        # we must convert va to a list of error objects first
        valist = va.to_list()
        self.assertEqual(len(valist),7)
        self.assertEqual(sum(valist),E(100,10))

if __name__ == "__main__":
    v = E(10)
    unittest.main()
