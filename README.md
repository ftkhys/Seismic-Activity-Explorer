# Seismic Activity Explorer

#### Video Demo: https://youtu.be/8pbCzWxQWUE?si=i1WJw8B6t1wNMDCS

#### Description:

Seismic Activity Explorer is a Python program that analyzes seismic activity recorded around Anak Krakatau on December 22, 2018. I chose this date because the seismic dataset I found contains waveform recordings from that date, which corresponds to a significant period of activity at Anak Krakatau. This made it an interesting real-world dataset to explore instead of using artificially generated data.

The program reads waveform data from a MiniSEED (`.seed`) file and allows the user to choose a seismic station from the stations available in the dataset. The goal of the project is to identify periods of elevated seismic activity and present the results in a way that is easier to understand than raw waveform data.

The main program is contained in `project.py`. The program uses the ObsPy library to read the MiniSEED file and automatically finds the seismic stations available in the dataset. After displaying the available stations and their channels, the user can select a station to analyze. The dataset contains 42 stations, and each station has three seismic channels: BHE, BHN, and BHZ.

For the selected station, the program analyzes each of its three seismic channels. The waveform is divided into one-minute windows. For each window, the program calculates the Root Mean Square (RMS) value, which provides a numerical representation of the amplitude of the seismic signal during that period.

The program then determines what can be considered normal activity for each channel. It calculates the median of the RMS values and the Median Absolute Deviation (MAD), and uses the formula `median + 3 × MAD` as the threshold for elevated activity. A window whose RMS value exceeds this threshold is classified as `HIGH`; otherwise, it is classified as `NORMAL`.

Consecutive high-activity windows are grouped together into events. The program then compares events detected across the three channels. This allows it to determine whether an event was detected by one, two, or all three channels. I chose this approach because the number of channels detecting an event provides a simple and understandable way to describe how consistently the activity appeared across the station's sensors. Events detected by one channel are classified as `WEAK`, two channels as `MODERATE`, and all three channels as `STRONG`.

The program also produces a human-readable summary after the detected events are displayed. Instead of only showing numerical results, the summary tells the user whether strong, moderate, or only isolated elevated activity was detected and gives the relevant time period. This makes the output easier to interpret without requiring the user to understand the underlying calculations.

The project contains three main files. `project.py` contains the complete program and its analysis functions. `test_project.py` contains pytest tests for several core functions, including activity classification, event overlap detection, and event strength classification. `requirements.txt` lists the external Python libraries required by the project, namely NumPy and ObsPy.

One important design choice was to keep the program terminal-based rather than building a graphical interface. This allowed me to focus on the Python programming concepts taught in CS50P while still creating a program that performs a meaningful analysis of real-world seismic data.

Another design choice was to use only the information available in the MiniSEED dataset rather than requiring additional external station metadata. This keeps the program self-contained and allows it to analyze the downloaded dataset without depending on an external service.

Overall, this project combines Python programming, numerical calculations, data processing, and automated testing to explore real seismic waveform data from Anak Krakatau.
