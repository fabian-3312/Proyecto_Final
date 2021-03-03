# Proyecto_Final-Logica_de_programacion



# Integrantes 
 > Maritzabel Cordoba Giraldo
 > 20191131053
 > Cristian Camilo Casallas Beltrán
 > 20201131025
 > Fabian Esteban Reyes Bejarano
 > 20201131048

## Universidad Distrital Francisco José de Caldas
## Tecnologia en Levantamientos topograficos
### 2020-lll

# Descripción
 >[Para este proyecto queremos generar un programa utilizando la herramienta de python, que nos permita realizar el calculo del ajuste de poligonales tanto cerradas como abiertas, teniendo en cuenta procedimientos como el ajuste de brujula o transito si la poligonal llegase a ser cerrada o de lo contrario utilizando el método de Crandall. Esto con finalidad de facilitar al maximo al usuario final una practica y rapida manera de llevar este proceso a cabo sin errores]

# Pasos para utilizar el programa
### Recomendaciones

 Para que su codigo no le presente problemas tenga en cuenta:

  - Su archivo debe ser (csv) de lo contrario no se reconocerá. Debe estar estructurado de la siguiente manera:
  - Los Angulos deben estar escritos en (gg.mmss),tome como ejemplo el siguiente: (17°25'36" = 17.2536)
  
  
         Delta       |    Angulo        |   Distancia           
   
(nombre del delta)   |(Angulo decimal)  |(Distancia puede ser con decimales)

(repetir N veces)    |(Repetir N veces) |(Repetir N veces)   



- la primera letra de la fila debe estar en mayuscula: Delta - Angulo - Distancia. Los nombres deben ser tal cual se muestran(sin comas, espacios o tildes).
- Favor realizar la cartera desde la primera fila y la primera columna
- Recuerde que al ser una poligonal cerrada esta debe cerrar en un mismo delta de inicio

- Al copiar la ruta y pegarla en la consola, le aparecerá de la siguiente forma:
"C:\Users\USUARIO\OneDrive\Documentos\MARITZABEL\LOGICA PROGRAMACION\hola_mundo.txt”. Se debe tener en cuenta que se debe copiar o eliminar las comillas que están presentes al inicio y final de la ruta. 

- La ruta de su archivo debe tener la siguiente estructura y cumplir con sus criterios:
- C: \ carpeta \ carpeta\...\Nombre del archivo(.)Ruta del acrchivo
- la unica separacion en carpeta debe ser (\)
- Ingrese la extencion sin comillas o comas al principio y al final.


# Procedimientos

- Digite si desea realizar un ajuste de poligonal. 1= si, 0= no 
- Digite si su poligonal es abierta o cerrada. 
- si usted elige abierta, su poligonal se ajustará por el método de crandall.
- En caso de que su poligonal sea cerrada, le preguntará si desea ajustarlo por el método de Brujula o por el método de Tránsito 
- Despúes de elegir que poligonal y cual método, debe ingresar la extensión del archivo como se recomendó anteriormente.
- Cada que el programa se ejecute de manera correcta, se anexara un archivo csv a la ruta de donde fue leido el primer archivo, con el nombre del archivo leido más ajuste de la poligonal y la fecha, hora de cuando se originóel programa.  
  
  
# INTERPRETE DE PYTHON Y COMANDOS DIRECTO

Es un leguaje de programación, la cual el humano ha diseñado para que la maquina lo interprete y e identifique la sintaxis y su semántica.
a continuación los pasos a seguir al momento de usar el código.

 1. Descargue **paython** en la versión de acuerdo a las características que se adapten a su equipó.     [link de python](<https://www.python.org/downloads)
 2. Descargue **VISUAL STUDIO CODE**   [link de Visual Studio Code](<https://code.visualstudio.com/download)
 3. Para comenzar abrimos el editor de python ( **Visual Studio Code**) y nos aparece al lado izquierdo la opción de crear una nueva carpeta. Digitamos el nombre que deseamos sin olvidar que se debe escribir el .py ejemplo:(antecedentes.py) y empezamos a ejecutar el código.
 4. Recuerde que puede usar otro editor que sea de su preferencia dentro de ellos, también se encuentra **jupyterNotebook**
 
 
 ## **POSIBLES ERRORES AL EJECUTAR EL CÓDIGO
 
 Es posible que cometas algunos errores en el momento de implementar el código de python, por eso te mostramos algunos de los errores que puedes cometer y que muestra el programa.
 
 1. El usuario ingresa un valor numérico, distinto a las opciones que se le plantean en pantalla o digita una letra.
Ejemplo: solucion = float(input('su poligonal es abierta o cerrada Abierta = 1 cerrada= 0: '))
si no usa ni el 1 ni el 2, en pantalla le aparece una notificación que le indica el error cometido pues números o letras distinto a lo solicitado interfieren en la ejecución del programa.

2. Para dar continuidad al programa,después de escribir de forma correcta la opción,en pantalla aparece un mensaje indicando que debe insertar la ruta de archivo de texto.
Si el usuario copia la  ruta de la siguiente manera, tendrá un error.
 
Al copiar la ruta y pegarla en la consola, le aparecerá de la siguiente forma:
"C:\Users\USUARIO\OneDrive\Documentos\MARITZABEL\LOGICA PROGRAMACION\hola_mundo.txt”. Se debe tener en cuenta que se debe copiar o eliminar las comillas que están presentes al inicio y final de la ruta. 
Para solucionar este error, en pantalla tendrá un mensaje indicando esta posible falla.
Uno de los más importantes escenarios, es la elaboración del archivo, pues debe estar estructurado correctamente para que se pueda leer. Debe estar de la siguiente forma:
•	Debe escribir la inicial del título en mayúscula 
•	No debe contener comas, sin espacios, asteriscos, espacios o tildes 
Uno de los datos que se pedirá introducir en las poligonales abiertas son las coordenadas de amarre y si el usuario no usa el formato solicitado en la consola, se produce un error , interrumpiendo el funcionamiento, dando lugar a la alerta en pantalla. (




 # **COMANDOS**
 ## **TIPO DE DATOS**
 **str**= secuencia de caracteres
 
 **type** = muestra la clase de código. Ej: print(" Hola Mundo")
 
 **type** = devuelve class- str
 
 **int** = Traduce número entero
 
 **float** = tipo de dato flotante
 
 **list**= Guardar datos para agrupar, se separa por comas y puedo tener lista con cualquier dato
 
 **input** = se utiliza para que el usuario introduzca los datos por consola y se almacenan en una variable.
  Ej: edad = input("Digite su edad:  ")
 
 **print** =  se utiliza para imprimir un string(texto) en pantalla
 ej: edad =  input("Digite su edad:  ")
 print(edad)
  **round=** Permite emitir un resultado con los decimales que deseamos.
 
 **NOTA = Los comandos se escriben en minúscula**
 # **CICLOS**
Como su nombre lo indica son ciclos ( repetitivo )
 **while =** (mientras ) mi límite depende de una condición. El opera mientras la condición no sea falsa, cuando la condición es falsa el ciclo para.

**for** = for, tiene límites (tiene definido cuantas veces voy a reiterar)
# **OPERADORES ARITMETICOS**

##**OPERACIÓN**  -------**PYTHON**
 **potencia**    ------------------         **
  **multiplicación** -------------          *
**división** ------------------------       /
**suma** -----------------------------    +
**resta**------------------------------     -
**modulos** ------------------------     %
 **divisón entera** ---------------       //

# **JERARQUIA**

 1. ()
 2.  ^ **
 3.  asterisco, /, mod , //,%
 4. (+ , -)
 
  # **Expresiones booleanas**
 
  **Constantes:** =     True, False
   **Operadores:**

   **and** - conjunción
   **or** - disyunción 
   **not** – negación
   ## Operadores relacionales
   **= =** (igual)
   **! =** (distinto)
   **< =** (≤, menor o igual)
    **> =** (≥, mayor o igual)
    **>** (mayor)
    **<** (menor)
    Para información sobre funciones predefinidas en python ver http://mundogeek.net/tutorial-python/
