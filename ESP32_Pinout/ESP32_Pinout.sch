EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Wire Notes Line
	7350 6000 5000 6000
Wire Notes Line
	5000 6000 5000 2150
Wire Notes Line
	5000 2150 7300 2150
Wire Notes Line
	7350 2150 7350 6000
Text Label 4500 5500 2    50   ~ 0
GND
Wire Wire Line
	5000 5350 4350 5350
Wire Wire Line
	5000 5200 4350 5200
Wire Wire Line
	5000 5050 4350 5050
Wire Wire Line
	5000 4900 4350 4900
Wire Wire Line
	5000 4750 4350 4750
Wire Wire Line
	5000 4600 4350 4600
Wire Wire Line
	5000 4450 4350 4450
Wire Wire Line
	5000 4300 4350 4300
Wire Wire Line
	5000 4150 4350 4150
Wire Wire Line
	5000 4000 4350 4000
Wire Wire Line
	5000 3850 4350 3850
Wire Wire Line
	5000 3700 4350 3700
Wire Wire Line
	5000 3550 4350 3550
Wire Wire Line
	5000 3400 4350 3400
Wire Wire Line
	5000 3250 4350 3250
Wire Wire Line
	5000 3100 4350 3100
Wire Wire Line
	5000 2950 4350 2950
Wire Wire Line
	8000 5300 7350 5300
Wire Wire Line
	8000 5150 7350 5150
Wire Wire Line
	8000 5000 7350 5000
Wire Wire Line
	8000 4850 7350 4850
Wire Wire Line
	8000 4700 7350 4700
Wire Wire Line
	8000 4550 7350 4550
Wire Wire Line
	8000 4400 7350 4400
Wire Wire Line
	8000 4250 7350 4250
Wire Wire Line
	8000 4100 7350 4100
Wire Wire Line
	8000 3950 7350 3950
Wire Wire Line
	8000 3800 7350 3800
Wire Wire Line
	8000 3650 7350 3650
Wire Wire Line
	8000 3500 7350 3500
Wire Wire Line
	8000 3350 7350 3350
Wire Wire Line
	8000 3200 7350 3200
Wire Wire Line
	8000 3050 7350 3050
Wire Wire Line
	8000 2900 7350 2900
Wire Wire Line
	8000 5450 7350 5450
$Comp
L RF_Module:ESP32-WROOM-32 U1
U 1 1 5CB2FDBD
P 6200 4150
F 0 "U1" H 6200 5731 50  0000 C CNN
F 1 "ESP32-WROOM-32" H 6200 5640 50  0000 C CNN
F 2 "RF_Module:ESP32-WROOM-32" H 6200 2650 50  0001 C CNN
F 3 "https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf" H 5900 4200 50  0001 C CNN
	1    6200 4150
	-1   0    0    1   
$EndComp
Text Label 4500 5350 2    50   ~ 0
P23
Text Label 4500 5200 2    50   ~ 0
P22
Text Label 4500 5050 2    50   ~ 0
TX
Text Label 4500 4900 2    50   ~ 0
RX
Text Label 4500 4750 2    50   ~ 0
P21
Text Label 4500 4600 2    50   ~ 0
GND
Text Label 4500 4450 2    50   ~ 0
P19
Text Label 4500 4300 2    50   ~ 0
P18
Text Label 4500 4150 2    50   ~ 0
P5
Text Label 4500 4000 2    50   ~ 0
P17
Text Label 4500 3850 2    50   ~ 0
P16
Text Label 4500 3700 2    50   ~ 0
P4
Text Label 4500 3550 2    50   ~ 0
P0
Text Label 4500 3400 2    50   ~ 0
P2
Text Label 4500 3250 2    50   ~ 0
P15
Text Label 4500 3100 2    50   ~ 0
SD1
Text Label 4500 2950 2    50   ~ 0
SD0
Wire Wire Line
	5000 2800 4350 2800
Text Label 4500 2800 2    50   ~ 0
CLK
Text Label 8000 5450 2    50   ~ 0
3V3
Text Label 8000 5300 2    50   ~ 0
EN
Text Label 8000 5150 2    50   ~ 0
SVP
Text Label 8000 5000 2    50   ~ 0
SVN
Text Label 8000 4850 2    50   ~ 0
P34
Text Label 8000 4700 2    50   ~ 0
P35
Text Label 8000 4550 2    50   ~ 0
P32
Text Label 8000 4400 2    50   ~ 0
P33
Text Label 8000 4250 2    50   ~ 0
P25
Text Label 8000 4100 2    50   ~ 0
P26
Text Label 8000 3950 2    50   ~ 0
P27
Text Label 8000 3800 2    50   ~ 0
P14
Text Label 8000 3650 2    50   ~ 0
P12
Text Label 8000 3500 2    50   ~ 0
GND
Text Label 8000 3350 2    50   ~ 0
P13
Text Label 8000 3200 2    50   ~ 0
SD2
Text Label 8000 3050 2    50   ~ 0
SD3
Text Label 8000 2900 2    50   ~ 0
CMD
Wire Wire Line
	7350 2750 8000 2750
Text Label 8000 2750 2    50   ~ 0
5V
Wire Wire Line
	5000 5500 4350 5500
$Comp
L Connector:USB_B_Micro J1
U 1 1 5CB3F92B
P 6200 2400
F 0 "J1" H 6257 2867 50  0000 C CNN
F 1 "USB_B_Micro" H 6257 2776 50  0000 C CNN
F 2 "" H 6350 2350 50  0001 C CNN
F 3 "~" H 6350 2350 50  0001 C CNN
	1    6200 2400
	0    1    1    0   
$EndComp
$Comp
L Switch:SW_Push SW1
U 1 1 5CB43DF3
P 5500 2300
F 0 "SW1" H 5500 2585 50  0000 C CNN
F 1 "SW_Push" H 5500 2494 50  0000 C CNN
F 2 "" H 5500 2500 50  0001 C CNN
F 3 "~" H 5500 2500 50  0001 C CNN
	1    5500 2300
	-1   0    0    1   
$EndComp
$Comp
L Switch:SW_Push SW2
U 1 1 5CB45AC6
P 6950 2250
F 0 "SW2" H 6950 2535 50  0000 C CNN
F 1 "SW_Push" H 6950 2444 50  0000 C CNN
F 2 "" H 6950 2450 50  0001 C CNN
F 3 "~" H 6950 2450 50  0001 C CNN
	1    6950 2250
	-1   0    0    1   
$EndComp
Text Notes 5600 2250 2    50   ~ 0
BOOT
Text Notes 7000 2250 2    50   ~ 0
EN\n
$EndSCHEMATC
