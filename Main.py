import os
from functools import partial

import openai
import streamlit as st
import newspaper
from newspaper import Config
from newspaper import Article
from openai import OpenAI
from pygooglenews import GoogleNews
import nltk

from googlenewsdecoder import gnewsdecoder

nltk.download('punkt_tab')

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10
gn = GoogleNews(lang='es', country='AR')
# No es necesario asignar la clave a la variable global de OpenAI
client = OpenAI(
    api_key="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")
articulos = []

base_url = 'https://www.infobae.com/politica/2025/02/02/los-limites-cristina-kirchner-envio-un-mensaje-a-javier-milei-tras-la-marcha-lgbt/'
article = Article(base_url, config=config)
article.download()
article.parse()
article.nlp()

def get_answer(link):
    Pregunta = "¿Cuál es la capital de Francia?"

    # Hacer la solicitud al modelo
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",  # Puedes usar "gpt-3.5-turbo" o "gpt-4"
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": Pregunta}
        ]
    )

    # Extraer y mostrar la respuesta
    print(respuesta['choices'][0]['message']['content'])

def get_titles(theme):
    global articulos
    search = gn.search(theme)
    newsitem = search['entries']
    for item in newsitem:
        # Crear un botón para cada título
        if st.button(item.title):
            # Si el botón es presionado, descargar y mostrar el artículo
            articulo = newspaper.Article(item.link,config=config)
            decoded_url = gnewsdecoder(articulo.url, interval=2)
            hashable_data = tuple(decoded_url.items())
            articulo = newspaper.Article(hashable_data.__getitem__(1)[1], config=config)
            articulo.download()
            articulo.parse()
            articulo.nlp()
            st.write(f"**Resumen:** {articulo.summary}")
            st.write(f"**Link:** {articulo.url}")



st.title("Noticias")
tema = st.text_input('Selecciona un tema', placeholder='Escribe el tema del que quieres ver noticias')
st.title("Pone un link de una noticia con una pregunta de titulo y se te respondera")
pregunta = st.text_input('Escribe un link', placeholder='?')
if tema:
    get_titles(tema)
if pregunta:
    get_answer(pregunta)