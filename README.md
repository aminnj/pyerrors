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
>>> v,e = E(10)
>>> print v,e
10.0 3.16227766017
>>> vs = sum([E(i) for i in range(10)])
>>> vs
45.0 ± 6.7082039325
```

### Install
`pip install pyerrors==1.0.0`

### Testing
`python tests.py`

### TODO
