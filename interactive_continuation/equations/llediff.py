import numpy as np
from .equation import Equation
import scipy.sparse as sp
from scipy.optimize import fsolve

from .utils import derivative_matrix, derivative


class LugiatoLeveferDiffusion(Equation):
    """Class representing the Lugiato-Lefever equation,
        dA/dt = S - (1 + i Delta) A - i beta_2  d2A/dx2 + i |A|^2 A."""
    def __init__(self, n_x=None):
        init_params = {
            'beta2': -1,
            'Delta': 1.7,
            'S': 1.215,
            'n_x': 512,
            'dx': 0.05,
            'epsilon': 0.1,
            'alpha1': 0.1
        }
        if n_x is None:
            n_x = init_params['n_x']

        super().__init__('LLE_diffusion', init_params, n_x,
                         field_names=['Re E', 'Im E'], sparse=True,
                         moving=True)
        
        self.param_cont = 'alpha1'
        self.extract = {'L2': self.get_L2, 'L2-HSS': self.get_L2_minus_homogeneous}
        self.set_n_x(n_x)

    def first_derivative(self, X):
        u, v = X[:self.n_x].ravel(), X[self.n_x:].ravel()

        dx = self.get_param('dx')

        Du = derivative(u, dx, axis=0, order=1, acc=8)
        Dv = derivative(v, dx, axis=0, order=1, acc=8)

        return np.append(Du, Dv)
    
    def first_derivative_matrix(self):
        dx = self.get_param('dx')
        D = derivative_matrix(self.n_x, dx, order=1, acc=8, sparse=True)
        return sp.kron(np.eye(2), D, format='csc')

    def F(self, X, eta, flatten=True):
        u, v = X[:self.n_x].ravel(), X[self.n_x:].ravel()

        dF = np.zeros_like(X)
        squared = (u * u + v * v)

        if self.param_cont == 'S':
            S = eta
            alpha1 = self.get_param('alpha1')
        elif self.param_cont == 'alpha1':
            S = self.get_param('S')
            alpha1 = eta
        else:
            raise ValueError(f'Could not recognize {self.param_cont} as a continuation parameter.')

        dx, delta, beta2, epsilon = self.get_params('dx Delta beta2 epsilon')

        Du = derivative(u, dx, axis=0, order=1, acc=8)
        Dv = derivative(v, dx, axis=0, order=1, acc=8)

        D2u = derivative(u, dx, axis=0, order=2, acc=8)
        D2v = derivative(v, dx, axis=0, order=2, acc=8)

        dF[:self.n_x] = S - u + delta * v - v * squared \
            + beta2 * D2v + epsilon * D2u + alpha1 * Dv
        dF[self.n_x:] = -delta * u - v + u * squared \
            - beta2 * D2u + epsilon * D2v - alpha1 * Du
        
        return dF

    def J(self, X, eta, time=True):
        U, V = X[:self.n_x], X[self.n_x:]

        u, v = U.ravel(), V.ravel()

        if self.param_cont == 'S':
            S = eta
            alpha1 = self.get_param('alpha1')
        elif self.param_cont == 'alpha1':
            S = self.get_param('S')
            alpha1 = eta
        else:
            raise ValueError(f'Could not recognize {self.param_cont} as a continuation parameter.')

        delta = self.get_param('Delta')

        principal_diag = np.append(-2 * u * v - 1, 2 * u * v - 1)
        upper_diag = delta - u * u - 3 * v * v
        lower_diag = -delta + 3 * u * u + v * v

        jac_homo = sp.diags([principal_diag, lower_diag, upper_diag],
                            offsets=[0, -self.n_x, self.n_x], format='csc')
        
        return jac_homo + self.Dxx + self.D * alpha1

    def F_eta(self, X, eta):
        dF = np.zeros_like(X)
        dx = self.get_param('dx')

        if self.param_cont == 'S':
            dF[:self.n_x] = 1
        elif self.param_cont == 'alpha1':
            u, v = X[:self.n_x].ravel(), X[self.n_x:].ravel()
            dF[:self.n_x] = derivative(v, dx, axis=0, order=1, acc=8)
            dF[self.n_x:] = -derivative(u, dx, axis=0, order=1, acc=8)
        else:
            raise ValueError(f'Could not recognize {self.param_cont} as a continuation parameter.')

        return dF

    def set_n_x(self, n_x):
        super().set_n_x(n_x)
        dx, beta2, epsilon, alpha1 = self.get_params('dx beta2 epsilon alpha1')
        D2 = derivative_matrix(self.n_x, dx, order=2, acc=8, sparse=True)
        self.Dxx = sp.kron(np.array([[epsilon, beta2],
                                     [-beta2, epsilon]]),
                           D2, format='csc')
        
        D = derivative_matrix(self.n_x, dx, order=1, acc=8, sparse=True)
        self.D = sp.kron(np.array([[0, 1.0],
                                    [-1.0, 0]]),
                            D, format='csc')

    def to_plot(self, Y):
        x = self.unpack(Y)[0]
        return x[:self.n_x] ** 2 + x[self.n_x:] ** 2

    def get_L2(self, Y):
        x = self.unpack(Y)[0]
        mod2 = x[:self.n_x] ** 2 + x[self.n_x:] ** 2
        l2 = np.sum(mod2, axis=0) / self.n_x

        return l2.mean()
    
    def get_homogeneous(self, S, A0):
        delta = self.get_param('Delta')
        
        def rhs_hss(X):
            u, v = X
            mod2 = u ** 2 + v ** 2
            return np.array([
                S - u + delta * v - v * mod2,
                u * mod2 - (v + delta * u)
            ])
            
        def jac_hss(X):
            u, v = X
            return np.array([
                [-1 - 2 * u * v, delta - 3 * v ** 2 - u ** 2],
                [-delta + 3 * u ** 2 + v ** 2, 2 * u * v - 1]
            ])
        
        X0 = np.array([A0.real, A0.imag])
        A_h = fsolve(rhs_hss, X0, fprime=jac_hss)
        
        return A_h[0] + 1j * A_h[1]
    
    def get_L2_minus_homogeneous(self, Y):
        x = self.unpack(Y)[0]
        eta = self.unpack(Y)[-1]
        A = x[:self.n_x] + 1j * x[self.n_x:]
        A_h = self.get_homogeneous(eta, A.mean())      
        mod2 = np.abs(A - A_h) ** 2  

        return np.sum(mod2, axis=0) / self.n_x