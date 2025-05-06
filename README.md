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

la implementación con condiciones iniciales en cero.

Tipo de filtro: Butterworth pasa banda.
Se selecciona un filtro Butterworth por su respuesta en frecuencia suave y sin ondulaciones, ideal para señales biológicas donde se requiere preservación de la forma de la onda ECG.

Parámetros del filtro:

Frecuencia de muestreo (fs): calculada a partir del tiempo de adquisición.

Frecuencia de corte baja: 0.5 Hz (para eliminar tendencia de baja frecuencia y componente DC).

Frecuencia de corte alta: 40 Hz (para eliminar ruido muscular (EMG) y artefactos de alta frecuencia).

Orden del filtro: 4 (suficiente para buena pendiente de atenuación sin hacer inestable el filtro).

Fórmulas utilizadas: valores normalizados de las frecuencias de corte baja y alta, Porque muchos métodos de diseño de filtros en Python esperan frecuencias normalizadas en el rango de 0 a 1, donde 1 representa la frecuencia de Nyquist.

low=flowcut/fNysquit

high=fhighcut/fNysquit

Donde:𝑓nyquist=𝑓𝑠/2

El filtro IIR de orden 𝑁 se implementa mediante la siguiente ecuación en diferencias:

![image](https://github.com/user-attachments/assets/48e73b6b-cb4c-4050-a946-12f41e58e4a5)

donde:

y[n] es la salida filtrada en el instante n,

x[n] es la entrada en el instante n,

𝑎𝑘 y 𝑏𝑘 son los coeficientes del filtro calculados previamente.

![image](https://github.com/user-attachments/assets/8b322acb-d16a-4bde-82da-a6ecaf320b82)

![image](https://github.com/user-attachments/assets/d11ebf49-4699-4824-889c-b2173d63483a)


Resultados:
 Coeficientes del filtro:
b = [ 0.00462052  0.         -0.01848209  0.          0.02772313  0.
 -0.01848209  0.          0.00462052]
a = [  1.          -6.37351272  17.82658688 -28.63910936  28.95397956
 -18.88197531   7.75812255  -1.83562278   0.19153118]

 Ecuacioón en diferencias 

  y[n]=  6.3735⋅y[n−1]−17.8266⋅y[n−2]+28.6391⋅y[n−3]−28.9540⋅y[n−4]
+18.8820⋅y[n−5]−7.7581⋅y[n−6]+1.8356⋅y[n−7]−0.1915⋅y[n−8]
+0.0046⋅x[n]−0.0185⋅x[n−2]+0.0277⋅x[n−4]−0.0185⋅x[n−6]+0.0046⋅x[n−8]

y[n]=3.7605y[n−1]−5.3150y[n−2]+3.3695y[n−3]−0.8187y[n−4]
+0.0048x[n]−0.0096x[n−2]+0.0048x[n−4]
​
Análisis de la HRV en el dominio del tiempo

La Variabilidad de la Frecuencia Cardíaca (HRV) es una medida de las variaciones en los intervalos de tiempo entre latidos cardíacos consecutivos, conocidos como intervalos R-R, obtenidos de una señal ECG. Un análisis en el dominio del tiempo proporciona información sobre el control autónomo del corazón, reflejando la actividad simpática y parasimpática.

Detección de picos R: Se aplicó un umbral adaptativo:

umbral=𝜇+0.3⋅𝜎

Donde 

μ y σ son la media y la desviación estándar del ECG filtrado. Se usó find_peaks con una distancia mínima entre picos para asegurar que se correspondan con latidos reales (aprox. ≥0.4s, lo que evita detectar picos falsos en intervalos cortos).

Cálculo de Intervalos R-R: Se calcularon con:

𝑅𝑅𝑖=𝑡(𝑅𝑖+1)−𝑡(𝑅𝑖)
 
Primeros 5 intervalos detectados:
[0.687, 1.075, 1.095, 1.012, 1.002] s

Frecuencia Cardíaca Promedio

FC promedio=60/mean(𝑅𝑅)=600/0.7277≈82.45 bpmFC 

Esto representa una frecuencia cardíaca normal en reposo.

Mean RR indica un ritmo cardíaco normal (≈ 82 bpm).

SDNN es relativamente alta, lo que sugiere buena capacidad de adaptación del sistema nervioso autónomo.

RMSSD y pNN50 son elevados, lo cual refleja una alta actividad parasimpática, característica de un individuo con buena recuperación y bajo estrés.

Estos valores son coherentes entre sí, sin inconsistencias numéricas, lo que valida la calidad del análisis.

Resultados: 

Intervalos R-R (primeros 5): [0.68744271 1.07491042 1.09490876 1.01241563 1.00241647] segundos

Frecuencia cardíaca promedio: 82.45 bpm

Primeros 5 intervalos R-R (s): [0.68744271 1.07491042 1.09490876 1.01241563 1.00241647]
Primeros 5 tiempos de R-R: [0.37121907 1.25239563 2.33730522 3.39096742 4.39838347]

--- PARÁMETROS DE HRV EN DOMINIO DEL TIEMPO ---
Mean RR: 0.7277 s
SDNN: 0.1556 s
RMSSD: 0.1219 s
NN50: 200
pNN50: 48.66 %

![image](https://github.com/user-attachments/assets/17e8d245-1a74-430b-905c-6287c8cd4708)

Los valores del intervalo R-R oscilan aproximadamente entre 0.45 s y 1.15 s, lo cual sugiere que la frecuencia cardíaca varió entre unos 52 y 133 latidos por minuto (bpm). Se observa una tendencia en U: Al principio los intervalos son altos (latidos más espaciados → menor FC). Luego los intervalos disminuyen (aumento de la FC). Finalmente, los intervalos vuelven a subir (disminución de la FC).

![image](https://github.com/user-attachments/assets/44c6034b-532e-4897-8875-c15ca8f9da04)

Se observa una frecuencia cardíaca que varía entre ~55 bpm y más de 140 bpm. La forma general también tiene una tendencia en U invertida: aumento de la frecuencia hacia la mitad del registro y disminución al final. Hay picos súbitos, especialmente uno muy alto (>140 bpm), que podría deberse a: Un artefacto de señal Un error en la detección de un R O un latido prematuro que acortó transitoriamente el intervalo R-R.

Aplicación de transformada Wavelet

Transformada Wavelet Continua (CWT) con PyWavelets (pywt)
Usamos la wavelet 'cmor' (Complejo Morlet), ideal para análisis tiempo-frecuencia de señales fisiológicas
Aplicamos sobre la nueva señal de HRV (serie de intervalos R-R vs tiempo)

El espectrograma revela una señal HRV con predominio claro y sostenido en la banda LF y escasa presencia en HF, lo cual se interpreta como una activación simpática prolongada y una supresión de la actividad parasimpática. Este patrón podría estar asociado con una situación de estrés prolongado, ansiedad, exigencia cognitiva o emocional, aunque sin más contexto clínico no se puede confirmar la causa exacta.

Desde el punto de vista fisiológico, estos resultados indican un desequilibrio autonómico que se aleja del tono vagal saludable observado en condiciones de reposo. La falta de oscilaciones en HF, junto con la presencia constante en LF, sugiere una respuesta del sistema nervioso autónomo orientada al estado de alerta o defensa.

![image](https://github.com/user-attachments/assets/2f521a08-5367-409d-9e71-5f80cacf6908)

![image](https://github.com/user-attachments/assets/392d6ac4-762a-47b3-b3ed-42fa94548f61)

En el espectrograma se observa que la potencia está mayormente concentrada por debajo de los 0.15 Hz, especialmente entre 0.04 y 0.1 Hz, lo cual se representa con colores cálidos (amarillo y rojo) en los primeros segundos y hacia el final del registro. La franja correspondiente a frecuencias superiores a 0.15 Hz permanece en azul oscuro, lo que indica una potencia muy baja o nula en la banda HF. Esta distribución espectral refleja una dominancia simpática durante todo el registro, sin evidencias claras de actividad parasimpática ni de oscilaciones asociadas a la respiración, lo cual sugiere un estado fisiológico de activación constante.


 

​



