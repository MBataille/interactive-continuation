import numpy as np
from .equation import Equation
import scipy.sparse as sp
from scipy.optimize import fsolve

from .utils import derivative_matrix, derivative

from findiff import FinDiff
dx = 0.25





class SwiftHohenberg(Equation):
    def __init__(self, n_x=None):
        init_params = {
            'nu' : 1.0,
            'epsilon': -0.2,
            'dx': 0.25,
            'n_x': 512,  
        }
        if n_x is None:
            n_x = init_params['n_x']

        super().__init__('SHE', init_params,
                         n_x, field_names=['u'], sparse=True)
        
        self.param_cont = 'epsilon'
        self.extract = {'L2': self.get_L2, 'F': self.free_energy}
        self.set_n_x(n_x)

    def get_L2(self, Y):
        x = self.unpack(Y)[0]
        return np.sum(x * x) / self.n_x

    def free_energy(self, Y):
        u, eta = self.unpack(Y)
        dF = - eta * u ** 2 - u ** 4 * 0.5 + u ** 6 / 3 - self.d_dx(u) ** 2 + self.d2_dx2(u) ** 2
        return np.sum(dF) / len(dF)

    def set_n_x(self, n_x):
        super().set_n_x(n_x)
        dx = self.get_param('dx')
        self.D2 = derivative_matrix(self.n_x, dx, order=2, acc=4, sparse=True)
        self.D4 = derivative_matrix(self.n_x, dx, order=4, acc=4, sparse=True)

        self.d2_dx2 = FinDiff(0, dx, 2)
        self.d_dx = FinDiff(0, dx, 1)

    def F(self, X, eta):
        nu, dx = self.get_params('nu dx')
        
        u = X[:self.n_x]
        D2u = derivative(u, dx, order=2, acc=4)
        D4u = derivative(u, dx, order=4, acc=4)

        return eta * u + u ** 3 - u ** 5 - nu * D2u - D4u
    
    def J(self, X, eta):
        u = X[:self.n_x]

        nu = self.get_param('nu')
        diag = sp.diags([eta + 3 * u ** 2 - 5 * u ** 4], offsets=[0], format='csc')

        return diag - nu * self.D2 - self.D4
    
    def F_eta(self, X, eta):
        u = X[:self.n_x]

        dF = np.zeros_like(X)
        dF[:self.n_x] = u

        return dF