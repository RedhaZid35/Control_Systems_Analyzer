

if __name__ == '__main__':
    # Num = [1]
    # Den = [1, 3, -20]
    system2 = MySystem([1], [-1, 1], TF_Feed=0.6)
    # instance= MySystem(Num, Den, TF_Feed = 1)
    # print(instance.is_stable_by_poles_method())
    # # instance.plot_impuls_response()
    # # instance.plot_step_response()
    # # instance.plot_bode_diagramme()
    # # instance.is_stable_by_poles_method(
    # # instance.plot_nyquist_diagramme()  
    # instance.plot_step_response()
    # S = step_info(instance.TF)
    # for k in S:
    #     print(f"{k}: {S[k]}")

    # # nichols(TransferFunction(Num, Den))
    # # # print(tf2ss(instance.TF))
    # # plt.show()
    sys = StateSpace([[-1., -1.],
                      [1., 0.]],
                      [[-1./np.sqrt(2.), 1./np.sqrt(2.)],
                      [0, 0]],
                      [[np.sqrt(2.), -np.sqrt(2.)]],
                      [[0, 0]])
    # # t,y = step_response(system2)
    # # plt.plot(t, y[0][1])
    # plt.xlabel('Time [s]')
    # plt.ylabel('Amplitude')
    # plt.title('Step response')
    # plt.grid()
    # plt.show()

    system2.plot_step_response()