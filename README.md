### Description

This is a simple error propagation library that does not handle correlations. However, in most cases, clever
writing can eliminate the need for properly handling correlations. The unit tests in
`tests.py` show most of the features of the library. In a nutshell, you can do
```python
>>> from pyerrors import E
>>> a = E(10) # instantiates an error object with poisson error by default (10.0 ± 3.16)
>>> b = E(10,2) # specified error (10.0 ± 2.0)
>>> (4.0*a-2*b)/3
6.66666666667 ± 4.42216638714
>>> ((4.0*a-2*b)/3).round(2)
6.67 ± 4.42
>>> # unpack as a 2-tuple, or by index
>>> v,e = E(10)
>>> print v,e
10.0 3.16227766017
>>> # sum
>>> print sum([E(i) for i in range(10)])
45.0 ± 6.7082039325
>>> # nice repr when using numpy inputs
>>> import numpy as np
>>> counts = np.histogram(np.random.normal(0,1,100),bins=np.linspace(-4,4,8))[0]
>>> va = E(counts)
>>> print va
[ 0.00 ± 0.00    2.00 ± 1.41   21.00 ± 4.58   47.00 ± 6.86   27.00 ± 5.20    3.00 ± 1.73    0.00 ± 0.00]
>>> # but numpy requires some coersion afterwards (see the relevant test case in `tests.py` for details)
>>> print sum(va.to_list())
100.0 ± 10.0
```

### Install
`pip install pyerrors==1.0.0`

### Testing
`python setup.py test`

### TODO
