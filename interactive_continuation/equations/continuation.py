import numpy as np
import pandas as pd
import os
from pathlib import Path
from threadpoolctl import threadpool_limits

from .equation import equation
from .llediff import LugiatoLeveferDiffusion
from .llediff_fft import LugiatoLeveferDiffusionFFT
from .utils import newton


EQUATIONS = {'LLE-D': LugiatoLeveferDiffusion,
             'LLE-D-FFT': LugiatoLeveferDiffusionFFT}

DATAFOLDER = Path(os.getcwd())
if DATAFOLDER.parts[-1] == 'src':
    DATAFOLDER = DATAFOLDER.parent()

DATAFOLDER = DATAFOLDER / 'data'

class Continuation:
    def __init__(self, eqn: equation, branchname, 
                 on_not_convergence=None):
        self.eqn = eqn
        self.on_not_convergence = on_not_convergence
        self.branchname = branchname

        self.Y0 = None
        self.cont_params = {'ds': 0.001,
                            'atol': 1e-9,
                            'w_x': 0.99}

        self.initialize_extract(self.eqn.extract)
        self.data = {scalar: [] for scalar in self.extract}
        
        self.continuation_count = 0

    def set_branchname(self, branchname):
        self.branchname = branchname
        self.branchfolder = DATAFOLDER / branchname

        if not self.branchfolder.exists():
            os.mkdir(self.branchfolder)

    def get_eta(self, Y):
        return self.eqn.unpack(Y)[-1]

    def get_max(self, Y):
        u = self.eqn.unpack(Y)[0]
        return np.max(u)

    def initialize_extract(self, extract: dict):
        if not extract:  # if empty
            extract = {'max': self.get_max}
        self.extract = {'eta': self.eqn.get_eta,
                        **extract}

    def append_scalars(self, Y):
        for scalar in self.extract:
            self.data[scalar].append(self.extract[scalar](Y))

    def save_profile(self, Y, filename=None):
        if filename is None:
            filename = f'x{self.continuation_count}.npy'
        
        self.eqn.save_profile(Y, self.branchfolder / filename)

    def load_profile(self, filename):
        return np.load(filename)

    def load_initial_condition(self, filename):
        self.Y0 = self.load_profile(filename)
        self.eqn.set_n_x_like(self.Y0)
        self.append_scalars(self.Y0)
        self.save_profile(self.Y0)

    def save_branch(self):
        df = pd.DataFrame(self.data)
        df.to_csv(self.branchfolder / 's.csv')

    def initialize_continuation(self, ds=0.1, direction='forward', w_x=0.5,
                                **newton_kwargs):
        if self.Y0 is None:
            raise ValueError
        
        self.ds = ds
        self.direction = direction
        self.w_x = w_x

        self.newton_kwargs = newton_kwargs

        self.eqn.initialize_continuation(self.Y0, ds, w_x, 
                                         direction=direction[0],
                                         eta=self.Y0[-1])

    def palc_step(self):
        # with threadpool_limits(limits=4):
        Y, msg = newton(self.eqn.rhs_palc, self.eqn.jacobian_palc,
                        self.Y0 + self.eqn.tau0 * self.ds, verbose=True,
                        solver=self.eqn.solver, **self.newton_kwargs)

        if Y is None:
            return Y, msg

        self.continuation_count += 1

        self.Y0 = Y
        self.append_scalars(Y)
        self.save_profile(Y)
        self.eqn.initialize_continuation(Y, self.ds, self.w_x,
                                         prev_tau=self.eqn.tau0)
        return Y, msg

    def get_current_profile(self):
        return self.eqn.to_plot(self.Y0)
    
    def get_profile_curve(self):
        xs = self.eqn.get_xs()
        profile = self.get_current_profile()
        return xs, profile

    def get_current_eta(self):
        return self.eqn.unpack(self.Y0)[-1]
    
    def get_closest_point(self):
        pass

    def get_closest_profile(self):
        pass

    def set_eqn_params(self, pname, pval):
        self.eqn.set_param(pname, pval)
    
    def get_eqn_params(self):
        pass

    def get_bifurcation_curve(self, x_axis, y_axis):
        if x_axis in self.data and y_axis in self.data:
            return self.data[x_axis], self.data[y_axis]

    def get_scalar_names(self):
        return self.data.keys()
