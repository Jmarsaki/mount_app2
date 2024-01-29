from flask import Flask, render_template_string
import urllib.request
import urllib.parse
import re

app = Flask(__name__)

@app.route('/')
def index():
    # Codificar la URL
    url = "https://en.wikipedia.org/wiki/Áhkká"
    encoded_url = urllib.parse.quote(url, safe=':/')

    # Descargar el contenido de la página web
    response = urllib.request.urlopen(encoded_url)
    content = response.read().decode('utf-8')

    # Extraer la información de la infobox
    infobox_regex = r'<table class="infobox vcard".*?</table>'
    infobox_data = re.findall(infobox_regex, content, re.DOTALL)

    # Procesar y limpiar la información
    processed_data = ""
    for data in infobox_data:
        data = re.sub(r'<[^>]*>', '', data)  # Eliminar las etiquetas HTML
        data = re.sub(r'&#160;|&#8201;', ' ', data)  # Reemplazar entidades HTML por espacios
        data = re.sub(r'\n+', '\n', data)  # Eliminar líneas en blanco repetidas
        data = re.sub(r'\t+', '\t', data)  # Eliminar tabulaciones repetidas
        data = re.sub(r'(^|\n)\t*$', '', data)  # Eliminar líneas en blanco al final
        processed_data += data.strip() + "\n\n"

    return render_template_string('<pre>{{ data }}</pre>', data=processed_data)

if __name__ == '__main__':
    app.run(debug=True)


    