import pandas as pd
import os
from os import remove
from shutil import rmtree

def file_is_empty(path): 
    #print("path: "+ path + " " + str(os.stat(path).st_size))
    return os.stat(path).st_size < 10


# inicialization
url = "https://anuario.montessorivirtual.org/wp-content/uploads/2021/07/"

# Lectura del archivo fuente CSV
df_comma = pd.read_csv("source.csv", sep=",")
df_semi = pd.read_csv("source.csv", sep=";")
if df_comma.shape[1] > df_semi.shape[1]:
    data = df_comma
else:
    data = df_semi

# Define la ruta de la carpeta
root = os.getcwd()
pathname = os.path.join(root, "result")

# Limpia la carpeta existente de
rmtree(pathname)

# Se verifica que exista la carpeta destino
if not os.path.isdir(pathname):
    os.mkdir("result")

# Obtiene la lista del curso sin duplicación
paginas = data['pagina'].drop_duplicates()

for pagina in paginas:
    # Inialización
    etiqueta = ""
    estilo = ""
    mensaje_html = ""
    mensaje_css = ""

    name_html = os.path.join(
        pathname, pagina.lower().replace(' ', '_') + '.html')
    name_css = os.path.join(
        pathname, pagina.lower().replace(' ', '_') + '.css')

    # Se crea el archivo html
    f_html = open(name_html, 'w', encoding="utf-8")
    f_css = open(name_css, 'w', encoding="utf-8")

    sub_data = data.query("pagina==@pagina")
    
    i = 1
    for index, row in sub_data.iterrows():

        # Obtiene el codigo del archivo
        code_number = row["campo"][len(row["campo"])-3:len(row["campo"])]
        code_url = url + row["campo"] + "." + row["extension"]

        if (row["tipo"] == "audio"):
            etiqueta = """<audio class="play-on-shown pause-on-hide" src="code_url"></audio>""".replace(
                'code_url', code_url)

        if (row["tipo"] == "video"):
            url_video = row["campo"]

            estilo = """
            .video_code_page_code_number {
            width: code_width;
            height: code_height;
            position: absolute;
            left: code_xpx;
            top: code_ypx
            }\n\n"""

            etiqueta = """<video class="video_code_page_code_number play-on-shown pause-on-hide" src="code_url"></video>"""
            
            etiqueta = etiqueta.replace('code_number', str(1))
            etiqueta = etiqueta.replace('code_page', pagina)
            
            etiqueta = etiqueta.replace('code_url', url_video)
            
            estilo = estilo.replace('code_number', str(1))
            estilo = estilo.replace('code_page', pagina)
            estilo = estilo.replace('code_width', str(row["ancho"]))
            estilo = estilo.replace('code_height', str(row["alto"]))
            estilo = estilo.replace('code_x', str(int(row['x'])))
            estilo = estilo.replace('code_y', str(int(row['y'])))
            
        if (row["tipo"] == "gif"):
            if (pd.isna(row['x']) or pd.isna(row['y']) or pd.isna(row['ancho'])):
                etiqueta = """<img width="100%" src="code_url">""".replace(
                'code_url', code_url)
            else:
                etiqueta = """<img style="position:absolute; left:code_xpx; top:code_ypx" src="code_url" width="code_width">""".replace(
                'code_url', code_url)
                
                etiqueta=etiqueta.replace('code_x', str(int(row['x'])))
                etiqueta = etiqueta.replace('code_y', str(int(row['y'])))
                etiqueta = etiqueta.replace('code_width', str(row["ancho"]))

        if (row["tipo"] == "boton_imagen"):

            #Sólo configura es estilo de la hoja la primera vez
            if (i == 1):
                if (row["nombre_visible"].lower() == "si"):
                    mensaje_css = """
                    .clicker {
                    outline:none;
                    cursor:pointer;
                    }

                    .myDiv {
                    position:absolute;
                    border: 5px outset white;
                    background-color: white;
                    text-align: center;
                    font-weight: bold;
                    }\n\n"""
                else:
                    mensaje_css = """
                    .clicker {
                    outline:none;
                    cursor:pointer;
                    }

                    .myDiv {
                    position:absolute;                    
                    text-align: center;
                    font-weight: bold;
                    }\n\n"""

            if (row["nombre_visible"].lower() == "si"):
                code_html = """<!--  code_name  -->\n<div class="clicker_code_page_code_number myDiv" style="left:code_xpx; top:code_ypx; font-size:code_letter; width:code_width; height:code_height"  tabindex="1">code_name</div>\n<div class="hiddendiv_code_page_code_number"></div> """
            else:
                code_html = """<!--  code_name  -->\n<div class="clicker_code_page_code_number myDiv" style="left:code_xpx; top:code_ypx; font-size:code_letter; width:code_width; height:code_height"  tabindex="1"></div>\n<div class="hiddendiv_code_page_code_number"></div> """    

            code_css = """/* **************** code_name ****************  */
            .hiddendiv_code_page_code_number{
            position:absolute;
            z-index: 100;
            display:none;
            width: 700px; /* Definir de acuerdo al ancho de la imagen */
            height: 700px; /* Definir de acuerdo al alto de la imagen */
            content: url("code_url");
            left:150px; 
            top:240px;
            }

            .clicker_code_page_code_number:focus + .hiddendiv_code_page_code_number{
            display:block;
            }"""
            
            etiqueta = code_html.replace('code_name', row['nombre'])
            etiqueta = etiqueta.replace('code_number', code_number)
            etiqueta = etiqueta.replace('code_x', str(row['x']))
            etiqueta = etiqueta.replace('code_y', str(row['y']))
            etiqueta = etiqueta.replace('code_page', pagina)
            etiqueta = etiqueta.replace('code_letter', str(row["letra"]))
            etiqueta = etiqueta.replace('code_width', str(row["ancho"]))
            etiqueta = etiqueta.replace('code_height', str(row["alto"]))

            estilo = code_css.replace('code_name', row['nombre'])
            estilo = estilo .replace('code_number', code_number)
            estilo = estilo .replace('code_page', pagina)
            estilo = estilo .replace('code_url', code_url)
            i += 1


        mensaje_html += etiqueta + "\r\n"
        mensaje_css += estilo + "\r\n"

    # Sólo crea el archivo si contiene datos
    f_css.write(mensaje_css)
    f_css.close()
    if (file_is_empty(name_css)):
        remove(name_css)

    f_html.write(mensaje_html)
    f_html.close()
    if (file_is_empty(name_html)):
        remove(name_html)
