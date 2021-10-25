from tkinter import filedialog                      #Módulo para abrir ventana de selección
from tkinter import messagebox                      #Módulo para cuadros de mensaje
from tkinter import *                               #Módulo para entorno gráfico
from tkinter import ttk                             #Módulo para usar comboBoxs
import re                                           #Módulo de expresiones regulares

#------------------------------------------Global-------------------------------------------------------------
archivoCargado = None
cargarArch = False
reservadas = ['claves', 'registros', 'imprimir', 'imprimirln', 'conteo', 'promedio', 'contarsi', 'datos', 'sumar',
'max', 'min', 'exportarreporte']
claves = []
registros = []


#-----------------------------------------Funciones-----------------------------------------------------------
def esLetra(caracter):
    valor = ord(caracter)                   #Convertir ASCII a entero
    if ((valor>= 65) and (valor<=90)) or ((valor>= 97) and (valor<=122)) or valor==165 or valor==164:
        return True
    else:
        return False

def esNumero(caracter):
    valor = ord(caracter)                   #Convertir ASCII a entero
    if ((valor>= 48) and (valor<=57)):
        return True
    else:
        return False

def imprimible(caracter):                   #Convertir ASCII imprimible a entero
    valor = ord(caracter)
    if (valor>=33 and valor<=39) or (valor>=128 and valor<=239) or (valor == 95):
        return True
    else:
        return False

def esComa(caracter):
    valor = ord(caracter)
    if valor == 44:
        return True
    else:
        False

def analizar(entrada):
    global txtConsola
    
    fila = 1
    columna = 0
    estado = 0
    lexemaAct = ''
    for c in entrada:
        if estado == 0:
            if esLetra(c):
                lexemaAct = lexemaAct + c
                estado = 1
            elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9:       #Ignorar espacio en blanco, nueva línea, tabulación horizontal
                pass 
            else:
                lexemaAct = ''
                estado = 0
        elif estado == 1:
            if esLetra(c):
                lexemaAct = lexemaAct + c
                estado = 1
            elif c == '=':
                lexemaAct = lexemaAct + c
                estado = 2
            elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9:       #Ignorar espacio en blanco, nueva línea, tabulación horizontal
                pass 
            else:
                lexemaAct = ''
                estado = 0
        elif estado == 2:
            if c == '[':
                lexemaAct = lexemaAct + c
                estado = 3
            elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9:       #Ignorar espacio en blanco, nueva línea, tabulación horizontal
                pass 
            else:
                lexemaAct = ''
                estado = 0
        elif estado == 3:
            if c == '"':
                lexemaAct = lexemaAct + c
                estado = 4
            elif c == '{':
                lexemaAct = lexemaAct + c
                estado = 5
            elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9:       #Ignorar espacio en blanco, nueva línea, tabulación horizontal
                pass 
            else:
                lexemaAct = ''
                estado = 0
        elif estado == 4:
            if esLetra(c):
                lexemaAct = lexemaAct + c
                estado = 6
            else:
                lexemaAct = ''
                estado = 0
        elif estado == 5:
            if esLetra(c):
                lexemaAct = lexemaAct + c
                estado = 9
            elif esNumero(c):
                lexemaAct = lexemaAct + c
                estado = 9
            elif c == '"':
                lexemaAct = lexemaAct + c
                estado = 9
            elif c == '.':
                lexemaAct = lexemaAct + c
                estado = 9
            elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9:       #Ignorar espacio en blanco, nueva línea, tabulación horizontal
                pass 
            else:
                lexemaAct = ''
                estado = 0
        elif estado == 6:
            if c == '"':
                lexemaAct = lexemaAct + c
                estado = 7
            elif esLetra(c):
                lexemaAct = lexemaAct + c
                estado = 6
            elif esNumero(c):
                lexemaAct = lexemaAct + c
                estado = 6
            elif imprimible(c):
                lexemaAct = lexemaAct + c
                estado = 6
            elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9:       #Ignorar espacio en blanco, nueva línea, tabulación horizontal
                pass 
            else:
                lexemaAct = ''
                estado = 0
        elif estado == 7:
            if c == ',':
                lexemaAct = lexemaAct + c
                estado = 3
            elif c == ']':
                lexemaAct = lexemaAct + c
                estado = 8
            elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9:       #Ignorar espacio en blanco, nueva línea, tabulación horizontal
                pass 
            else:
                lexemaAct = ''
                estado = 0
        elif estado == 8:
            valido = False
            extraccion = ''
            print('Se reconocio en S8: ' + lexemaAct + ' fila: ' , fila , ' col: ', columna-(len(lexemaAct)-1))
            for palabraR in reservadas:
                if lexemaAct.startswith(palabraR):
                    valido = True
            if valido:
                #extraer claves y asignar a lista de claves
                if lexemaAct.startswith('claves'):
                    extraccion = lexemaAct.replace('claves', '')        #Quitar la plabra claves
                    extraccion = extraccion.replace('=[', '')           #Quitar =[
                    extraccion = extraccion.replace(']', '')            #Quitar ]
                    extraccion = extraccion.replace('"', '')            #Quitar comillas
                    extraccion = extraccion + ','
                    temporal = ''
                    for c in extraccion:
                        if c != ',':                                    #Separación por comas
                            temporal = temporal + c
                        else:
                            claves.append(temporal)
                            temporal = ''
                    #print(claves)
                #extraer registros y asignar a lista de registros
                if lexemaAct.startswith('registros'):
                    extraccion = lexemaAct.replace('registros', '')     #Quitar la plabra registros
                    extraccion = extraccion.replace('=[', '')           #Quitar =[
                    extraccion = extraccion.replace(']', '')            #Quitar ]
                    temp = []
                    temporal = ''
                    for c in extraccion:
                        if c != '}':                                    #Separación por }
                            temporal = temporal + c
                        else:
                            temp.append(temporal)
                            temporal = ''
                    temporal = ''
                    for i in range(len(temp)):                          
                        temp[i] = temp[i].replace('{', '')              #Quitar { de cada registro
                        temp[i] = temp[i] + ','
                        for c in temp[i]:
                            if c != ',':                                    #Separación por comas
                                temporal = temporal + c
                            else:
                                print(temporal)
                                temporal = ''
                    
                    #print('Elementos en registro: ' , len(temp))
                    #print(temp)
            lexemaAct = ''
            estado = 0

        elif estado == 9:
            if c == '"':
                lexemaAct = lexemaAct + c
                estado = 9
            elif c == '.':
                lexemaAct = lexemaAct + c
                estado = 9
            elif c == ',':
                lexemaAct = lexemaAct + c
                estado = 5  
            elif esLetra(c):
                lexemaAct = lexemaAct + c
                estado = 9
            elif esNumero(c):
                lexemaAct = lexemaAct + c
                estado = 9 
            elif c =='}':
                lexemaAct = lexemaAct + c
                estado = 10
            elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9:       #Ignorar espacio en blanco, nueva línea, tabulación horizontal
                pass 
            else:
                lexemaAct = ''
                estado = 0
        elif estado == 10:
            if c == '{':
                lexemaAct = lexemaAct + c
                estado = 5
            elif c == ']':
                lexemaAct = lexemaAct + c
                estado = 8
            elif ord(c) == 32 or ord(c) == 10 or ord(c) == 9:       #Ignorar espacio en blanco, nueva línea, tabulación horizontal
                pass 
            else:
                lexemaAct = ''
                estado = 0
            
            
            '''lexema = '\n>>' +  extraccion
            txtConsola.config(state='normal')
            txtConsola.insert('insert', lexema)
            txtConsola.config(state='disabled')'''
            
        

        # Control de filas y columnas
        if (ord(c) == 10):              #Salto de Línea
            columna = 0
            fila = fila + 1
            continue
        elif (ord(c) == 9):             #Tabulación Horizontal
            columna = columna +  4
            continue
        elif (ord(c) == 32):            #Espacio en blanco
            columna = columna + 1
            continue
        
        columna = columna + 1
        


def abrirArchivo():
    global archivoCargado, cargarArch, ventana, txtEditor
    rutaArchivo = filedialog.askopenfilename(title = "Seleccionar archivo XML")
    extension = re.findall('(\.lfp)$', rutaArchivo)                    #<------------ ver extensión valida
    
    if rutaArchivo == '':
        messagebox.showinfo('Error','No se selecciono nigún archivo')
    elif len(extension)>0 and extension[0] == '.lfp':
        archivoCargado = open(rutaArchivo, 'r')
        archivoLFP = archivoCargado.read()
        archivoCargado.close()
        datosDelArchivo = archivoLFP.lower()                               #Cambio a minúsculas
        
        messagebox.showinfo('Información','Cargado con éxito')
        cargarArch = True
        ventana.title('Consola LFP - ' + rutaArchivo)
        txtEditor.insert('insert', datosDelArchivo)                        #Mostrar datos del archivo en el editor de texto
    else:
        messagebox.showinfo('Error','El archivo seleccionado no posee extensión \'.pxla\'')
        rutaArchivo = ''


def leerCodigo():
    global txtEditor
    if cargarArch:
        codigo = txtEditor.get('1.0', 'end-1c')                             #Extraer contenido del editor de texto
        txtConsola.config(state='normal')
        txtConsola.insert('insert', '>>Ejecución iniciada')
        txtConsola.config(state='disabled')
        analizar(codigo)
        
    else:
        messagebox.showwarning('Error', 'No se ha cargado el archivo...')


#----------------------------------Objetos de entorno gráfico Global---------------------------------------------
ventana = Tk()
marcoInicial = Frame()
btnAbrir = Button(marcoInicial, text='Abrir archivo', command=abrirArchivo)
btnAnalizar = Button(marcoInicial, text='Analizar archivo', command=leerCodigo)
btnVerReporte = Button(marcoInicial, text='Ver reporte')
lstSeleccionarReporte = ttk.Combobox(marcoInicial, width=25, state='readonly')      #comboBox
txtEditor = Text(marcoInicial, bg="#566573", foreground="white", width=70, height=25)          #Área de texto
txtConsola = Text(marcoInicial, bg="black", foreground="white", state='disabled', width=70, height=25)


#------------------------------------Entorno grafico----------------------------------------------------------
def ventana_inicial():
    global ventana, marcoInicial, btnAbrir, btnAnalizar, lstSeleccionarReporte, txtEditor
    ventana.title('Consola LFP')
    ventana.geometry('1250x550')
    ventana.resizable(False, False)
    marcoInicial.pack()
    marcoInicial.config(width='1250', height='550')
    btnAbrir.place(x=50, y=20)
    btnAnalizar.place(x=160, y=20)
    lstSeleccionarReporte.place(x=290, y=20)
    lstSeleccionarReporte['values'] = ['Reporte de Tokens', 'Reporte de Errores', 'árbol de derivación'] #Valores del comboBox
    btnVerReporte.place(x=490, y=20)
    txtEditor.place(x=30, y=100)
    txtConsola.place(x=635, y=100)  


if __name__=='__main__':
    ventana_inicial()


ventana.mainloop()