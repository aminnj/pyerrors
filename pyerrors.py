# -*- coding: UTF-8 -*-

import operator

hypot = lambda a,b: (a**2.+b**2.)**0.5

class E:
    """
    Properly propagates errors using all standard operations.
    Doesn't handle correlations.
    """
    def __init__(self, val, err=None):
        # assume poisson
        if err is None: err = abs(1.0*val)**0.5
        self.val, self.err = 1.0*val, 1.0*err

    def _addsub(self,other,op):
        other_val, other_err = self.get_val(other)
        new_val = op(self.val,other_val)
        new_err = hypot(self.err,other_err)
        return E(new_val, new_err)

    def _muldiv(self,other,op,rev=False):
        other_val, other_err = self.get_val(other)
        if rev:
            new_val = op(other_val,self.val)
        else:
            new_val = op(self.val,other_val)
        rel_err = hypot(self.err/self.val, other_err/other_val)
        new_err = rel_err*new_val
        return E(new_val, new_err)

    def __add__(self, other):
        return self._addsub(other,operator.__add__)

    def __radd__(self, other):
        return self._addsub(other,operator.__add__)

    def __sub__(self, other):
        return self._addsub(other,operator.__sub__)

    def __rsub__(self, other):
        return self._addsub(other,operator.__rsub__)

    def __mul__(self, other):
        return self._muldiv(other,operator.__mul__)

    def __rmul__(self, other):
        return self._muldiv(other,operator.__mul__)

    def __div__(self, other):
        return self._muldiv(other,operator.__div__)

    def __rdiv__(self, other):
        return self._muldiv(other,operator.__div__,rev=True)

    def __pow__(self, other):
        other_val, other_err = self.get_val(other)
        new_val = self.val ** other_val
        new_err = self.val**(other_val-1)
        if other_err > 0.:
            from numpy import log
            new_err *= (other_val**2*self.err**2 + self.val**2*other_err**2*log(self.val)**2)**0.5
        else:
            new_err *= other_val * self.err
        return E(new_val, new_err)

    def __neg__(self):
        return E(-1.*self.val, self.err)

    def __lt__(self, other):
         return self.val < other.val

    def __eq__(self, other):
         return (abs(self.val - other.val) < 1.e-6) and (abs(self.err - other.err) < 1.e-6)

    def __getitem__(self, idx):
        if idx==0: return self.val
        elif idx in [1,-1]: return self.err
        else: raise IndexError

    def rep(self,use_ascii=False):
        if use_ascii:
            sep = "+-"
        else:
            sep = u"\u00B1".encode("utf-8")
        if type(self.val).__name__ == "ndarray":
            import numpy as np
            # trick:
            # want to use numpy's smart formatting (truncating,...) of arrays
            # so we convert value,error into a complex number and format
            # that 1D array :)
            formatter = {"complex_kind": lambda x:"%5.2f {} %4.2f".format(sep) % (np.real(x),np.imag(x))}
            return np.array2string(self.val+self.err*1j,formatter=formatter, suppress_small=True, separator="   ")
        else:
            return "%s %s %s" % (str(self.val), sep, str(self.err))

    __str__ = rep

    __repr__ = rep

    def get_val(self, other):
        other_val, other_err = other, 0.0
        if type(other)==type(self):
            other_val, other_err = other.val, other.err
        return other_val, other_err

    def round(self, ndec):
        if ndec == 0:
            self.val = int(self.val)
        else:
            self.val = round(self.val,ndec)
        self.err = round(self.err,ndec)
        return self

    def to_list(self):
        return [self.__class__(*x) for x in zip(self.val,self.err)]

    def __array__(self):
        return np.array(self.to_list())

if __name__ == "__main__":
    pass
