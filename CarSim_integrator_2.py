from pathlib import Path
from scipy import integrate
from matplotlib import pyplot
import numpy

contents_yaw_rate_o = Path('data_yaw_rate_o.txt').read_text()
contents_yaw_reference_o = Path('data_yaw_reference_o.txt').read_text()
contents_yaw_rate_v = Path('data_yaw_rate_v.txt').read_text()
contents_yaw_reference_v = Path('data_yaw_reference_v.txt').read_text()

# Output sljedeće funkcije će biti lista gdje je svaki pojedini element novi redak u učitanoj datoteci.
lines_rate_o = contents_yaw_rate_o.splitlines()
lines_ref_o = contents_yaw_reference_o.splitlines()

lines_rate_v = contents_yaw_rate_v.splitlines()
lines_ref_v = contents_yaw_reference_v.splitlines()

# Priprema liste.
rate_both_columns_o = []
ref_both_columns_o = []

rate_both_columns_v = []
ref_both_columns_v = []

# String na svakom retku pretvaram u svoju listu uz 4 razmaka kao separator, zatim te mini liste redaka spajam u veliku listu.
for line in lines_rate_o:
    if '	' in line:
        line_list = line.rsplit("	")
        rate_both_columns_o += line_list
for line in lines_ref_o:
    if '	' in line:
        line_list = line.rsplit("	")
        ref_both_columns_o += line_list

for line in lines_rate_v:
    if '	' in line:
        line_list = line.rsplit("	")
        rate_both_columns_v += line_list
for line in lines_ref_v:
    if '	' in line:
        line_list = line.rsplit("	")
        ref_both_columns_v += line_list

# Uklanjam prva dva elementa koji se odnose na nazive stupaca.
rate_both_columns_final_o = rate_both_columns_o[2:]
ref_both_columns_final_o = ref_both_columns_o[2:]

rate_both_columns_final_v = rate_both_columns_v[2:]
ref_both_columns_final_v = ref_both_columns_v[2:]

# Rastavljam na dvije liste, svaka za svoju fizikalnu veličinu.
yaw_rate_time_str_o = []
yaw_rate_str_o = []
yaw_ref_time_str_o = []
yaw_ref_str_o = []

yaw_rate_time_str_v = []
yaw_rate_str_v = []
yaw_ref_time_str_v = []
yaw_ref_str_v = []

# Enumerate pruža indeks svakom od elemenata na listi počevši s 0. Ako želim svaki drugi odvojit, kod izgleda kako izgleda:
for index, element in enumerate(rate_both_columns_final_o):
    if index % 2 == 0:
        yaw_rate_time_str_o.append(element)
    else:
        yaw_rate_str_o.append(element)
for index, element in enumerate(ref_both_columns_final_o):
    if index % 2 == 0:
        yaw_ref_time_str_o.append(element)
    else:
        yaw_ref_str_o.append(element)

for index, element in enumerate(rate_both_columns_final_v):
    if index % 2 == 0:
        yaw_rate_time_str_v.append(element)
    else:
        yaw_rate_str_v.append(element)
for index, element in enumerate(ref_both_columns_final_v):
    if index % 2 == 0:
        yaw_ref_time_str_v.append(element)
    else:
        yaw_ref_str_v.append(element)

# Lista stringova u listu floatova.
yaw_rate_o = []
for element in yaw_rate_str_o:
    yaw_rate_o.append(float(element))
yaw_rate_time_o = []
for element in yaw_rate_time_str_o:
    yaw_rate_time_o.append(float(element))
yaw_ref_o = []
for element in yaw_ref_str_o:
    yaw_ref_o.append(float(element))
yaw_ref_time_o = []
for element in yaw_ref_time_str_o:
    yaw_ref_time_o.append(float(element))

yaw_rate_v = []
for element in yaw_rate_str_v:
    yaw_rate_v.append(float(element))
yaw_rate_time_v = []
for element in yaw_rate_time_str_v:
    yaw_rate_time_v.append(float(element))
yaw_ref_v = []
for element in yaw_ref_str_v:
    yaw_ref_v.append(float(element))
yaw_ref_time_v = []
for element in yaw_ref_time_str_v:
    yaw_ref_time_v.append(float(element))

# Režem listu na otprilike 3. sekundu od početka simulacije gdje se yaw_rate napokon ustabilio. 
yaw_rate_4_o = yaw_rate_o[30:]
yaw_rate_time_4_o = yaw_rate_time_o[30:]
yaw_ref_4_o = yaw_ref_o[30:]
yaw_ref_time_4_o = yaw_ref_time_o[30:]

yaw_rate_4_v = yaw_rate_v[30:]
yaw_rate_time_4_v = yaw_rate_time_v[30:]
yaw_ref_4_v = yaw_ref_v[30:]
yaw_ref_time_4_v = yaw_ref_time_v[30:]

# Provjerom ustanovljeno da su, očekivano, vremenske liste za obje veličine jednake pa prelazimo na novu, zajedničku:
time = yaw_rate_time_4_o

# Provjerom preko lena ustanovljeno -> sve su 71 element.

result_o = []
subtraction_o = numpy.subtract(yaw_rate_4_o,yaw_ref_4_o)
result_o = integrate.cumtrapz(subtraction_o, time)

result_v = []
subtraction_v = numpy.subtract(yaw_rate_4_v,yaw_ref_4_v)
result_v = integrate.cumtrapz(subtraction_v, time)

# Ostaje pitanje toga kaj lista rezultata ima jedan član manje od liste vremena.
open = pyplot.plot(time[:-1], result_o)
viscous = pyplot.plot(time[:-1], result_v)
pyplot.yticks([0,-0.25,-0.5,-0.75,-1,-1.25,-1.5,-1.75, -2])
pyplot.grid(True)
pyplot.ylabel('Relative yaw angle [ °]')
pyplot.xlabel('Time [s]')
#pyplot.title('Relative yaw angle of a FWD vehicle for sudden WOT from\n steady state cornering around a 100 m radius skid pad.')
pyplot.legend(['open front differential', 'viscous front LSD'])
pyplot.show()



