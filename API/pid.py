from control import (tf, feedback, ss, tf2ss, tf2io, ss2tf, ss2io, _convert_to_statespace, common_timebase, isctime, interconnect, StateSpace, summing_junction)

def my_pid_designer(plant , sign=-1, input_signal='r',
                           Kp0=0, Ki0=0, Kd0=0, tau=0.01,
                           C_ff=0, derivative_in_feedback_path=False,
                           plot=False):
    """Manual PID controller design based on root locus using Sisotool

    Uses `Sisotool` to investigate the effect of adding or subtracting an
    amount `deltaK` to the proportional, integral, or derivative (PID) gains of
    a controller. One of the PID gains, `Kp`, `Ki`, or `Kd`, respectively, can
    be modified at a time. `Sisotool` plots the step response, frequency
    response, and root locus.

    When first run, `deltaK` is set to 0; click on a branch of the root locus
    plot to try a different value. Each click updates plots and prints
    the corresponding `deltaK`. To tune all three PID gains, repeatedly call
    `rootlocus_pid_designer`, and select a different `gain` each time (`'P'`,
    `'I'`, or `'D'`). Make sure to add the resulting `deltaK` to your chosen
    initial gain on the next iteration.

    Example: to examine the effect of varying `Kp` starting from an intial
    value of 10, use the arguments `gain='P', Kp0=10`. Suppose a `deltaK`
    value of 5 gives satisfactory performance. Then on the next iteration,
    to tune the derivative gain, use the arguments `gain='D', Kp0=15`.

    By default, all three PID terms are in the forward path C_f in the diagram
    shown below, that is,

    C_f = Kp + Ki/s + Kd*s/(tau*s + 1).

    ::

          ------> C_ff ------    d
          |                 |    |
      r   |     e           V    V  u         y
      ------->O---> C_f --->O--->O---> plant --->
              ^-            ^-                |
              |             |                 |
              |             ----- C_b <-------|
              ---------------------------------

    If `plant` is a discrete-time system, then the proportional, integral, and
    derivative terms are given instead by Kp, Ki*dt/2*(z+1)/(z-1), and
    Kd/dt*(z-1)/z, respectively.

    It is also possible to move the derivative term into the feedback path
    `C_b` using `derivative_in_feedback_path=True`. This may be desired to
    avoid that the plant is subject to an impulse function when the reference
    `r` is a step input. `C_b` is otherwise set to zero.

    If `plant` is a 2-input system, the disturbance `d` is fed directly into
    its second input rather than being added to `u`.

    Remark: It may be helpful to zoom in using the magnifying glass on the
    plot. Just ake sure to deactivate magnification mode when you are done by
    clicking the magnifying glass. Otherwise you will not be able to be able
    to choose a gain on the root locus plot.

    Parameters
    ----------
    plant : :class:`LTI` (:class:`TransferFunction` or :class:`StateSpace` system)
        The dynamical system to be controlled
    gain : string (optional)
        Which gain to vary by `deltaK`. Must be one of `'P'`, `'I'`, or `'D'`
        (proportional, integral, or derative)
    sign : int (optional)
        The sign of deltaK gain perturbation
    input : string (optional)
        The input used for the step response; must be `'r'` (reference) or
        `'d'` (disturbance) (see figure above)
    Kp0, Ki0, Kd0 : float (optional)
        Initial values for proportional, integral, and derivative gains,
        respectively
    tau : float (optional)
        The time constant associated with the pole in the continuous-time
        derivative term. This is required to make the derivative transfer
        function proper.
    C_ff : float or :class:`LTI` system (optional)
        Feedforward controller. If :class:`LTI`, must have timebase that is
        compatible with plant.
    derivative_in_feedback_path : bool (optional)
        Whether to place the derivative term in feedback transfer function
        `C_b` instead of the forward transfer function `C_f`.
    plot : bool (optional)
        Whether to create Sisotool interactive plot.

    Returns
    -------
    closedloop : class:`StateSpace` system
        The closed-loop system using initial gains.

    """

    plant = _convert_to_statespace(plant)
    if plant.ninputs == 1:
        plant = ss2io(plant, inputs='u', outputs='y')
    elif plant.ninputs == 2:
        plant = ss2io(plant, inputs=['u', 'd'], outputs='y')
    else:
        raise ValueError("plant must have one or two inputs")
    C_ff = ss2io(_convert_to_statespace(C_ff),   inputs='r', outputs='uff')
    dt = common_timebase(plant, C_ff)

    # create systems used for interconnections
    e_summer = summing_junction(['r', '-y'], 'e')
    # if plant.ninputs == 2:
    #     u_summer = summing_junction(['ufb', 'uff'], 'u')
    # else:
    u_summer = summing_junction(['ufb', 'd'], 'u')

    if isctime(plant):
        prop  = tf(1, 1)
        integ = tf(1, [1, 0])
        deriv = tf([1, 0], [tau, 1])
    else: # discrete-time
        prop  = tf(1, 1, dt)
        integ = tf([dt/2, dt/2], [1, -1], dt)
        deriv = tf([1, -1], [dt, 0], dt)

    # add signal names by turning into iosystems
    prop  = tf2io(prop,        inputs='e', outputs='prop_e')
    integ = tf2io(integ,       inputs='e', outputs='int_e')
    if derivative_in_feedback_path:
        deriv = tf2io(-deriv,  inputs='y', outputs='deriv')
    else:
        deriv = tf2io(deriv,   inputs='e', outputs='deriv')

    # create gain blocks
    Kpgain = tf2io(tf(Kp0, 1),inputs='prop_e',  outputs='ufb')
    Kigain = tf2io(tf(Ki0, 1),inputs='int_e',   outputs='ufb')
    Kdgain = tf2io(tf(Kd0, 1),inputs='deriv',  outputs='ufb')

    # the second input and output are used by sisotool to plot step response
    loop = interconnect((plant, Kpgain, Kigain, Kdgain, prop, integ, deriv, e_summer, u_summer),
                            inplist=['r'],
                            outlist=['y'], check_unused=False)
    cl = loop[0,0] # closed loop transfer function with initial gains
    # print(cl.ninputs)
    sys = ss2tf(StateSpace(cl.A, cl.B, cl.C, cl.D, cl.dt))
    return sys
