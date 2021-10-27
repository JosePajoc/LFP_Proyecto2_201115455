from datetime import datetime

class reporte():
    def __init__(self, claves, registros):
        self.claves = claves
        self.registros = registros
        self.ahora = datetime.now()

    def verDatos(self):
        print(self.claves)
        print(self.registros)
    
    def crearReporte(self, titulo):
        archivoCSS = open("reporte html/estilos.css", "w")
        contenidoCSS = """html {   font-size: 20px; font-family: 'Open Sans', sans-serif; } \n
                    h1 { font-size: 60px; text-align: center; } \n
                    p, li {   font-size: 16px;   line-height: 2;   letter-spacing: 1px; }\n
                    html { background-color: #00539F; }
                    body { width: 1100px; margin: 0 auto; background-color: #FF9500; padding: 0 20px 20px 20px; border: 5px solid black; }
                    h1 { margin: 0; padding: 20px 0; color: #00539F; text-shadow: 3px 3px 1px black; }"""
        archivoCSS.write(contenidoCSS)
        archivoCSS.close()

        nombreHTML = 'reporte html/' + titulo + '.html'
        archivoHTML = open(nombreHTML, 'w')
        archivoHTML.write('<!doctype html> \n')
        archivoHTML.write('<html> \n')
        archivoHTML.write('<head>\n')
        archivoHTML.write('\t<title>' + titulo +'</title>\n')
        archivoHTML.write('\t<link href="estilos.css" rel="stylesheet" type="text/css">\n')
        archivoHTML.write('</head>\n')
        archivoHTML.write("<body>\n")
        archivoHTML.write('<h1>Reporte elaborado: ' + str(self.ahora.date()) + '</h1>\n')
        archivoHTML.write('<h2>Hora: ' + str(self.ahora.hour) + ':' + str(self.ahora.minute) +'</h2>\n')
        
        archivoHTML.write('<table border = "1">')
        archivoHTML.write('<tr>')
        tamanio = len(self.claves)
        archivoHTML.write('<td colspan = "' + str(tamanio) + '">' + titulo + '</td>')
        archivoHTML.write('</tr>')

        archivoHTML.write('<tr>')
        for campo in self.claves:
            archivoHTML.write('<td>' + campo + '</td>')
        archivoHTML.write('</tr>')

        for fila in range(len(self.registros)):
            archivoHTML.write('<tr>')
            for col in range(len(self.registros[fila])):
                archivoHTML.write('<td>' + self.registros[fila][col] + '</td>')
            archivoHTML.write('</tr>')

        archivoHTML.write('</table>')
        archivoHTML.write("</body>\n")
        archivoHTML.write("</html>\n")
        archivoHTML.close()