import pandas as pd
import matplotlib.pyplot as plt

def extract_labels(df):
    labels = set()
    for col in df.columns:
        if col.endswith(' X'):
            labels.add(col[:-2])
    return labels

def clk_waveform(save_path="../temp"):
    df = pd.read_csv("../assets/clk_waveform.csv", escapechar='\\')
    # print(df)

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    plt.plot(df['boot<0> X'], df['boot<0> Y'], label='boot[0]')
    plt.plot(df['charge<0> X'], df['charge<0> Y'], label='charge[0]')
    plt.legend()
    plt.grid(True, which='both')
    plt.xlim(0, 1.6e-7)
    plt.ylabel('Voltage (V)')

    plt.subplot(2, 1, 2)
    plt.plot(df['boot<1> X'], df['boot<1> Y'], label='boot[1]')
    plt.plot(df['charge<1> X'], df['charge<1> Y'], label='charge[1]')
    plt.legend()
    plt.grid(True, which='both')
    plt.xlim(0, 1.6e-7)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')

    plt.tight_layout()
    plt.savefig(f"{save_path}/clk_waveform.svg")
    # plt.show()
    plt.close()

def dummy(save_path="../temp"):
    df = pd.read_csv("../assets/dummy.csv", escapechar='\\', dtype=float, na_values=[' ', '  '])
    labels = ['No Dummy X', 'No Dummy Y', 'Dummy Fingers=2 X', 'Dummy Fingers=2 Y', 'Dummy Fingers=4 X', 'Dummy Fingers=4 Y', 'Dummy Fingers=8 X', 'Dummy Fingers=8 Y']
    df.columns = labels
    # print(df)

    plt.figure(figsize=(10, 6))
    plt.plot(df['Dummy Fingers=8 X'], df['Dummy Fingers=8 Y'], label='Dummy Fingers=8')
    plt.plot(df['Dummy Fingers=4 X'], df['Dummy Fingers=4 Y'], label='Dummy Fingers=4')
    plt.plot(df['Dummy Fingers=2 X'], df['Dummy Fingers=2 Y'], label='Dummy Fingers=2')
    plt.plot(df['No Dummy X'], df['No Dummy Y'], label='No Dummy')
    plt.legend()
    plt.grid(True, which='both')
    plt.xlim(2.53e-06, 2.62e-06)
    plt.ylim(0.99, 1)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.tight_layout()
    plt.savefig(f"{save_path}/dummy.svg")
    # plt.show()
    plt.close()

def line_regulation(save_path="../temp"):
    df = pd.read_csv("../assets/line_regulation.csv", escapechar='\\')
    df['iQ (iLoad=0.01) Y'] = 1e6 * df['iQ (iLoad=0.01) Y']  # Convert to uA for better readability
    df['iQ (iLoad=1e-07) Y'] = 1e6 * df['iQ (iLoad=1e-07) Y']
    # print(df)

    plt.figure(figsize=(10, 6))
    plt.plot(df['vOut (iLoad=1e-07) X'], df['vOut (iLoad=1e-07) Y'], label='iLoad=100nA')
    plt.plot(df['vOut (iLoad=0.01) X'], df['vOut (iLoad=0.01) Y'], label='iLoad=10mA')
    # Highlight the two ends of Output Voltage curve (iLoad=10mA)
    x = df['vOut (iLoad=0.01) X']
    y = df['vOut (iLoad=0.01) Y']
    plt.scatter([x.iloc[0], x.iloc[-1]], [y.iloc[0], y.iloc[-1]], color='orange', zorder=5)
    plt.hlines(y.iloc[0], xmin=x.iloc[0], xmax=x.iloc[-1], linestyles='dashed', colors=['orange'])
    plt.vlines(x.iloc[-1], ymin=y.iloc[0], ymax=y.iloc[-1], linestyles='dashed', colors=['orange'])
    # Calculate dx, dy, slope for iLoad=10mA
    dx = x.iloc[-1] - x.iloc[0]
    dy = y.iloc[-1] - y.iloc[0]
    slope2 = dy / dx if dx != 0 else float('inf')
    # Annotate values in a message bubble pointing to the vertical line
    plt.annotate(
        f"dx={dx:.1f}V\ndy={1000*dy:.2f}mV\nslope={1000*slope2:.3f}mV/V",
        xy=(x.iloc[-1], y.iloc[0]),
        xytext=(-20, 40),
        textcoords='offset points',
        ha='right',
        va='center',
        color='orange',
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="orange", lw=1),
        arrowprops=dict(arrowstyle="->", color='orange', lw=1)
    )
    # Highlight the two ends of Output Voltage curve (iLoad=100nA)
    x = df['vOut (iLoad=1e-07) X']
    y = df['vOut (iLoad=1e-07) Y']
    plt.scatter([x.iloc[0], x.iloc[-1]], [y.iloc[0], y.iloc[-1]], color='blue', zorder=5)
    plt.hlines(y.iloc[-1], xmin=x.iloc[0], xmax=x.iloc[-1], linestyles='dashed')
    plt.vlines(x.iloc[0], ymin=y.iloc[0], ymax=y.iloc[-1], linestyles='dashed')
    # Calculate dx, dy, slope
    dx = x.iloc[-1] - x.iloc[0]
    dy = y.iloc[-1] - y.iloc[0]
    slope = dy / dx if dx != 0 else float('inf')
    # Annotate values in a message bubble pointing to the vertical line
    plt.annotate(
        f"dx={dx:.1f}V\ndy={1000*dy:.2f}mV\nslope={1000*slope:.3f}mV/V",
        xy=(x.iloc[0], y.iloc[-1]),
        xytext=(120, -40),
        textcoords='offset points',
        ha='right',
        va='center',
        color='blue',
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="blue", lw=1),
        arrowprops=dict(arrowstyle="->", color='blue', lw=1)
    )
    plt.legend()
    plt.grid(True, which='both')
    plt.xlabel('Vdd (V)')
    plt.ylabel('Output Voltage (V)')
    plt.tight_layout()
    plt.savefig(f"{save_path}/line_regulation_vOut.svg")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(df['iQ (iLoad=1e-07) X'], df['iQ (iLoad=1e-07) Y'], label='iLoad=100nA')
    plt.plot(df['iQ (iLoad=0.01) X'], df['iQ (iLoad=0.01) Y'], label='iLoad=10mA')
    plt.legend()
    plt.grid(True, which='both')
    plt.xlabel('Vdd (V)')
    plt.ylabel('Quiescent Current (uA)')
    plt.tight_layout()
    plt.savefig(f"{save_path}/line_regulation_iQ.svg")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(df['vCtrl (iLoad=1e-07) X'], df['vCtrl (iLoad=1e-07) Y'], label='iLoad=100nA')
    plt.plot(df['vCtrl (iLoad=0.01) X'], df['vCtrl (iLoad=0.01) Y'], label='iLoad=10mA')
    plt.plot([0,2], [0,3], 'r--', label='1.5 Vdd')
    plt.plot([0,2], [0,2], 'k--', label='Vdd')
    plt.plot([0,2], [0,1], 'b--', label='0.5 Vdd')
    plt.legend()
    plt.grid(True, which='both')
    plt.xlim(1.1, 1.8)
    plt.ylim(0.8, 2)
    plt.xlabel('Vdd (V)')
    plt.ylabel('Gate Control Voltage (V)')
    plt.tight_layout()
    plt.savefig(f"{save_path}/line_regulation_vCtrl.svg")
    # plt.show()
    plt.close()

def load_regulation(save_path="../temp"):
    df = pd.read_csv("../assets/load_regulation.csv", escapechar='\\')
    df['iQ Y'] = 1e6 * df['iQ Y']
    # print(df)

    plt.figure(figsize=(10, 6))
    plt.plot(df['vOut_dc X'], df['vOut_dc Y'])
    # Highlight the two ends of Output Voltage curve
    x = df['vOut_dc X']
    y = df['vOut_dc Y']
    plt.scatter([x.iloc[0], x.iloc[-1]], [y.iloc[0], y.iloc[-1]], color='blue', zorder=5)
    plt.hlines(y.iloc[-1], xmin=x.iloc[0], xmax=x.iloc[-1], linestyles='dashed')
    plt.vlines(x.iloc[0], ymin=y.iloc[0], ymax=y.iloc[-1], linestyles='dashed')
    # Calculate dx, dy, slope
    dx = x.iloc[-1] - x.iloc[0]
    dy = y.iloc[-1] - y.iloc[0]
    slope = dy / dx if dx != 0 else float('inf')
    # Annotate values in a message bubble pointing to the vertical line
    plt.annotate(
        f"dx={1000*dx:.3f}mA\ndy={1000*dy:.2f}mV\nslope={slope:.3f}mV/mA",
        xy=(x.iloc[0], y.iloc[-1]),
        xytext=(120, 40),
        textcoords='offset points',
        ha='right',
        va='center',
        color='blue',
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="blue", lw=1),
        arrowprops=dict(arrowstyle="->", color='blue', lw=1)
    )
    plt.grid(True, which='both')
    plt.xscale('log')
    plt.xlabel('Load Current (A)')
    plt.ylabel('Output Voltage (V)')
    plt.tight_layout()
    plt.savefig(f"{save_path}/load_regulation_vOut.svg")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(df['iQ X'], df['iQ Y'])
    plt.grid(True, which='both')
    plt.xscale('log')
    plt.xlabel('Load Current (A)')
    plt.ylabel('Quiescent Current (uA)')
    plt.tight_layout()
    plt.savefig(f"{save_path}/load_regulation_iQ.svg")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(df['vCtrl X'], df['vCtrl Y'])
    plt.grid(True, which='both')
    plt.xscale('log')
    plt.xlabel('Load Current (A)')
    plt.ylabel('Gate Control Voltage (V)')
    plt.tight_layout()
    plt.savefig(f"{save_path}/load_regulation_vCtrl.svg")
    # plt.show()
    plt.close()

def output_impedance(save_path="../temp"):
    df = pd.read_csv("../assets/output_impedance.csv", escapechar='\\')
    # print(df)

    labels = extract_labels(df)
    # Calculate magnitude from real and imaginary parts
    for label in labels:
        y_re_col = f"{label} YRe"
        y_im_col = f"{label} YReImag"
        y_col = f"{label} Y"
        df[y_col] = (df[y_re_col]**2 + df[y_im_col]**2)**0.5

    color = 'blue'
    plt.figure(figsize=(10, 6))
    for label in labels:
        plt.plot(df[f'{label} X'], df[f'{label} Y'], label=label, color=color)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Z (Ohm)")
    plt.xlim(1, 1e10)
    plt.xscale('log')
    plt.yscale('log')
    plt.grid()
    plt.savefig(f"{save_path}/output_impedance.svg")
    # plt.show()
    plt.close()

def PSRR(save_path="../temp/PSRR"):
    df = pd.read_csv("../assets/PSRR.csv", escapechar='\\')
    # print(df)

    # Find max value in columns ending with ' Y'
    peak_PSRR = df[df.columns[df.columns.str.endswith(' Y')]].max().max()
    # print(f"Max value in dataframe: {peak_PSRR}")
    # Find max value in row 1
    max_DC_PSRR = df.iloc[0][df.columns[df.columns.str.endswith(' Y')]].max()
    # print(f"Max DC PSRR: {max_DC_PSRR} dB")
    f_trans = 3e6

    labels = extract_labels(df)

    color = 'blue'
    plt.figure(figsize=(10, 6))
    for label in labels:
        plt.plot(df[f'{label} X'], df[f'{label} Y'], label=label, color=color)
    plt.hlines(y=peak_PSRR, xmin=1, xmax=1e10, linestyles='dashed', label='Max Value')
    plt.vlines(x=f_trans, ymin=-100, ymax=0, linestyles='dashed', label='Transition Frequency')
    plt.annotate(f'Worst Case PSRR: {peak_PSRR:.1f} dB', xy=(1, peak_PSRR+1), color=color)
    plt.annotate(f'Transition Frequency: {f_trans/1e6:.1f} MHz', xy=(f_trans, -12), color=color)
    plt.annotate(f'Worst Case DC PSRR: {max_DC_PSRR:.1f} dB', xy=(1, max_DC_PSRR+1), color=color)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("PSRR (dB)")
    plt.xlim(1, 1e10)
    plt.ylim(-60, -10)
    plt.xscale('log')
    plt.grid()
    plt.savefig(f"{save_path}/PSRR.svg")
    # plt.show()
    plt.close()

def tran_comp_waveform(save_path="../temp"):
    df = pd.read_csv("../assets/tran_comp_waveform.csv", escapechar='\\')
    labels = ['iLoad X', 'iLoad Y', 'iOut X', 'iOut Y', 'vOut X', 'vOut Y']
    df.columns = labels
    df['iOut Y'] = - df['iOut Y'] * 1e3  # Convert to mA
    df['iLoad Y'] = df['iLoad Y'] * 1e3
    # print(df)

    fig, ax1 = plt.subplots()
    fig.set_size_inches(10, 6)

    color='blue'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Voltage (V)', color=color)
    ax1.plot(df['vOut X'], df['vOut Y'], label='Output Voltage', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis

    color='red'
    ax2.set_ylabel('Current (mA)', color=color)  # we already handled the x-label with ax1
    # plt.plot(df['iOut X'], df['iOut Y'], label='Output Current', color='green')
    plt.plot(df['iLoad X'], df['iLoad Y'], label='Load Current', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    legend = fig.legend()
    ax1.grid(True, which='both', axis='x')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    # Zoom in Undershoot
    t = [2e-6, 2e-6+68.21e-12]
    v = [0.9990976356428115, 1-275.8e-3]

    color='blue'
    ax1.scatter(t, v, color=color)
    ax1.hlines(v[0], xmin=t[0], xmax=t[1], linestyles='dashed')
    ax1.vlines(t[1], ymin=v[0], ymax=v[1], linestyles='dashed')
    # Calculate dt, dv, slope
    dt = t[1] - t[0]
    dv = v[1] - v[0]
    # Annotate values in a message bubble pointing to the vertical line
    ax1.annotate(
        f"Response Time={1e12*dt:.2f}ps\nUndershoot={-1000*dv:.2f}mV",
        xy=(t[1], v[0]),
        xytext=(120, -30),
        textcoords='offset points',
        ha='right',
        va='center',
        color='blue',
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="blue", lw=1),
        arrowprops=dict(arrowstyle="->", color='blue', lw=1)
    )

    ax1.set_xlim(1.99999e-6, 2.0002e-6)
    ax1.set_ylim(0.7, 1.03)
    fig.savefig(f"{save_path}/tran_comp_waveform_undershoot_zoom.svg")

    # Undershoot
    ax1.set_xlim(1.99e-6, 2.05e-6)
    ax1.set_ylim(0.6, 1.3)
    ax2.yaxis.set_visible(False)

    ax1.hlines(v[0], xmin=t[0], xmax=3e-6, linestyles='dashed')
    fig.savefig(f"{save_path}/tran_comp_waveform_undershoot.svg")

    # Overshoot
    t = 4.000364423193259e-06
    v = 1.190561618887162

    ax1.scatter([t], [v], color=color)
    ax1.hlines(0.9974847177765783, xmin=4e-6, xmax=5e-6, linestyles='dashed')
    ax1.vlines(t, ymin=1, ymax=v, linestyles='dashed')
    # Annotate values in a message bubble pointing to the overshoot point
    ax1.annotate(
        f"Overshoot={1000*(v-1):.1f}mV",
        xy=(t, v),
        xytext=(150, -20),
        textcoords='offset points',
        ha='right',
        va='center',
        color='blue',
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="blue", lw=1),
        arrowprops=dict(arrowstyle="->", color='blue', lw=1)
    )

    ax1.set_xlim(3.99e-6, 4.05e-6)
    # ax1.set_ylim(0.97, 1.23)
    ax1.yaxis.set_visible(False)
    ax2.yaxis.set_visible(True)
    legend.remove()
    fig.savefig(f"{save_path}/tran_comp_waveform_overshoot.svg")

    # plt.show()
    plt.close()

def tran_waveform(save_path="../temp"):
    df = pd.read_csv("../assets/tran_waveform.csv", escapechar='\\')
    labels = ['iLoad X', 'iLoad Y', 'iOut X', 'iOut Y', 'vOut X', 'vOut Y']
    df.columns = labels
    df['iOut Y'] = - df['iOut Y'] * 1e3  # Convert to mA
    df['iLoad Y'] = df['iLoad Y'] * 1e3
    # print(df)

    fig, ax1 = plt.subplots()
    fig.set_size_inches(10, 6)

    color='blue'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Voltage (V)', color=color)
    ax1.plot(df['vOut X'], df['vOut Y'], label='Output Voltage', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis

    color='red'
    ax2.set_ylabel('Current (mA)', color=color)  # we already handled the x-label with ax1
    # plt.plot(df['iOut X'], df['iOut Y'], label='Output Current', color='green')
    plt.plot(df['iLoad X'], df['iLoad Y'], label='Load Current', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    legend = fig.legend()
    ax1.grid(True, which='both', axis='x')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    # Zoom in Undershoot
    t = [2e-6, 2e-6+18.51e-12]
    v = [1.000765703871354, 1-663.4e-3]

    color='blue'
    ax1.scatter(t, v, color=color)
    ax1.hlines(v[0], xmin=t[0], xmax=t[1], linestyles='dashed')
    ax1.vlines(t[1], ymin=v[0], ymax=v[1], linestyles='dashed')
    # Calculate dt, dv, slope
    dt = t[1] - t[0]
    dv = v[1] - v[0]
    # Annotate values in a message bubble pointing to the vertical line
    ax1.annotate(
        f"Response Time={1e12*dt:.2f}ps\nUndershoot={-1000*dv:.2f}mV",
        xy=(t[1], v[0]),
        xytext=(120, -30),
        textcoords='offset points',
        ha='right',
        va='center',
        color='blue',
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="blue", lw=1),
        arrowprops=dict(arrowstyle="->", color='blue', lw=1)
    )

    ax1.set_xlim(1.99999e-6, 2.00005e-6)
    ax1.set_ylim(0.3, 1.03)
    fig.savefig(f"{save_path}/tran_waveform_undershoot_zoom.svg")

    # Undershoot
    ax1.set_xlim(1.99e-6, 2.05e-6)
    ax1.set_ylim(0.25, 1.3)
    ax2.yaxis.set_visible(False)

    ax1.hlines(v[0], xmin=t[0], xmax=3e-6, linestyles='dashed')
    fig.savefig(f"{save_path}/tran_waveform_undershoot.svg")

    # Overshoot
    t = 4.000364423193259e-06
    v = 1.190561618887162

    ax1.scatter([t], [v], color=color)
    ax1.hlines(0.9974847177765783, xmin=4e-6, xmax=5e-6, linestyles='dashed')
    ax1.vlines(t, ymin=1, ymax=v, linestyles='dashed')
    # Annotate values in a message bubble pointing to the overshoot point
    ax1.annotate(
        f"Overshoot={1000*(v-1):.1f}mV",
        xy=(t, v),
        xytext=(150, -20),
        textcoords='offset points',
        ha='right',
        va='center',
        color='blue',
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="blue", lw=1),
        arrowprops=dict(arrowstyle="->", color='blue', lw=1)
    )

    ax1.set_xlim(3.99e-6, 4.05e-6)
    # ax1.set_ylim(0.97, 1.23)
    ax1.yaxis.set_visible(False)
    ax2.yaxis.set_visible(True)
    legend.remove()
    fig.savefig(f"{save_path}/tran_waveform_overshoot.svg")

    # plt.show()
    plt.close()
