from abc import ABC, abstractmethod
import numpy as np
from pypardiso import spsolve
from scipy.integrate import solve_ivp
import scipy.sparse as sp
from typing import TypeVar

from .utils import derivative


class Equation:
    def __init__(self, name, init_params, n_x, field_names=['u'],
                 sparse=True, moving=False):
        self.name = name
        self.init_params = init_params
        self.n_x = n_x
        self.field_names = field_names

        self.n_fields = len(field_names)
        self._N = self.n_x * self.n_fields
        self.parameters = init_params.copy()

        self.extract = {}
        self.sparse = sparse

        self.moving = moving

        if self.sparse:
            self.solver = spsolve
            self.hstack = lambda x: sp.hstack(x, format='csc')
            self.vstack = lambda x: sp.vstack(x, format='csc')
        else:
            self.solver = np.linalg.solve
            self.hstack = np.hstack
            self.vstack = sp.vstack

        self.w_x = 0.5

    @abstractmethod
    def F(self, x, eta):
        pass

    @abstractmethod
    def J(self, x, eta):
        pass

    @abstractmethod
    def F_eta(self, x, eta):
        pass

    def F_dns(self, t, x, eta):
        return self.F(x, eta)

    def J_dns(self, t, x, eta):
        return self.J(x, eta)

    def get_eta(self, Y):
        return Y[-1]

    def unpack(self, Y):
        return Y[:self._N], *Y[self._N:]

    def pack(self, x, *args):
        return np.append(x, args)

    def solve_dns(self, t_span, x0, t_eval, **kwargs):
        def F_dns(t, x0, eta):
            return self.F(x0, eta)
        return solve_ivp(F_dns, t_span, x0, t_eval=t_eval, **kwargs).y

    def get_param(self, pname):
        if pname in self.parameters:
            return self.parameters[pname]

    def set_param(self, pname, pval):
        if pname in self.parameters:
            self.parameters[pname] = pval

    def set_n_x(self, n_x):
        self.n_x = n_x
        self._N = self.n_x * self.n_fields

        if self.moving:
            self._Dx = self.first_derivative_matrix()

    def set_n_x_like(self, Y):
        n_x = self.get_n_x_from_profile_len(len(Y))
        self.set_n_x(n_x)

    def get_n_x_from_profile_len(self, profile_len):
        if self.moving:
            return int(round((profile_len - 2) / self.n_fields))
        return int(round((profile_len - 1) / self.n_fields))
    
    def to_plot(self, Y):
        return self.unpack(Y)[0]

    def get_params(self, pnames: str):
        pnames_list = pnames.split(' ')
        return [self.get_param(pname) for pname in pnames_list]
    
    def get_param_names(self):
        return self.parameters.keys()

    def rhs_palc(self, Y):
        if self.moving:
            return self.rhs_palc_moving(Y)
        
        x, eta = self.unpack(Y)
        x0, eta0 = self.unpack(self.Y0)
        xdot0, etadot0 = self.unpack(self.tau0)

        dF = self.F(x, eta)

        s = np.dot(Y - self.Y0, self.tau0) - self.ds
        return self.pack(dF, s)
    
    def rhs_palc_moving(self, Y):
        x, v, eta = self.unpack(Y)
        x0, v0, eta0 = self.unpack(self.Y0)

        dF = self.F(x, eta) + v * self.first_derivative(x)

        p = np.dot(x, self.first_derivative(x0)) * self.get_param('dx')
        s = np.dot(Y - self.Y0, self.tau0) - self.ds
        return self.pack(dF, [p, s])
    
    def first_derivative(self, x):
        raise NotImplementedError
    
    def jacobian_palc(self, Y, for_tangent=False):
        if self.moving:
            return self.jacobian_palc_moving(Y, for_tangent=for_tangent)
        
        x, eta = self.unpack(Y)

        jac = self.J(x, eta)
        
        # Deriv of F w/r to param
        last_col = self.F_eta(x, eta).reshape(self._N, 1)

        if for_tangent:
            return jac, last_col.ravel()

        last_row = self.tau0

        if self.sparse:
            jac = sp.hstack([jac, last_col], format='csc')
            jac = sp.vstack([jac, last_row], format='csc')
        else:
            jac = np.hstack([jac, last_col])
            jac = np.vstack([jac, last_row])

        return jac
    
    def jacobian_palc_moving(self, Y, for_tangent=False):
        x, v, eta = self.unpack(Y)
        x0, v0, eta0 = self.unpack(self.Y0)

        jac = self.J(x, eta) + v * self._Dx
        
        # Deriv of F w/r to param
        last_col = np.append(self.F_eta(x, eta), 0).reshape(self._N+1, 1)

        # Deriv of F w/r to speed
        prev_col = self.first_derivative(x).reshape(self._N, 1)
        prev_row = np.append(self.first_derivative(x0), 0) * self.get_param('dx')

        jac = self.hstack([jac, prev_col])
        jac = self.vstack([jac, prev_row])

        if for_tangent:
            return jac, last_col.ravel()

        last_row = self.tau0

        jac = self.hstack([jac, last_col])
        jac = self.vstack([jac, last_row])

        return jac 
       
    def get_tangent(self, Y, prev_tau):
        reduced_jac, rhs = self.jacobian_palc(Y, for_tangent=True)

        tau = self.solver(reduced_jac, -rhs)
        tau = np.append(tau, 1)

        if np.dot(tau, prev_tau) < 0:
            tau = -tau
        return tau / np.linalg.norm(tau)
    
    def get_xs(self):
        dx = self.get_param('dx')
        if dx is None:
            return np.arange(self.n_x)
        else:
            x0, xf = 0, self.n_x * dx
            return np.linspace(x0, xf, self.n_x, endpoint=False)

    def initialize_continuation(self, Y0, ds, w_x, prev_tau=None, direction='f',
                                eta=None):
        self.Y0 = Y0.copy()
        self.ds = ds
        self.w_x = w_x

        if eta:
            self.eta = eta

        if prev_tau is None:
            prev_tau = np.zeros_like(Y0)
            if direction == 'f':
                prev_tau[-1] = 1
            else:
                prev_tau[-1] = -1

        self.tau0 = self.get_tangent(Y0, prev_tau)
        
    def save_profile(self, Y, filename):
        np.save(filename, Y)


equation = TypeVar('equation', bound=Equation)
