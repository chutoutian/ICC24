A sample of dataset after preprocess is provided. 

Parameters in each line are:
| time step | MAC rate | PDCP SDU numbers | MCS index | Cell level MAC rate | PRB numbers | APP layer throughput (bandwidth) |

The full raw dataset can be found at: https://drive.google.com/file/d/10ifhBa4-1Ytn2pRYoX-gFPCKIh0Ctus8/view?usp=sharing

## Descriptions

We conduct five experiments and collected five datasets. Sets 1 to 5 represent five data collection records, with four data collection points, each having different wireless channel quality. Each expeirment includes 1 to 3 background terminals and 1 test terminal, distributed across the four data collection points.

During data collection, the test terminal repeatedly runs video downloading and the real-time download speeds are recorded. The base station side reports some lower-layer information of the wireless protocol stack to the data collection server (near-RT RIC).

The JSON file contains records of download speeds from the terminals, while the CSV file includes data reported by the base station, including background terminals, test terminals, and base station-level data

