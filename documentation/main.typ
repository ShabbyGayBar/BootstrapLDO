#import "@preview/charged-ieee:0.1.4": ieee
#import "@preview/unify:0.7.1": *
#import "@preview/wordometer:0.1.5": total-words, word-count

#show: ieee.with(
  title: [A Bootstrapped NMOS LDO Regulator for Low Supply Voltage and High PSRR],
  abstract: [
    This work presents a bootstrapped NMOS low-dropout (LDO) regulator designed to operate effectively under low supply voltage conditions while maintaining high performance in terms of line regulation, load regulation, transient response, and power supply rejection ratio (PSRR). The proposed design leverages a bootstrap circuit to elevate the gate voltage of the NMOS pass transistor, enabling it to function efficiently even when the supply voltage is limited. Simulation results demonstrate that the bootstrapped NMOS LDO achieves a line regulation of 10.248 mV/V, a load regulation of 0.534 mV/mA, and a transient response figure of merit (FoM) as low as 25.65 fs under large load steps. Additionally, the design exhibits robust PSRR performance, making it suitable for applications requiring stable power delivery in low-voltage environments.
  ],
  authors: (
    (
      name: "Brian Li",
      // department: [IME],
      organization: [University of Macau],
      location: [Macau, China],
      email: "brian.li@connect.um.edu.mo",
    ),
  ),
  index-terms: ("Bootstrap switch", "Low-dropout regulator", "LDO", "Power management"),
  bibliography: bibliography("refs.bib"),
  figure-supplement: [Fig.],
)

#show: word-count // Start word counting

#set figure(placement: top)

= Introduction

Low-dropout (LDO) regulators are widely used in modern electronic systems to provide stable and efficient power supply to various components. They are particularly favored for their simplicity, low noise, and fast transient response.

Among different types of LDOs, NMOS-based LDOs offer several advantages, including higher current handling capability and better thermal performance compared to their PMOS counterparts. However, they typically require a higher supply voltage to operate effectively, which can be a limitation in low-voltage applications.

NMOS LDOs face challenges in low supply voltage scenarios due to their threshold voltage requirements. As the supply voltage decreases, the headroom for the NMOS pass transistor becomes limited, leading to potential dropout issues and reduced output voltage accuracy.

To address these challenges, this work proposes a bootstrapped NMOS LDO. By utilizing a bootstrap capacitor and switch, the gate voltage of the NMOS transistor can be elevated above the supply voltage, allowing for improved performance in low-voltage applications without the need for a higher supply voltage.

= Proposed Bootstrapped NMOS LDO

#figure(
  image("../figures/schematic_conventional.svg", height: 4cm),
  caption: [Conventional NMOS LDO architecture],
) <schematic_conventional>

A conventional NMOS LDO architecture is illustrated in @schematic_conventional, where the NMOS pass transistor regulates the output voltage based on the feedback from the output node. The gate of the NMOS transistor is driven by an error amplifier that compares the output voltage with a reference voltage.

A major limitation of this architecture is its need for a higher gate voltage to ensure proper NMOS transistor operation. This is often challenging in low supply voltage scenarios.

Multiple techniques have been proposed to overcome this limitation, such as using charge pumps@charge_pump_LDO_2022 or using a higher separate voltage supply. However, these approaches can introduce additional complexity, power consumption, and noise into the system.

#figure(
  image("../figures/schematic_proposed.svg", height: 4cm),
  caption: [A conceptual model of the proposed bootstrapped NMOS LDO],
) <schematic_proposed>

The proposed bootstrapped NMOS LDO architecture, shown in @schematic_proposed, addresses these challenges by incorporating a bootstrap capacitor between the output of the error amplifier and the gate of the NMOS pass device.

The bootstrap circuit, highlighted in purple in @schematic_proposed, consists of a capacitor and 4 switches driven by non-overlapping clock signals `boot` and `charge`, whose waveform is shown in @clk_waveform.

#figure(
  image("../figures/clk_waveform.svg"),
  caption: [Non-overlapping clock waveform for bootstrap circuit],
) <clk_waveform>

During the `boot` phase, the capacitor is placed between the output of the error amplifier and the gate of the NMOS transistor.

During the `charge` phase of the clock, the capacitor is charged to the output voltage. To avoid the gate being left floating during the `charge` phase, another bootstrap circuit with complementary clock phases, highlighted in dark purple in @schematic_proposed, is used to maintain the error amplifier's control on the gate voltage.

The bootstrap circuit elevates the gate voltage of the NMOS transistor above the supply voltage during operation, allowing for improved regulation performance even at low supply voltages. This approach maintains the simplicity of the LDO design while enhancing its capability to operate effectively in low-voltage environments.

= Circuit Implementation

== Bootstrap Circuit

Unfortunately, adding a $V_"dd"$ to the output of the error amplifier to drive the gate of the NMOS pass transistor exceeds the proper operating voltage of the NMOS pass device when $V_"dd"$ varies.

#figure(
  image("../figures/line_regulation_vCtrl.svg"),
  caption: [Simulated proper NMOS gate control voltage range under varying $V_"dd"$],
) <line_regulation_vCtrl>

As shown in @line_regulation_vCtrl, the NMOS gate control voltage stays within $[0.5 V_"dd", 1.5 V_"dd"]$, which means that the bootstrap circuit needs to provide a voltage boost of precisely $0.5 V_"dd"$ to ensure proper operation across the entire $V_"dd"$ range.

#figure(
  grid(
    columns: 2,
    image("../figures/schematic_bootstrap_boot.svg", height: 4cm),
    image("../figures/schematic_bootstrap_charge.svg", height: 4cm),
  ),
  caption: [Bootstrap circuit schematic. left: `boot` phase; right: `charge` phase],
) <schematic_bootstrap>

In order to achieve this, a bootstrap circuit as shown in @schematic_bootstrap is designed. During the `charge` phase, two identical capacitors share the $V_"dd"$ voltage, charging each capacitor to approximately $0.5 V_"dd"$. During the `boot` phase, the capacitors are put in parallel, exhibiting the $0.5 V_"dd"$ voltage boost required.

Another important consideration in the bootstrap circuit design is the clock feedthrough and charge injection effect from the switches directly connected to the gate of the NMOS pass transistor. This effect can introduce unwanted voltage spikes on the gate, potentially disrupting the regulation performance. To mitigate this, dummy switches controlled by the complementary clock signals are added in parallel with the main switches.

#figure(
  image("../figures/dummy.svg"),
  caption: [Gate control voltage waveform under different dummy compensation],
) <dummy>

The effectiveness of the dummy switches in reducing voltage spikes is demonstrated in @dummy, where the gate control voltage spikes where reduced from dozens of millivolts to around 10 millivolts.

#figure(
  image("../figures/bootstrap.png"),
  caption: [Complete schematic of the bootstrap circuit, including dummy switches for charge injection mitigation],
) <bootstrap>

The schematic of the complete bootstrap circuit with dummy switches is shown in @bootstrap.

== Error Amplifier

The DC voltage gain from the supply voltage $V_"dd"$ to the output voltage $V_"out"$ can be expressed as:
$
  A_"line"
  = 1 / (1/Z_"L" + 1 + g_"m" r_"o" + A dot g_"m" r_"o")
  approx 1 / (A dot g_"m" r_"o")
$ <eq_line_regulation>

When testing the LDO line regulation performance, the small signal parameters $g_"m"$ and $r_"o"$ of the pass transistor can be considered constant. Therefore, it's line performance can be estimated by @eq_line_regulation.

Simulation shows that at high load current and low dropout voltage conditions, the $r_"o"$ of the pass transistor degrades significantly due to channel length modulation, leading to an intrinsic gain $g_"m" r_"o"$ of only around 1. To ensure line regulation of less than #qty(10, "mV/V", per: "\/"), the error amplifier is designed to have a high gain of around #qty(40, "dB").

#figure(
  image("../figures/opamp.png"),
  caption: [Error amplifier schematic],
) <opamp>

The error amplifier schematic is shown in @opamp, which is a two-stage amplifier with Miller compensation. The first stage is a differential pair with current mirror load, providing high gain and common-mode rejection. The second stage is a common-source amplifier that further amplifies the signal before driving the bootstrap circuit. The current ratio between the two stages is set to #qty(2, "uA"):#qty(8, "uA") to provide sufficient slew rate at the output.

= Simulation Results

#figure(
  image("../figures/TB_ldo.png"),
  caption: [Simulation testbench schematic],
) <TB_ldo>

The proposed bootstrapped NMOS LDO is implemented in a standard #qty(65, "nm") CMOS process. The LDO receives a reference voltage $V_"ref"$ of #qty(0.6, "V"), resulting in a nominal output voltage $V_"out"$ of #qty(1.0, "V"). The 2-way non-overlapping bootstrap clock frequency is set to #qty(12.5, "MHz"). The simulation testbench schematic is shown in @TB_ldo.

== Line Regulation <line_regulation>

#figure(
  image("../figures/line_regulation_vOut.svg"),
  caption: [Simulated line regulation performance],
) <line_regulation_vOut>

By sweeping the supply voltage $V_"dd"$ from #qty(1.1, "V") to #qty(1.8, "V") at constant load currents of #qty(100, "nA") and #qty(10, "mA"), respectively, the averaged stable state output voltage is simulated and presented in @line_regulation_vOut, which shows a line regulation of #qty(10.248, "mV/V", per: "\/") across the entire supply voltage range.

== Power Consumption

#figure(
  image("../figures/line_regulation_iQ.svg"),
  caption: [Simulated quiescent current under varying $V_"dd"$ and load conditions],
) <line_regulation_iQ>

Based on the conditions of @line_regulation, the quiescent current is simulated and presented in @line_regulation_iQ. The quiescent current remains relatively constant at around #qty(10, "uA") to #qty(20, "uA") across the entire supply voltage range, demonstrating the efficiency of the proposed design.

== Load Regulation

#figure(
  image("../figures/load_regulation_vOut.svg"),
  caption: [Simulated load regulation performance],
) <load_regulation_vOut>

By sweeping the load current from #qty(100, "nA") to #qty(10, "mA") at a constant supply voltage of #qty(1.2, "V"), the averaged stable state output voltage is simulated and presented in @load_regulation_vOut, which shows a load regulation of #qty(0.534, "mV/mA", per: "\/") across the entire load current range.

== Transient Response <tran_response>

The transient response of the LDO is evaluated by applying a step load current and observing the output voltage response. The rise and fall times of the load current step are set to #qty(1, "ps") to ensure accurate FoM calculation.

=== Small Step Load Change <small_step>

The load current steps from #qty(10, "uA") to #qty(1, "mA") and back to #qty(10, "uA"). The results are presented in @tran_comp_waveform and @tran_comp_waveform_zoom.

The output voltage exhibits an undershoot of #qty(274.90, "mV") and an overshoot of #qty(190.6, "mV") when the load current steps from #qty(10, "uA") to #qty(1, "mA") and back to #qty(10, "uA"), respectively. The settling time for both transitions is around #qty(15, "ns"). The response time from the load step to the peak of the undershoot is around #qty(68.21, "ps").

The corresponding figure of merit (FoM) is:
$
  "FoM"
  = T_"R" I_"Q" / I_"max"
  = #qty(68.21, "ps") dot #qty(13.38, "uA") / #qty(1, "mA")
  = #qty(912.6, "fs")
$ <eq_fom_small_step>

#figure(
  grid(
    columns: 2,
    image("../figures/tran_comp_waveform_undershoot.svg"), image("../figures/tran_comp_waveform_overshoot.svg"),
  ),
  caption: [Simulated transient response],
) <tran_comp_waveform>

#figure(
  image("../figures/tran_comp_waveform_undershoot_zoom.svg"),
  caption: [Simulated transient response],
) <tran_comp_waveform_zoom>

#figure(
  grid(
    columns: 2,
    image("../figures/tran_waveform_undershoot.svg"), image("../figures/tran_waveform_overshoot.svg"),
  ),
  caption: [Simulated transient response],
) <tran_waveform>

#figure(
  image("../figures/tran_waveform_undershoot_zoom.svg"),
  caption: [Simulated transient response],
) <tran_waveform_zoom>

=== Large Step Load Change <large_step>

The load current steps from #qty(100, "nA") to #qty(10, "mA") and back to #qty(100, "nA"). The results are presented in @tran_waveform and @tran_waveform_zoom.

The output voltage exhibits a much larger undershoot of #qty(664.17, "mV") and overshoot of #qty(109.6, "mV") under larger load current steps. The settling time for these transitions is around #qty(23, "ns"). The response time from the load step to the peak of the undershoot is around #qty(18.51, "ps").

The corresponding figure of merit (FoM) is:
$
  "FoM"
  = T_"R" I_"Q" / I_"max"
  = #qty(18.51, "ps") dot #qty(13.86, "uA") / #qty(10, "mA")
  = #qty(25.65, "fs")
$ <eq_fom_large_step>

== PSRR

Replacing the bootstrap circuit with a $V_"dd"\/2$ dc voltage source, the PSRR performance is simulated by applying a small-signal AC voltage source at the supply voltage node and measuring the output voltage AC response under multiple load & supply voltage conditions. The results are presented in @PSRR.

#figure(
  image("../figures/PSRR.svg"),
  caption: [Simulated PSRR performance],
) <PSRR>

The PSRR performance shows a higher attenuation of supply voltage variations than conventional PMOS LDOs, with a PSRR peaking of around #qty(-16.7, "dB") at around #qty(300, "MHz"). The worst case PSRR across all load and supply voltage conditions at low frequencies is around #qty(-34.0, "dB") under #qty(3, "MHz"), where the NMOS dropout gets too low and could not provide sufficient $r_"o"$. In most other conditions, the PSRR is less than #qty(-50, "dB") under #qty(3, "MHz").

= Conclusion

This work presents a bootstrapped NMOS LDO regulator designed to operate effectively under low supply voltage conditions while maintaining high performance in terms of line regulation, load regulation, transient response, and PSRR, as shown in a table. The proposed design leverages a bootstrap circuit to elevate the gate voltage of the NMOS pass transistor, enabling it to function efficiently even when the supply voltage is limited.

#figure(
  table(
    columns: (2fr, 1fr, 1fr),
    align: center + horizon,

    table.header([Metrics], [Values], [Units]),
    table.cell(rowspan: 2)[Line Regulation\ (#qty(1.1, "V")-#qty(1.8, "V"))],
    $10.248^1$, table.cell(rowspan: 2)[#unit("mV/V", per: "\/")],
    $9.983^2$,
    [Load Regulation\ (#qty(100, "nA")-#qty(10, "mA"))], $0.534$, unit("mV/mA", per: "\/"),
    [Quiescent Current\ (at #qty(1.2, "V") supply voltage)], $13.38$, unit("uA"),
    table.cell(rowspan: 2)[Transient Response FoM],
    $912.6^3$, table.cell(rowspan: 2)[#unit("fs")],
    $25.65^4$,
    table.cell(rowspan: 2)[PSRR],
    $lt.eq -34.0^5$, table.cell(rowspan: 2)[#unit("dB")],
    $-16.7^6$,

    table.cell(
      colspan: 3,
      align: left + horizon,
    )[
      #set text(size: 6pt)
      1 At constant load current of #qty(100, "nA").\
      2 At constant load current of #qty(10, "mA").\
      3 Load current step from #qty(10, "uA") to #qty(1, "mA").\
      4 Load current step from #qty(100, "nA") to #qty(10, "mA").\
      5 Under #qty(3, "MHz")\
      6 Peak PSRR at around #qty(300, "MHz")\
    ],
  ),
  caption: [Summary of the bootstrapped nmos ldo performance metrics],
) <tab:summary>

Additionally, the design exhibits robust PSRR performance, making it suitable for applications requiring stable power delivery in low-voltage environments. The proposed bootstrapped NMOS LDO offers a promising solution for modern low-power electronic systems.

== Potential Improvements

Despite the fast transient response, @tran_response shows significant undershoot and overshoot during load transients. For example, in @large_step, the #qty(664.17, "mV") undershoot may cause the regulated circuit to malfunction at low supply voltages.

Conventionally, adding a decoupling capacitor at the output node can help reduce voltage spikes during load transients by providing a temporary energy reservoir. However, they consume significant chip area and worsen response time as well as the FoM. In the case of @large_step, a decoupling capacitor of around #qty(2.3, "nF") is required to reduce the undershoot to less than #qty(100, "mV"), which is impractical for on-chip implementation.

// #total-words
