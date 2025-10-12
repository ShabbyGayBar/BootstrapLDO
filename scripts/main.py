from plot import *

def main():
    clk_waveform(save_path="../figures")
    dummy(save_path="../figures")
    line_regulation(save_path="../figures")
    load_regulation(save_path="../figures")
    output_impedance("../figures")
    PSRR(save_path="../figures")
    tran_comp_waveform(save_path="../figures")
    tran_waveform(save_path="../figures")

if __name__ == "__main__":
    main()
