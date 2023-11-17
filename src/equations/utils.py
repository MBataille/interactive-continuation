import numpy as np
import findiff as fd
import scipy.sparse as sp
from pypardiso import spsolve


def riemann_sum(u: np.ndarray, dt: float):
    """Returns the integral (computed as the Riemann sum) of a 1D array"""
    return np.sum(u) * dt


def diagonal_matrix(diag_val, N, k):
    return np.diag(np.zeros(N-abs(k)) + diag_val, k=k)


def get_finite_difference_coefficients(order, acc):
    d = fd.coefficients(order, acc)['center']
    return d['coefficients'], d['offsets']


def forward_derivative(u, dt, axis=1):
    return (np.roll(u, -1, axis=axis) - u) / dt


def forward_derivative_matrix(n_t, dt, sparse=False):
    if sparse:
        D = sp.diags([1/dt, -1/dt], offsets=[1, 0],
                     shape=(n_t, n_t), format='csc')
    else:
        D = np.eye(n_t, k=1) / dt - np.eye(n_t, k=0) / dt
    D[-1, 0] = 1/dt
    return D


def derivative(u: np.ndarray, dt: float, axis: int = 1, order=1, acc=2):
    coefs, offsets = get_finite_difference_coefficients(order, acc)
    du = np.zeros_like(u)
    for i, coef in enumerate(coefs):
        offset = i - (len(coefs) - 1) // 2
        du += coef * np.roll(u, -offset, axis=axis)
    return du / dt ** order


def get_ik(n_x: int, dx: float):
    return 2j * np.pi / dx * np.fft.fftfreq(n_x)


def spectral_derivative(u_ft: np.ndarray, dx: np.float, order=1):
    ik = get_ik(u_ft.shape[0], dx) ** order
    return np.fft.ifft(ik * u_ft).real


def spectral_derivative_matrix(n_x, dx, order=1):
    ik = get_ik(n_x, dx) ** order
    ik_ift = np.fft.ifft(ik).real

    D = np.zeros((n_x, n_x))
    for k in range(n_x):
        D[k] = np.roll(ik_ift, k)
    
    return D


def derivative_matrix(n_t, dt, order=1, acc=2, sparse=False, kind='center'):
    coefs_dict = fd.coefficients(order, acc)[kind]
    coefs = coefs_dict['coefficients']
    offsets = coefs_dict['offsets']

    D = np.zeros((n_t, n_t))
    for coef, offset in zip(coefs, offsets):
        D += diagonal_matrix(coef, n_t, offset)

        # periodic boundary conditions
        aoff = abs(offset)
        for i in range(aoff):
            j = n_t - aoff + i
            row, col = (i, j) if offset < 0 else (j, i)
            D[row, col] = coef

    D = D / dt ** order
    if sparse:
        return sp.csc_matrix(D)
    return D


def newton(func, jac, X, max_iter=20, atol=1e-9, verbose=False, sparse=True,
           callback=None, solver=None, damping=1.0, maxerr=1, max_step=1.0):
    xi = X.copy()
    if solver is None:
        solver = spsolve if sparse else np.linalg.solve

    fxi = func(xi)
    err = np.abs(fxi).sum() / len(fxi)

    # return value
    R = None

    if verbose:
        msg = f'Step 0: |F| = {err:.4e}, eta = {xi[-1]:.5f}'

    for n_iter in range(max_iter):
        delta = solver(jac(xi), fxi)
        if abs(delta[-1]) > max_step:
            xi -= delta * max_step / abs(delta[-1])
        else:
            xi -= delta * damping
        fxi = func(xi)
        err = np.abs(fxi).sum() / len(fxi)

        if verbose:
            msg += f'\nStep {n_iter}: |F| = {err:.4e}, '\
                    + f'Delta = {np.abs(delta).sum() / len(delta):.4e}, ' \
                    + f', eta = {xi[-1]:.5f}'

        if callback:
            callback(xi)

        if err < atol:
            R = xi
            break

        if err > maxerr:
            break

    if verbose:
        return R, msg
    return R
