import numpy as np
from .equation import Equation
import scipy.sparse as sp

from .utils import derivative_matrix, derivative


class LugiatoLeveferDiffusion(Equation):
    """Class representing the Lugiato-Lefever equation,
        dA/dt = S - (1 + i Delta) A - i beta_2  d2A/dx2 + i |A|^2 A."""
    def __init__(self, n_x=None):
        init_params = {
            'beta2': -1,
            'Delta': 6.25,
            'S': 3.0,
            'n_x': 512,
            'dx': 0.05,
            'epsilon': 0.02
        }
        if n_x is None:
            n_x = init_params['n_x']

        super().__init__('LLE_diffusion', init_params, n_x,
                         field_names=['Re E', 'Im E'], sparse=True)
        
        self.extract = {'L2': self.get_L2}
        self.set_n_x(n_x)


    def F(self, X, eta, flatten=True):
        u, v = X[:self.n_x].ravel(), X[self.n_x:].ravel()

        dF = np.zeros_like(X)
        squared = (u * u + v * v)

        dx, delta, beta2, epsilon = self.get_params('dx Delta beta2 epsilon')

        D2u = derivative(u, dx, axis=0, order=2, acc=8)
        D2v = derivative(v, dx, axis=0, order=2, acc=8)

        dF[:self.n_x] = eta - u + delta * v - v * squared \
            + beta2 * D2v + epsilon * D2u
        dF[self.n_x:] = -delta * u - v + u * squared \
            - beta2 * D2u + epsilon * D2v
        
        return dF

    def J(self, X, eta, time=True):
        U, V = X[:self.n_x], X[self.n_x:]

        u, v = U.ravel(), V.ravel()

        delta = self.get_param('Delta')

        principal_diag = np.append(-2 * u * v - 1, 2 * u * v - 1)
        upper_diag = delta - u * u - 3 * v * v
        lower_diag = -delta + 3 * u * u + v * v

        jac_homo = sp.diags([principal_diag, lower_diag, upper_diag],
                            offsets=[0, -self.n_x, self.n_x], format='csc')
        return jac_homo + self.Dxx

    def F_eta(self, X, eta):
        dF = np.zeros_like(X)
        dF[:self.n_x] = 1
        return dF

    def set_n_x(self, n_x):
        super().set_n_x(n_x)
        dx, beta2, epsilon = self.get_params('dx beta2 epsilon')
        D = derivative_matrix(self.n_x, dx, order=2, acc=8, sparse=True)
        self.Dxx = sp.kron(np.array([[epsilon, beta2],
                                     [-beta2, epsilon]]),
                           D, format='csc')

    def to_plot(self, Y):
        x = self.unpack(Y)[0]
        return x[:self.n_x] ** 2 + x[self.n_x:] ** 2

    def get_L2(self, Y):
        x = self.unpack(Y)[0]
        mod2 = x[:self.n_x] ** 2 + x[self.n_x:] ** 2
        l2 = np.sum(mod2, axis=0) / self.n_x

        return l2.mean()
