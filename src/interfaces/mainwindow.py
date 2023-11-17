from PySide6 import QtWidgets
from PySide6.QtCore import QObject, QThread, Signal, QRunnable, QThreadPool

import logging
import numpy.typing as npt

from .mainwindow_ui import Ui_MainWindow
from src.equations.continuation import Continuation, EQUATIONS, DATAFOLDER

logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
c_handler.setFormatter(formatter)
logger.addHandler(c_handler)

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    result = Signal(object, str)

class ContinuationWorker(QRunnable):
    def __init__(self, continuation):
        super().__init__(self)
        self.continuation = continuation
        self.signals = WorkerSignals()
        self.is_killed = False

    def run(self):
        while not self.is_killed:
            Y, msg = self.continuation.palc_step()
            if Y is None:
                self.signals.error.emit(msg)
                break
            self.signals.result.emit(Y, msg)
        
        self.signals.finished.emit()

    def kill(self):
        self.is_killed = True

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.continuation = None
        self.is_continuating = False

        self.setupUi(self)
        self.init_eqns_combobox()


        # connect signals
        self.playpause_pushButton.clicked.connect(self.play)
        self.initcond_pushButton.clicked.connect(self.load_init_cond)

    def init_eqns_combobox(self):
        self.eqn_combobox.clear()
        self.eqn_combobox.currentIndexChanged.connect(self.select_eqn)
        self.eqn_combobox.addItems(EQUATIONS.keys())

    def select_eqn(self, index):
        selected_eqn_name = self.eqn_combobox.itemText(index)
        selected_eqn = EQUATIONS[selected_eqn_name]
        
        self.continuation = Continuation(selected_eqn(), '')
        logger.debug(f'Selected Equation: {selected_eqn_name}')

        self.init_xy_axis()
        self.init_cont_params()

    def init_xy_axis(self):
        axis_names = self.continuation.get_scalar_names()
        self.xaxis_combobox.addItems(axis_names)
        self.yaxis_combobox.addItems(axis_names)

        self.yaxis_combobox.setCurrentIndex(1)

    def set_current_branchname(self):
        new_branchname = self.branch_entry.text()
        self.continuation.set_branchname(new_branchname)

    def load_init_cond(self):
        initial_condition_name = self.initcond_entry.text()
        initial_condition_path = DATAFOLDER / initial_condition_name

        logger.debug(f'Loading initial condition: {initial_condition_name}')
        
        if initial_condition_path.exists():
            self.continuation.load_initial_condition(initial_condition_path)
            self.draw_profile_plot()
            self.draw_main_plot()

    def get_selected_axis(self):
        xaxis = self.xaxis_combobox.currentText()
        yaxis = self.yaxis_combobox.currentText()

        return xaxis, yaxis

    def draw_main_plot(self, data=None):
        if data is None:
            xaxis, yaxis = self.get_selected_axis()
            data = self.continuation.get_bifurcation_curve(xaxis, yaxis)

        xs, ys = data

        logger.debug(f'Drawing main plot')

        self.mainplot.plot(xs, ys, name='main_curve', clear=True)
        self.mainplot.plot([xs[-1]], [ys[-1]], name='main_marker', marker='o')

    def update_main_plot(self, data=None):
        if data is None:
            xaxis, yaxis = self.get_selected_axis()
            data = self.continuation.get_bifurcation_curve(xaxis, yaxis)

        xs, ys = data

        self.mainplot.update('main_curve', xs, ys, auto_lims=True)
        self.mainplot.update('main_marker', [xs[-1]], [ys[-1]])

    def draw_profile_plot(self, data=None):
        if data is None:
            data = self.continuation.get_profile_curve()
        
        logger.debug(f'Drawing profile plot')

        xs, ys = data

        self.secondaryplot.plot(xs, ys, name='profile', clear=True)

    def update_profile_plot(self, data=None):
        if data is None:
            data = self.continuation.get_profile_curve()

        xs, ys = data
        self.secondaryplot.update('profile', xs, ys)        

    def set_continuation_log(self, msg):
        self.log_label.setText(msg)

    def get_x_y_axis(self):
        pass

    def init_cont_params(self):
        cont_params = self.continuation.cont_params

        self.ds_entry.setText(str(cont_params['ds']))
        self.atol_entry.setText(str(cont_params['atol']))
        self.w_x_entry.setText(str(cont_params['w_x']))

    def get_current_cont_params(self):
        ds = float(self.ds_entry.text())
        atol = float(self.atol_entry.text())
        w_x = float(self.w_x_entry.text())
        direction = self.direction_combobox.currentText()

        cont_params = {'ds': ds, 'atol': atol, 'w_x': w_x, 
                       'direction': direction}

        return cont_params
    
    def kill_worker(self):
        self.runner.kill()

    def stop_continuating(self):
        self.is_continuating = False

    def play(self):
        if self.continuation is None:
            return
        
        if self.is_continuating:
            self.stop_continuating()
            self.kill_worker()
            return

        self.set_current_branchname()
        
        cont_params = self.get_current_cont_params()
        self.continuation.initialize_continuation(**cont_params)

        eqn = self.continuation.eqn
        n_x = eqn.n_x; dx, beta2, epsilon, Delta = eqn.get_params('dx beta2 epsilon Delta')
        logger.debug(f'Starting Continuation with following parameters:\n' \
                     +f'n_x = {n_x}, beta2 = {beta2},epsilon = {epsilon}, Delta = {Delta}\n'\
                     + f'dx = {dx}, w_x = {eqn.w_x}, ds = {eqn.ds}')

        self.is_continuating = True
        self.continuation_loop()

    def update_plot(self, Y, msg):
        self.update_profile_plot()
        self.update_main_plot()
        self.set_continuation_log(msg)

    def continuation_loop(self):
        self.threadpool = QThreadPool()

        self.runner = ContinuationWorker(self.continuation)
        self.runner.signals.result.connect(self.update_plot)
        self.runner.signals.finished.connect(self.stop_continuating)
        # self.runner.signals.error.connect(self.stop_continuating)

        self.threadpool.start(self.runner)
        

