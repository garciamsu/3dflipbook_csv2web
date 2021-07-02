import pandas as pd
import os
from shutil import rmtree


#Lectura del archivo fuente CSV
data = pd.read_csv("source.csv") 

#Define la ruta de la carpeta
root = os.getcwd()
pathname = os.path.join(root, "result")

#Limpia la carpeta existente de
rmtree(pathname)

#Se verifica que exista la carpeta destino
if not os.path.isdir(pathname):
    os.mkdir("result")

#Obtiene la lista del curso sin duplicación    
cursos = data['curso'].drop_duplicates()

for curso in cursos:    
    #Inialización    
    mensaje_html = ""   
    mensaje_html += "<!-- **************** Sección Específica ****************  -->" +  "\r\n"

    mensaje_css = ""
    mensaje_css += """/* **************** Sección General ****************  */
    .clicker {
    outline:none;
    cursor:pointer;
    }

    .myDiv {
    position:absolute;
    border: 5px outset white;
    background-color: white;
    text-align: center;
    font-size: 1.3em;
    font-weight: bold;
    width: 150px;    
    }\n\n"""
        
    name_html = os.path.join(pathname, curso.lower().replace(' ', '_') +'.html')
    name_css = os.path.join(pathname, curso.lower().replace(' ', '_') +'.css')
        
    #Se crea el archivo html
    f_html = open(name_html, 'w', encoding="utf-8")
    f_css = open(name_css, 'w', encoding="utf-8")
    
    sub_data = data.query("curso==@curso")
    
    
    for index, row in sub_data.iterrows():

        #subcadena = row[ini:fin]            
        code_number = row["url"][len(row["url"])-7:len(row["url"])-4]            
                
        code_html = """<!--  code_name  -->\n<div class="clicker_code_number myDiv" style="left:code_xpx; top:code_ypx"  tabindex="1">code_name</div>\n<div class="hiddendiv_code_number"></div> """

        code_css = """/* **************** code_name ****************  */
        .hiddendiv_code_number{
        position:absolute;
        z-index: 100;
        display:none;
        width: 700px; /* Definir de acuerdo al ancho de la imagen */
        height: 700px; /* Definir de acuerdo al alto de la imagen */
        content: url("code_url");
        left:150px; 
        top:240px;
        }

        .clicker_code_number:focus + .hiddendiv_code_number{
        display:block;
        }"""

        etiqueta = code_html.replace('code_name', row['nombre'])
        etiqueta = etiqueta.replace('code_number', code_number)
        etiqueta = etiqueta.replace('code_x', str(row['x']))
        etiqueta = etiqueta.replace('code_y', str(row['y']))

        estilo = code_css.replace('code_name', row['nombre'])
        estilo  = estilo .replace('code_number', code_number)
        estilo  = estilo .replace('code_url', str(row['url']))        
        
        mensaje_html += etiqueta +  "\r\n"
        mensaje_css += estilo +  "\r\n"        
        
    f_css.write(mensaje_css)
    f_css.close()

    f_html.write(mensaje_html)
    f_html.close()

