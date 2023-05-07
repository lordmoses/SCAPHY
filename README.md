# SCAPHY: Detecting Modern ICS Attacks via Correlating Behaviors in SCADA and PHYsical

This repository contains dataset of the SCAPHY Paper, which appears at the IEEE Security and Privacy conference 2023 at San. Franscisco. 


This dataset contains both the SCADA host execution data and the Physical process data collected from the same ICS experiment. 

The SCADA data is induced by pertinent OPC events, which cause the configured SCADA event handlers to execute the SCADA process-control routines. The SCADA execution data is from real-world SCADA suites, MySCADA. We also have SCADA data from ScadaBR, which is an open source SCADA suite that runs on Apache Tomcat. We also have SCADA data from WINSPS, a Step7-type SCADA/ICS software program.

The Physical process data is collected from a combination of real-world processes running on Physical RTUs, historical data from industry partners, and simulations in a industry-scale testbed called FactoryIO.


We collected over 180G of experiemental data, some comprising of SCADA VMs and memory images. Most data are available based on special request since they cannot fit on the github server. To request data, email mosesjike@gatech.edu

If you use our dataset, please cite the SCAPHY paper. 

BibTex
`@inproceedings{ike2022scaphy, title={SCAPHY: Detecting Modern ICS Attacks by Correlating Behaviors in SCADA and PHYsical}, author={Ike, Moses and Phan, Kandy and Sadoski, Keaton and Valme, Romuald and Lee, Wenke}, booktitle={2023 IEEE Symposium on Security and Privacy (SP)}, pages={362--379}, year={2022}, organization={IEEE Computer Society}}`

Ike, Moses, et al. "SCAPHY: Detecting Modern ICS Attacks by Correlating Behaviors in SCADA and PHYsical." 2023 IEEE Symposium on Security and Privacy (SP). IEEE Computer Society, 2022.

