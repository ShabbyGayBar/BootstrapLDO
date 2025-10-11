#import "@preview/charged-ieee:0.1.4": ieee

#show: ieee.with(
  title: [A Bootstrapped NMOS LDO Regulator for Low Supply Voltage and High PSRR],
  abstract: [
  ],
  authors: (
    (
      name: "Brian Li",
      // department: [Co-Founder],
      organization: [University of Macau],
      location: [Macau, China],
      email: "brian.li@connect.um.edu.mo",
    ),
  ),
  index-terms: ("Bootstrap switch", "Low-dropout regulator", "LDO", "Power management"),
  bibliography: bibliography("refs.bib"),
  figure-supplement: [Fig.],
)

= Introduction

Low-dropout (LDO) regulators are widely used in modern integrated circuits to provide stable and low-noise power supply voltages. However, traditional LDO designs often face challenges in achieving high power supply rejection ratio (PSRR) and low dropout voltage simultaneously, especially under low supply voltage conditions. This paper presents a novel bootstrapped NMOS LDO regulator that addresses these challenges by utilizing a bootstrapping technique to enhance the performance of the NMOS pass transistor.

= Design Methodology

- OpAmp
  - Gain
  - PM
- Clk gen
  - Non-overlap Waveform
- Level shifter
- Regulating NMOS
  - lvt
- Decoupling cap
  - pole
