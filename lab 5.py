# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 17:22:18 2025

@author: HP RY5
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

# ------------ CARGAR DATOS -------------------
voltage = np.loadtxt("C:/Users/HP RY5/Desktop/Practica_1/LINA2.txt", delimiter=',')
# Definir duración total
duracion_total = 300  # segundos

# Número de muestras
num_muestras = len(voltage)

# Crear el vector de tiempo
tiempo = np.linspace(0, duracion_total, num_muestras)

# Mostrar para confirmar
print("El numero ed muestras es: ", num_muestras)
print("Tiempo final es: ", tiempo[-1], "segundos")


# ------------ ESTIMAR FRECUENCIA DE MUESTREO ------------
duracion_total = tiempo[-1] - tiempo[0]
fs = len(tiempo) / duracion_total
print("La frecuencia de muestreo es: ", fs, "Hz")
plt.figure(figsize=(20, 5))
plt.plot(tiempo, voltage, label="Señal Original", color='blue')
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Señal ECG Original")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------- ESTADÍSTICOS DE SEÑAL CRUDA -------------------
print("\n--- Estadísticos de la señal cruda ---")
print(f"Voltaje mínimo: {np.min(voltage):.4f} V")
print(f"Voltaje máximo: {np.max(voltage):.4f} V")
print(f"Media: {np.mean(voltage):.4f} V")
print(f"Desviación estándar: {np.std(voltage):.4f} V")
# ------------ DISEÑAR FILTRO IIR (BUTTERWORTH PASA-BANDA) ------------
lowcut = 0.5   # Hz
highcut = 40.0 # Hz
order = 4      # Orden del filtro

nyquist = 0.5 * fs
low = lowcut / nyquist
high = highcut / nyquist

b, a = butter(order, [low, high], btype='band')

# ------------ ECUACIÓN EN DIFERENCIAS ------------
# y[n] = -a1*y[n-1] - a2*y[n-2] - ... + b0*x[n] + b1*x[n-1] + ...
print("\nCoeficientes del filtro:")
print("b =", b)
print("a =", a)

# ------------ FILTRAR LA SEÑAL ------------
filtered_voltage = filtfilt(b, a, voltage)  # Condiciones iniciales asumidas en 0

plt.figure(figsize=(20, 5))
plt.plot(tiempo, filtered_voltage, label="Señal Filtrada (0.5-40 Hz)", color='orange')
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.title("Señal ECG Filtrada Completa")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------ DETECTAR PICOS R ------------
# Buscamos picos prominentes
threshold = np.mean(filtered_voltage) + 0.3 * np.std(filtered_voltage)
peaks, properties = find_peaks(filtered_voltage, height=threshold, distance=fs*0.4)  

# ------------ CALCULAR INTERVALOS R-R ------------
rr_intervals = np.diff(tiempo[peaks])  # en segundos
print("\nIntervalos R-R (primeros 5):", rr_intervals[:5], "segundos")

# ------------ GRAFICAR ------------
plt.figure(figsize=(20,6))
plt.plot(tiempo, filtered_voltage, label="Señal ECG Filtrada", color='orange')
plt.plot(tiempo[peaks], filtered_voltage[peaks], 'rx', label="Picos R detectados")
plt.xlabel('Tiempo (s)')
plt.ylabel('Voltaje (V)')
plt.title('ECG Filtrado con Picos R Detectados')
plt.legend()
plt.grid(True)
plt.xlim(0, 10)  # Puedes ampliar el rango si quieres
plt.tight_layout()
plt.show()

# ------------ OPCIONAL: MOSTRAR RITMO CARDIACO ------------
# Frecuencia cardiaca promedio (bpm)
mean_rr = np.mean(rr_intervals)
heart_rate = 60 / mean_rr
print(f"\nFrecuencia cardíaca promedio: {heart_rate:.2f} bpm")
# ------------------- CÁLCULO DE INTERVALOS R-R -------------------

# Obtener tiempos de los picos R detectados
tiempos_picos = tiempo[peaks]  # tiempo en segundos

# Calcular los intervalos R-R
rr_intervals = np.diff(tiempos_picos)  # segundos

# Calcular los tiempos medios entre pares de picos R para la nueva señal
rr_times = tiempos_picos[:-1] + rr_intervals / 2  # punto medio entre cada par de picos

# Mostrar primeros resultados
print("\nPrimeros 5 intervalos R-R (s):", rr_intervals[:5])
print("Primeros 5 tiempos de R-R:", rr_times[:5])
# ------------------- GRAFICAR NUEVA SEÑAL DE HRV -------------------
plt.figure(figsize=(12, 4))
plt.plot(rr_times, rr_intervals, marker='o', linestyle='-', color='green')
plt.xlabel("Tiempo (s)")
plt.ylabel("Intervalo R-R (s)")
plt.title("Serie temporal de intervalos R-R (HRV)")
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------- FRECUENCIA CARDÍACA INSTANTÁNEA -------------------
# Calcular frecuencia en bpm
frecuencia_bpm = 60 / rr_intervals

# ------------------- GRAFICAR FRECUENCIA -------------------
plt.figure(figsize=(12, 4))
plt.plot(rr_times, frecuencia_bpm, marker='o', linestyle='-', color='purple')
plt.xlabel("Tiempo (s)")
plt.ylabel("Frecuencia Cardíaca (bpm)")
plt.title("Frecuencia Cardíaca Instantánea (derivada de los intervalos R-R)")
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------- PARÁMETROS DE HRV EN TIEMPO -------------------

# Mean RR (media de los intervalos)
mean_rr = np.mean(rr_intervals)

# SDNN (desviación estándar de los intervalos)
sdnn = np.std(rr_intervals, ddof=1)

# RMSSD (raíz cuadrada de la media de las diferencias cuadráticas sucesivas)
diff_rr = np.diff(rr_intervals)
rmssd = np.sqrt(np.mean(diff_rr**2))

# NN50 (cuántas diferencias consecutivas son > 50 ms)
nn50 = np.sum(np.abs(diff_rr) > 0.05)  # en segundos (50 ms = 0.05 s)

# pNN50 (porcentaje de NN50 respecto al total)
pnn50 = (nn50 / len(diff_rr)) * 100

# Mostrar resultados
print("\n--- PARÁMETROS DE HRV EN DOMINIO DEL TIEMPO ---")
print(f"Mean RR: {mean_rr:.4f} s")
print(f"SDNN: {sdnn:.4f} s")
print(f"RMSSD: {rmssd:.4f} s")
print(f"NN50: {nn50}")
print(f"pNN50: {pnn50:.2f} %")

import pywt
import matplotlib.pyplot as plt

# ------------------- TRANSFORMADA WAVELET CONTINUA -------------------

# Escalas adecuadas para frecuencias de interés
# Usamos frecuencias invertidas (pseudo-frecuencia = fs / escala)
sampling_interval = np.mean(np.diff(rr_times))  # tiempo entre muestras (segundos)

# Definir rango de frecuencias en Hz (LF y HF)
freqs = np.linspace(0.03, 0.5, 200)  # de 0.03 a 0.5 Hz
scales = pywt.scale2frequency('cmor1.5-1.0', 1) / (freqs * sampling_interval)

# Aplicar CWT
coeffs, frequencies = pywt.cwt(rr_intervals, scales, 'cmor1.5-1.0', sampling_period=sampling_interval)
power = np.abs(coeffs) ** 2

# ------------------- GRAFICAR ESPECTROGRAMA -------------------

plt.figure(figsize=(15, 6))
plt.contourf(rr_times, frequencies, power, 100, cmap='jet')
plt.title("Espectrograma HRV usando Transformada Wavelet (cmor)")
plt.ylabel("Frecuencia (Hz)")
plt.xlabel("Tiempo (s)")
plt.ylim(0, 0.5)
plt.colorbar(label='Potencia')
plt.tight_layout()
plt.show()