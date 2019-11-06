from Tkinter import *
import Tkinter as tk
import time, csv, serial

def envio_serial(dato):
    global puerto, mensaje

    puerto_com = puerto.get()

    if (puerto_com != ""):
        # Iniciando conexion serial
        arduinoPort = serial.Serial(puerto_com, 9600, timeout=1)
        flagCharacter = dato
        
        # Retardo para establecer la conexion serial
        time.sleep(1.8) 
        arduinoPort.write(flagCharacter)
        #getSerialValue = arduinoPort.readline()
        #getSerialValue = arduinoPort.read()
        #getSerialValue = arduinoPort.read(6)
        #print '\nValor retornado de Arduino: %s' % (getSerialValue)
        
        # Cerrando puerto serial
        arduinoPort.close()
    else:
        mensaje.config(text="No se ha indicado el puerto a usar.")
        mensaje.config(fg="red")

def procesar_csv():
    global boton_inicio, amplitud, tiempo, mensaje
    
    ref_amp = amplitud.get()
    ref_tmp = tiempo.get()

    if ((ref_amp!="") and (ref_tmp!="")):
        mensaje.config(text=" ")
        # boton_inicio.config(text='Procesando...')
        # boton_inicio.config(state=DISABLED) 
        with open('convulsion2.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:                
                #if (i==6):
                # print(row)
                # print(row[' headset type:INSIGHT']) # EEG.AF3
                # print(row[' headset serial:A1D20009']) # EEG.T7
                # print(row[' headset firmware:930']) # EEG.Pz
                # print(row[' subject name:rbri19']) # EEG.T8
                # print(row[' channels:87']) # EEG.AF4
                print ""
            envio_serial('a')
    else:        
        mensaje.config(text="Debe ingresar los dos valores")
        mensaje.config(fg="red")

raiz = tk.Tk()
# Gets the requested values of the height and widht.
windowWidth = raiz.winfo_reqwidth()
windowHeight = raiz.winfo_reqheight()
 
# Gets both half the screen width/height and window width/height
positionRight = int(raiz.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(raiz.winfo_screenheight()/2 - windowHeight/2)
# Gets the requested values of the height and widht.
windowWidth = raiz.winfo_reqwidth()
windowHeight = raiz.winfo_reqheight()

raiz.geometry("+{}+{}".format(positionRight, positionDown))

raiz.title("Procesar CSV") #Cambiar el nombre de la ventana
raiz.geometry("200x200") #Configurar tamano

# recoge los datos para analizar los valores del csv
Label(raiz, text="Puerto Serial").pack()
puerto = Entry(raiz, justify="left", state="normal")
puerto.pack()

Label(raiz, text="Referencia 1 (amplitud)").pack()
amplitud = Entry(raiz, justify="right", state="normal")
amplitud.pack()

Label(raiz, text="Referencia 2 (tiempo)").pack()
tiempo = Entry(raiz, justify="right", state="normal")
tiempo.pack()

Label(raiz, text="Procesar Archivo CSV").pack()
# Enlezamos la funcion a la accion del boton
boton_inicio = Button(raiz, text="INICIAR", command=procesar_csv)
boton_inicio.pack()

mensaje = Label(raiz, text=" ")
mensaje.pack()

raiz.mainloop()