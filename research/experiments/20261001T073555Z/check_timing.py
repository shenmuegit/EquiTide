"""Boundary check: maturity uses publication time, not just realized label exit."""
import numpy as np
from ridge import train_mask,fit_ridge
# Last entry closes before cutoff but publishes at cutoff: must be purged.
t=np.array([0,10,20,30]);ends=np.array([5,15,25,35]);available=np.array([5,20,40,35]);cutoff=40
assert train_mask(t,ends,available,0,cutoff).tolist()==[True,True,False,True]
# Publication after cutoff and decision outside interval cannot enter fitting.
assert not train_mask(t,ends,np.array([41,20,30,35]),0,cutoff)[0]
assert not train_mask(t,ends,available,10,30)[0]
# Changing only a withheld row does not change scaler or learned parameters.
x=np.array([[1.,2.],[2.,3.],[3.,4.],[999.,999.]]);y=np.array([1.,2.,3.,999.]);mask=np.array([1,1,1,0],dtype=bool)
a=fit_ridge(x[mask],y[mask],1);x[-1]=[-999,-999];y[-1]=-999;b=fit_ridge(x[mask],y[mask],1)
np.testing.assert_array_equal(a.named_steps['scale'].mean_,b.named_steps['scale'].mean_);np.testing.assert_array_equal(a.named_steps['model'].coef_,b.named_steps['model'].coef_)
print('PASS: mature publication cutoff, chronological boundaries and withheld-data perturbation')
