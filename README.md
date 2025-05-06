# Variabilidad-de-la-Frecuencia-Cardiaca

FUNDAMENTOS TEORICOS

Sistema Nervioso Autónomo (SNA)

-Actividad simpática: acelera la frecuencia cardíaca (respuesta a estrés).
-Actividad parasimpática: desacelera la frecuencia cardíaca (reposo y relajación).

Variabilidad de la Frecuencia Cardiaca (HRV)

-Representa fluctuaciones en los intervalos R-R.
-Refleja el equilibrio entre actividad simpática y parasimpática.
-HRV baja → estrés o enfermedad.
-HRV alta → buena salud cardiovascular y adaptabilidad.

Transformada Wavelet

-Herramienta de análisis tiempo-frecuencia para señales no estacionarias.
-Permite observar cómo cambia la potencia de ciertas frecuencias (LF, HF) a lo largo del tiempo.
-Wavelets adecuadas para biológicas: Morlet, Mexican Hat, Daubechies.

ADQUISICION DE LA SEÑAL

Se cargó la señal de ECG desde un archivo de texto plano (LINA2.txt) usando la función np.loadtxt, especificando que los valores están separados por comas. El archivo contiene únicamente los valores de voltaje adquiridos durante un experimento de 300 segundos de duración.

A partir del número total de muestras (num_muestras), se generó un vector de tiempo equiespaciado con np.linspace, que va desde 0 hasta 300 segundos. Esto permitió relacionar cada muestra con su instante de adquisición.

La frecuencia de muestreo efectiva fue estimada con la fórmula:

Fs=(numero de muestras)/(duración total)=N/T
 
lo que garantiza que el eje temporal y la señal estén correctamente sincronizados para su análisis.

Finalmente, se graficó la señal cruda en función del tiempo. Esta gráfica permite observar visualmente la forma de onda de la señal original antes de cualquier tipo de procesamiento, facilitando la identificación de posibles artefactos, ruido o pérdidas de información.

![image](https://github.com/user-attachments/assets/66be4a2f-a382-4b16-8119-93f85b387333)

Resultados: 

El numero ed muestras es:  120011

Tiempo final es:  300.0 segundos

La frecuencia de muestreo es:  400.0366666666667 Hz

--- Estadísticos de la señal cruda ---

Voltaje mínimo: 4.0000 V

Voltaje máximo: 246.0000 V

Media: 120.7679 V

Desviación estándar: 25.4015 V

PRE-PROCESAMIENTO DE LA SEÑAL 

Tipo de filtro: Butterworth pasa banda.
Se selecciona un filtro Butterworth por su respuesta en frecuencia suave y sin ondulaciones, ideal para señales biológicas donde se requiere preservación de la forma de la onda ECG.

Parámetros del filtro:

Frecuencia de muestreo (fs): calculada a partir del tiempo de adquisición.

Frecuencia de corte baja: 0.5 Hz (para eliminar tendencia de baja frecuencia y componente DC).

Frecuencia de corte alta: 40 Hz (para eliminar ruido muscular (EMG) y artefactos de alta frecuencia).

Orden del filtro: 4 (suficiente para buena pendiente de atenuación sin hacer inestable el filtro).

Fórmulas utilizadas:

Frecuencias normalizadas:

![image](https://github.com/user-attachments/assets/8b322acb-d16a-4bde-82da-a6ecaf320b82)




