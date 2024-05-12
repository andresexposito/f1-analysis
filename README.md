# Descripción

Este proyecto une dos de mis grandes pasiones: los datos y la Fórmula 1, obteniendo datos de FastF1 para generar gráficas comparativas en Python entre dos pilotos, durante el GP seleccionado. 

# Cómo usarlo

## -	IDE

Se utilizan las siguientes librerías, por lo que será necesario tenerlas instaladas antes de ejecutar el programa para que este funcione correctamente:
<ul>
<li>FastF1</li>	
<li>Numpy</li>
<li>Logging</li>
<li>Matplotlib</li>
<li>Seaborn</li>
</ul>

En primer lugar, debemos abrir la carpeta <i>F1_Analysis</i> con nuestro IDE favorito. Esta carpeta contiene, a su vez, una carpeta llamada cache, donde se almacenará la caché de nuestro programa, y un archivo llamado FastF1.py, que es el que utilizaremos para visualizar los gráficos.

Para inicializarlo, ejecutamos el archivo desde nuestro IDE y seguimos las instrucciones del programa, que nos solicitará una carrera y dos pilotos para realizar la comparativa. 

Si no sabemos los circuitos, países o pilotos disponibles, hay una serie de comandos, que nos mostrará el programa en cada caso, para poder ver las opciones que podemos elegir.

Una vez introducidos estos datos, nos irá mostrando los gráficos uno a uno. Para pasar al siguiente, únicamente debemos cerrar la ventana del gráfico y automáticamente aparecerá el siguiente.

## -	Google Colab
Ejecutamos la primera celda para instalar FastF1.

Una vez instalado, ejecutamos la segunda celda y seguimos las instrucciones del terminal situado debajo de la celda, donde nos solicitará una carrera y dos pilotos.

Los gráficos se mostrarán uno debajo de otro en la parte inferior del terminal.
