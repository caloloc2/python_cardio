# librerias para codificar la parte visual (ventanas, botons, etc)
from Tkinter import *
import Tkinter as tk
# libreria pra convertir timestamp en formato fecha
from datetime import datetime
# librerias para manejar el tiempo(delay), archivos csv y puerto serial
import time, csv, serial

# funcion para el envio de datos por puerto serial
def envio_serial(dato):
    global puerto, mensaje

    #obtiene el puerto a manejar desde el campo de la ventana
    puerto_com = puerto.get()

    if (puerto_com != ""):
        # Iniciando conexion serial
        arduinoPort = serial.Serial(puerto_com, 9600, timeout=1)
        flagCharacter = dato
        
        # Retardo para establecer la conexion serial
        time.sleep(1.8) 
        arduinoPort.write(flagCharacter)        

        # Cerrando puerto serial
        arduinoPort.close()
    else:
        mensaje.config(text="No se ha indicado el puerto a usar.")
        mensaje.config(fg="red")

def procesar_csv():
    global boton_inicio, amplitud, tiempo, mensaje, archivo
    
    # obtiene desde los campos de la ventana
    ref_amp = float(amplitud.get())
    ref_tmp = float(tiempo.get())
    archivo_csv = archivo.get()

    # valida que se haya ingresado los dos valores de tiempo y amplitud
    if ((ref_amp!="") and (ref_tmp!="")):        
        mensaje.config(text=" ")
        with open(archivo_csv) as csvfile: # abre el documento especificado para su lectura
            reader = csv.DictReader(csvfile)
            convulsion = False # variable que determina si cumple las condiciones para convulsionar o no

            aux = 0 # variable de conteo 
            for row in reader:    # recorre cada linea del archivo csv para obtener los datos
                try:
                    timestamp = float(row['title:12']) # TimeStamp
                    tiempo = datetime.fromtimestamp(timestamp) # convierte a formato fecha                    
                    segundo = tiempo.second # obtiene los segundos 
                    segundo_aux = 0 # variable auxiliar

                    af3 = float(row[' headset type:INSIGHT']) # EEG.AF3
                    t7 = float(row[' headset serial:A1D20009']) # EEG.T7
                    pz = float(row[' headset firmware:930']) # EEG.Pz
                    t8 = float(row[' subject name:rbri19']) # EEG.T8
                    af4 = float(row[' channels:87']) # EEG.AF4
                    
                    # si alguno de los valores obtenidos supera al limite establecido en la ventana (amplitud)
                    if ((af3>ref_amp) or (t7>ref_amp) or (pz>ref_amp) or (t8>ref_amp) or (af4>ref_amp)):
                        # y si ademas, el tiempo es igual o supera al establecido (tiempo -> en segundos)
                        if (segundo_aux!=segundo): # si cambia el tiempo (segundo)
                            segundo_aux = segundo # guarda el ultivo valor
                            aux += 1 # cuenta las iteraciones en segundos
                except:
                    print("No se pudo convertir la variable tiempo")
            
            if (aux>=ref_tmp): # si las iteraciones sobrepasan el tiempo de referencia establecido
                convulsion = True # paciente convulsionando
            
            if (convulsion): # si es verdadero
                print ('El paciente esta convulsionando')
                envio_serial('a') # envia la letra a por puerto serial
            else: # caso contrario (es decir, es falso)
                print ('El paciente no esta convulsionando')
                envio_serial('b') # envia la letra a por puerto serial
    else:        
        mensaje.config(text="Debe ingresar los dos valores")
        mensaje.config(fg="red")

raiz = tk.Tk()
# Centra la ventana en la pantalla
windowWidth = raiz.winfo_reqwidth()
windowHeight = raiz.winfo_reqheight()
positionRight = int(raiz.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(raiz.winfo_screenheight()/2 - windowHeight/2)
windowWidth = raiz.winfo_reqwidth()
windowHeight = raiz.winfo_reqheight()
raiz.geometry("+{}+{}".format(positionRight, positionDown))

raiz.title("Procesar CSV") # Cambiar el nombre de la ventana
raiz.geometry("200x240") # Configurar tamano

# recoge los datos para analizar los valores del csv
Label(raiz, text="Archivo a Analizar").pack()
archivo = Entry(raiz, justify="left", state="normal")
archivo.pack()

Label(raiz, text="Puerto Serial").pack()
puerto = Entry(raiz, justify="left", state="normal")
puerto.pack()

Label(raiz, text="Referencia 1 (amplitud)").pack()
amplitud = Entry(raiz, justify="right", state="normal")
amplitud.pack()

Label(raiz, text="Referencia 2 (tiempo [seg])").pack()
tiempo = Entry(raiz, justify="right", state="normal")
tiempo.pack()

Label(raiz, text="Procesar Archivo CSV").pack()
# Enlezamos la funcion a la accion del boton
boton_inicio = Button(raiz, text="INICIAR", command=procesar_csv)
boton_inicio.pack()

mensaje = Label(raiz, text=" ")
mensaje.pack()

raiz.mainloop() # muestra la ventana creada