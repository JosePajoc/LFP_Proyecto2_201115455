from tkinter import *
from tkinter import filedialog                      #Módulo para abrir ventana de selección
from tkinter import messagebox                      #Módulo para cuadros de mensaje
from tkinter import *                               #Módulo para entorno gráfico
from tkinter import ttk                             #Módulo para usar comboBoxs
import re                                           #Módulo de expresiones regulares

#------------------------------------------Global-------------------------------------------------------------
archivoCargado = False

#-----------------------------------------Funciones-----------------------------------------------------------
def abrirArchivo():
    global archivoCargado
    rutaArchivo = filedialog.askopenfilename(title = "Seleccionar archivo XML")
    extension = re.findall('(\.lfp)$', rutaArchivo)                    #<------------ ver extensión valida
    
    if rutaArchivo == '':
        messagebox.showinfo('Error','No se selecciono nigún archivo')
    elif len(extension)>0 and extension[0] == '.lfp':
        archivoCargado = open(rutaArchivo, 'r')
        archivoLFP = archivoCargado.read()
        archivoCargado.close()
        datosDelArchivo = archivoLFP.lower()                               #Cambio a minúsculas
        print(datosDelArchivo)
        messagebox.showinfo('Información','Cargado con éxito')
        archivoCargado = True
    else:
        messagebox.showinfo('Error','El archivo seleccionado no posee extensión \'.pxla\'')
        rutaArchivo = ''


#----------------------------------Objetos de entorno gráfico Global---------------------------------------------
ventana = Tk()
marcoInicial = Frame()
btnAbrir = Button(marcoInicial, text='Abrir archivo', command=abrirArchivo)
btnAnalizar = Button(marcoInicial, text='Analizar archivo')
btnVerReporte = Button(marcoInicial, text='Ver reporte')
lstSeleccionarReporte = ttk.Combobox(marcoInicial, width=25, state='readonly')      #comboBox
txtEditor = Text(marcoInicial, bg="#566573", foreground="white")          #Área de texto
txtConsola = Text(marcoInicial, bg="black", foreground="white", state='disabled')


#------------------------------------Entorno grafico----------------------------------------------------------
def ventana_inicial():
    global ventana, marcoInicial, btnAbrir, btnAnalizar, lstSeleccionarReporte, txtEditor
    ventana.title('Consola LFP')
    ventana.geometry('800x600')
    ventana.resizable(False, False)
    marcoInicial.pack()
    marcoInicial.config(width='750', height='600')
    btnAbrir.place(x=50, y=20)
    btnAnalizar.place(x=160, y=20)
    lstSeleccionarReporte.place(x=290, y=20)
    lstSeleccionarReporte['values'] = ['Reporte de Tokens', 'Reporte de Errores', 'árbol de derivación'] #Valores del comboBox
    btnVerReporte.place(x=490, y=20)
    txtEditor.place(x=30, y=100)
    txtEditor.config(width=35, height=20)
    txtConsola.place(x=400, y=100)
    txtConsola.config(width=35, height=20)


if __name__=='__main__':
    ventana_inicial()


ventana.mainloop()