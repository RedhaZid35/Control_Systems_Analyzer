
import warnings

import numpy as np
import scipy as sp
from numpy import einsum, maximum, minimum
from scipy.linalg import eig, eigvals, matrix_balance, norm
from copy import copy
from control.timeresp import _default_time_vector, _get_ss_simo, forced_response, TimeResponseData
from control import config
from control.exception import pandas_check
from control.namedio import isctime, isdtime
from control.statesp import StateSpace, _convert_to_statespace, _mimo2simo, _mimo2siso
from control.xferfcn import TransferFunction
import matplotlib.pyplot as plt


def ramp_response(sys,U, T=None, X0=0., input=None, output=None, T_num=None,
                  transpose=False, return_x=False, squeeze=None):
    # pylint: disable=W0622
    """Compute the ramp response for a linear system, for any given input.

    If the system has multiple inputs and/or multiple outputs, the ramp
    response is computed for each input/output pair, with all other inputs set
    to zero.  Optionally, a single input and/or single output can be selected,
    in which case all other inputs are set to 0 and all other outputs are
    ignored.

    For information on the **shape** of parameters `T`, `X0` and
    return values `T`, `yout`, see :ref:`time-series-convention`.

    Parameters
    ----------
    sys : StateSpace or TransferFunction
        LTI system to simulate

    T : array_like or float, optional
        Time vector, or simulation time duration if a number. If T is not
        provided, an attempt is made to create it automatically from the
        dynamics of sys. If sys is continuous-time, the time increment dt
        is chosen small enough to show the fastest mode, and the simulation
        time period tfinal long enough to show the slowest mode, excluding
        poles at the origin and pole-zero cancellations. If this results in
        too many time steps (>5000), dt is reduced. If sys is discrete-time,
        only tfinal is computed, and final is reduced if it requires too
        many simulation steps.

    X0 : array_like or float, optional
        Initial condition (default = 0). Numbers are converted to constant
        arrays with the correct shape.

    input : int, optional
        Only compute the ramp response for the listed input.  If not
        specified, the ramp responses for each independent input are
        computed (as separate traces).

    output : int, optional
        Only report the ramp response for the listed output.  If not
        specified, all outputs are reported.

    T_num : int, optional
        Number of time steps to use in simulation if T is not provided as an
        array (autocomputed if not given); ignored if sys is discrete-time.

    transpose : bool, optional
        If True, transpose all input and output arrays (for backward
        compatibility with MATLAB and :func:`scipy.signal.lsim`).  Default
        value is False.

    return_x : bool, optional
        If True, return the state vector when assigning to a tuple (default =
        False).  See :func:`forced_response` for more details.

    squeeze : bool, optional
        By default, if a system is single-input, single-output (SISO) then the
        output response is returned as a 1D array (indexed by time).  If
        squeeze=True, remove single-dimensional entries from the shape of the
        output even if the system is not SISO. If squeeze=False, keep the
        output as a 3D array (indexed by the output, input, and time) even if
        the system is SISO. The default value can be set using
        config.defaults['control.squeeze_time_response'].

    Returns
    -------
    results : TimeResponseData
        Time response represented as a :class:`TimeResponseData` object
        containing the following properties:

        * time (array): Time values of the output.

        * outputs (array): Response of the system.  If the system is SISO and
          squeeze is not True, the array is 1D (indexed by time).  If the
          system is not SISO or ``squeeze`` is False, the array is 3D (indexed
          by the output, trace, and time).

        * states (array): Time evolution of the state vector, represented as
          either a 2D array indexed by state and time (if SISO) or a 3D array
          indexed by state, trace, and time.  Not affected by ``squeeze``.

        * inputs (array): Input(s) to the system, indexed in the same manner
          as ``outputs``.

        The return value of the system can also be accessed by assigning the
        function to a tuple of length 2 (time, output) or of length 3 (time,
        output, state) if ``return_x`` is ``True``.

    See Also
    --------
    forced_response, initial_response, impulse_response

    Notes
    -----
    This function uses the `forced_response` function with the input set to a
    unit ramp.

    Examples
    --------
    >>> T, yout = step_response(sys, T, X0)

    """
    # Create the time vector
    if T is None or np.asarray(T).size == 1:
        T = _default_time_vector(sys, N=T_num, tfinal=T, is_step=True)

    # If we are passed a transfer function and X0 is non-zero, warn the user
    if isinstance(sys, TransferFunction) and np.any(X0 != 0):
        warnings.warn(
            "Non-zero initial condition given for transfer function system. "
            "Internal conversion to state space used; may not be consistent "
            "with given X0.")

    # Convert to state space so that we can simulate
    sys = _convert_to_statespace(sys)

    # Set up arrays to handle the output
    ninputs = sys.ninputs if input is None else 1
    noutputs = sys.noutputs if output is None else 1
    yout = np.empty((noutputs, ninputs, np.asarray(T).size))
    xout = np.empty((sys.nstates, ninputs, np.asarray(T).size))
    uout = np.empty((ninputs, ninputs, np.asarray(T).size))

    # Simulate the response for each input
    for i in range(sys.ninputs):
        # If input keyword was specified, only simulate for that input
        if isinstance(input, int) and i != input:
            continue

        # Create a set of single inputs system for simulation
        squeeze, simo = _get_ss_simo(sys, i, output, squeeze=squeeze)

        response = forced_response(simo, T, U, X0, squeeze=True)
        inpidx = i if input is None else 0
        yout[:, inpidx, :] = response.y
        xout[:, inpidx, :] = response.x
        uout[:, inpidx, :] = U

    # Figure out if the system is SISO or not
    issiso = sys.issiso() or (input is not None and output is not None)

    return response


def ramp_info(sysdata, T=None, T_num=None, yfinal=None,
              SettlingTimeThreshold=0.02, RiseTimeLimits=(0.1, 0.9)):
    """
    Step response characteristics (Rise time, Settling Time, Peak and others).

    Parameters
    ----------
    sysdata : StateSpace or TransferFunction or array_like
        The system data. Either LTI system to similate (StateSpace,
        TransferFunction), or a time series of step response data.
    T : array_like or float, optional
        Time vector, or simulation time duration if a number (time vector is
        autocomputed if not given, see :func:`step_response` for more detail).
        Required, if sysdata is a time series of response data.
    T_num : int, optional
        Number of time steps to use in simulation if T is not provided as an
        array; autocomputed if not given; ignored if sysdata is a
        discrete-time system or a time series or response data.
    yfinal : scalar or array_like, optional
        Steady-state response. If not given, sysdata.dcgain() is used for
        systems to simulate and the last value of the the response data is
        used for a given time series of response data. Scalar for SISO,
        (noutputs, ninputs) array_like for MIMO systems.
    SettlingTimeThreshold : float, optional
        Defines the error to compute settling time (default = 0.02)
    RiseTimeLimits : tuple (lower_threshold, upper_theshold)
        Defines the lower and upper threshold for RiseTime computation

    Returns
    -------
    S : dict or list of list of dict
        If `sysdata` corresponds to a SISO system, S is a dictionary
        containing:

        RiseTime:
            Time from 10% to 90% of the steady-state value.
        SettlingTime:
            Time to enter inside a default error of 2%
        SettlingMin:
            Minimum value after RiseTime
        SettlingMax:
            Maximum value after RiseTime
        Overshoot:
            Percentage of the Peak relative to steady value
        Undershoot:
            Percentage of undershoot
        Peak:
            Absolute peak value
        PeakTime:
            time of the Peak
        SteadyStateValue:
            Steady-state value

        If `sysdata` corresponds to a MIMO system, `S` is a 2D list of dicts.
        To get the step response characteristics from the j-th input to the
        i-th output, access ``S[i][j]``


    See Also
    --------
    step, lsim, initial, impulse

    Examples
    --------
    >>> from control import step_info, TransferFunction
    >>> sys = TransferFunction([-1, 1], [1, 1, 1])
    >>> S = step_info(sys)
    >>> for k in S:
    ...     print(f"{k}: {S[k]:3.4}")
    ...
    RiseTime: 1.256
    SettlingTime: 9.071
    SettlingMin: 0.9011
    SettlingMax: 1.208
    Overshoot: 20.85
    Undershoot: 27.88
    Peak: 1.208
    PeakTime: 4.187
    SteadyStateValue: 1.0

    MIMO System: Simulate until a final time of 10. Get the step response
    characteristics for the second input and specify a 5% error until the
    signal is considered settled.

    >>> from numpy import sqrt
    >>> from control import step_info, StateSpace
    >>> sys = StateSpace([[-1., -1.],
    ...                   [1., 0.]],
    ...                  [[-1./sqrt(2.), 1./sqrt(2.)],
    ...                   [0, 0]],
    ...                  [[sqrt(2.), -sqrt(2.)]],
    ...                  [[0, 0]])
    >>> S = step_info(sys, T=10., SettlingTimeThreshold=0.05)
    >>> for k, v in S[0][1].items():
    ...     print(f"{k}: {float(v):3.4}")
    RiseTime: 1.212
    SettlingTime: 6.061
    SettlingMin: -1.209
    SettlingMax: -0.9184
    Overshoot: 20.87
    Undershoot: 28.02
    Peak: 1.209
    PeakTime: 4.242
    SteadyStateValue: -1.0
    """
    if isinstance(sysdata, (StateSpace, TransferFunction)):
        if T is None or np.asarray(T).size == 1:
            T = _default_time_vector(sysdata, N=T_num, tfinal=T, is_step=True)
        T, Yout = step_response(sysdata, T, squeeze=False)
        if yfinal:
            InfValues = np.atleast_2d(yfinal)
        else:
            InfValues = np.atleast_2d(sysdata.dcgain())
        retsiso = sysdata.issiso()
        noutputs = sysdata.noutputs
        ninputs = sysdata.ninputs
    else:
        # Time series of response data
        errmsg = ("`sys` must be a LTI system, or time response data"
                  " with a shape following the python-control"
                  " time series data convention.")
        try:
            Yout = np.array(sysdata, dtype=float)
        except ValueError:
            raise ValueError(errmsg)
        if Yout.ndim == 1 or (Yout.ndim == 2 and Yout.shape[0] == 1):
            Yout = Yout[np.newaxis, np.newaxis, :]
            retsiso = True
        elif Yout.ndim == 3:
            retsiso = False
        else:
            raise ValueError(errmsg)
        if T is None or Yout.shape[2] != len(np.squeeze(T)):
            raise ValueError("For time response data, a matching time vector"
                             " must be given")
        T = np.squeeze(T)
        noutputs = Yout.shape[0]
        ninputs = Yout.shape[1]
        InfValues = np.atleast_2d(yfinal) if yfinal else Yout[:, :, -1]

    ret = []
    for i in range(noutputs):
        retrow = []
        for j in range(ninputs):
            yout = Yout[i, j, :]

            # Steady state value
            InfValue = InfValues[i, j]
            sgnInf = np.sign(InfValue.real)

            rise_time: float = np.NaN
            settling_time: float = np.NaN
            settling_min: float = np.NaN
            settling_max: float = np.NaN
            peak_value: float = np.Inf
            peak_time: float = np.Inf
            undershoot: float = np.NaN
            overshoot: float = np.NaN
            steady_state_value: complex = np.NaN

            if not np.isnan(InfValue) and not np.isinf(InfValue):
                # RiseTime
                tr_lower_index = np.where(
                    sgnInf * (yout - RiseTimeLimits[0] * InfValue) >= 0
                    )[0][0]
                tr_upper_index = np.where(
                    sgnInf * (yout - RiseTimeLimits[1] * InfValue) >= 0
                    )[0][0]
                rise_time = T[tr_upper_index] - T[tr_lower_index]

                # SettlingTime
                settled = np.where(
                    np.abs(yout/InfValue-1) >= SettlingTimeThreshold)[0][-1]+1
                # MIMO systems can have unsettled channels without infinite
                # InfValue
                if settled < len(T):
                    settling_time = T[settled]

                settling_min = min((yout[tr_upper_index:]).min(), InfValue)
                settling_max = max((yout[tr_upper_index:]).max(), InfValue)

                # Overshoot
                y_os = (sgnInf * yout).max()
                dy_os = np.abs(y_os) - np.abs(InfValue)
                if dy_os > 0:
                    overshoot = np.abs(100. * dy_os / InfValue)
                else:
                    overshoot = 0

                # Undershoot : InfValue and undershoot must have opposite sign
                y_us_index = (sgnInf * yout).argmin()
                y_us = yout[y_us_index]
                if (sgnInf * y_us) < 0:
                    undershoot = (-100. * y_us / InfValue)
                else:
                    undershoot = 0

                # Peak
                peak_index = np.abs(yout).argmax()
                peak_value = np.abs(yout[peak_index])
                peak_time = T[peak_index]

                # SteadyStateValue
                steady_state_value = InfValue

            retij = {
                'RiseTime': rise_time,
                'SettlingTime': settling_time,
                'SettlingMin': settling_min,
                'SettlingMax': settling_max,
                'Overshoot': overshoot,
                'Undershoot': undershoot,
                'Peak': peak_value,
                'PeakTime': peak_time,
                'SteadyStateValue': steady_state_value
                }
            retrow.append(retij)

        ret.append(retrow)
    

    return ret[0][0] if retsiso else ret


# sys = TransferFunction([1], [1, 2])
# tu = np.linspace(1, 10, 100)
# U = np.linspace(0, 10, len(tu))
# t, y = ramp_response(sys,U)
# plt.plot(t,y)
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitude')
# plt.title('Step response')
# plt.grid()
# plt.show()