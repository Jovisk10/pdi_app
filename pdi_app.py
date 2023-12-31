from functions.functions_img import brighten_img, threshold_img, contrast_img, sobel_img, canny_img, histogram_img, histogram_fn, channel_rgb, channel_ycbcr
from functions.functions_webcam import threshold_webcam, brighten_webcam, contrast_webcam, sobel_webcam, canny_webcam, channel_rgb_w, channel_ycbcr_w, gray_scale, img_webcam
import streamlit as st
from PIL import Image
import numpy as np
import cv2 as cv
import base64


st.set_page_config(layout="wide", page_title='PDI App') #Deixando a página no modo wide por default

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_bg = get_img_as_base64("./style/background.png")
img_bg_sb = get_img_as_base64("./style/bg_slide.png")

#background-image: url("https://images.pexels.com/photos/3648850/pexels-photo-3648850.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"); 
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("data:image/png;base64,{img_bg}"); 
background-size: cover;
}}

[data-testid="stSidebar"] {{
background-image: url("data:image/png;base64,{img_bg_sb}"); 
background-size: cover;
}}

[data-testid="stFileUploadDropzone"] {{
background-size: cover;
}}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


def main_loop():
    st.title("PDI App")
    st.subheader("This app allows you to play with Image filters!")

    bar = st.sidebar
    bar.title("PDI App")
    entry_option = bar.selectbox('Selecione o formato da entrada:', ['Upload da Imagem', 'Webcam'])
    option = bar.selectbox('Selecione a opção desejada:', ['Limiarização', 'Brilho', 'Contraste', 'Sobel', 'Canny', 'Visualizar'])
    #scale = bar.radio('Selecione a escala:', ['Escala de Cinza', 'Escala de Cor'])
    bar.markdown(''' ### Parâmetros: ''')
    vis = img2 = img3 = img4 = text_frame3 = text_frame4 = ''

    # match entry_option:
    if entry_option == 'Upload da Imagem':
            
            image = st.file_uploader("Upload Your Image", type=['jpg', 'png', 'jpeg','tif'], label_visibility='collapsed')

            if not image: 
                return None
        
            else: 
                original_image = Image.open(image)
                original_image = np.array(original_image)
                
                try:
                    img = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
                except:
                    img = original_image

            if option == 'Limiarização':

                threshold_value = bar.slider("Limiarização", min_value=-1, max_value=255, value=-1)
                text_frame2 = 'Imagem binarizada'
                img2 = threshold_img(img, threshold_value)

            elif option == 'Brilho':
                brightness_value = bar.slider("Brilho", min_value=-1, max_value=255, value=0)
                text_frame2 = 'Imagem de saída'
                text_frame3 = 'Histograma da imagem de entrada'
                text_frame4 = 'Histograma da imagem de saída'
                img2 = brighten_img(img, brightness_value)

            elif option == 'Contraste':
                contrast_value = bar.slider("Contraste", min_value=0.0, max_value=2.0, value=1.0)
                text_frame2 = 'Imagem de saída'
                text_frame3 = 'Histograma da imagem de entrada'
                text_frame4 = 'Histograma da imagem de saída'
                img2 = contrast_img(img, contrast_value)

            elif option == 'Sobel':
                sobel_value_1 = bar.slider("Sobel X", min_value=1, max_value=2, value=1)
                sobel_value_2 = bar.slider("Sobel Y", min_value=1, max_value=2, value=1)

                text_frame2 = 'Imagem com sobel nas coordenadas xy'
                img2 = sobel_img(img, sobel_value_1, sobel_value_2, 'xy')

                text_frame3 = 'Imagem com sobel nas coordenadas x'
                img3 = sobel_img(img, sobel_value_1, sobel_value_2, 'x')

                text_frame4 = 'Imagem com sobel nas coordenadas y'
                img4 = sobel_img(img, sobel_value_1, sobel_value_2, 'y') 

            elif option == 'Canny':
                canny_value_1 = bar.slider("Limiar mínimo", min_value=0, max_value=255, value=0)
                canny_value_2 = bar.slider("Limiar máximo", min_value=0, max_value=255, value=0)
                text_frame2 = 'Imagem de saída'
                img2 = canny_img(img, canny_value_1, canny_value_2)

            elif option == 'Visualizar':
                    
                vis = bar.selectbox('Selecione o formato da conversão:', ['Escala de Cinza','RGB', 'YCBCR'])

                try:
                    img = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
                    img = original_image

                except:
                    st.error('Opção "Visualizar" não está disponível para imagens em escala de cinzas :(', icon="🚨")
                    vis = img  = None

                if vis == 'Escala de Cinza':

                    text_frame2 = 'Imagem em escala de cinza' 
                    img2 = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)

                elif vis == 'RGB':
                        
                    text_frame2 = "Componente Vermelha (R)"
                    img2 = channel_rgb(original_image, 'r')
                    text_frame3 = "Componente Verde (G)"
                    img3 = channel_rgb(original_image, 'g')
                    text_frame4 = "Componente Azul (B)"
                    img4 = channel_rgb(original_image, 'b')

                elif vis == 'YCBCR':

                    text_frame2 = "Componente Y"
                    img2 = channel_ycbcr(original_image, 'y')
                    text_frame3 = "Componente Cb"
                    img3 = channel_ycbcr(original_image, 'cb')
                    text_frame4 = "Componente Cr"
                    img4 = channel_ycbcr(original_image, 'cr')

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            with col1: # Coluna da img de entrada
                st.text("Imagem de entrada")
                st.image([img], width=550)

            with col2: # Coluna da img de entrada
                st.text(f'{text_frame2}')
                st.image([img2], width=550)

            with col3: # Coluna da img de entrada
                st.text(f'{text_frame3}')

                if option == 'Brilho' or option == 'Contraste':
                    histogram_fn(img)
                    
                elif option == 'Sobel':
                    st.image(img3, width=550)

                if vis == 'RGB' or vis == 'YCBCR':
                    st.image([img3], width=550)
                    

            with col4: # Coluna da img de entrada
                
                st.text(f'{text_frame4}')

                if option == 'Brilho' or option ==  'Contraste':
                    histogram_fn(img2)
                    
                elif option == 'Sobel':
                    st.image(img4, width=550)

                if vis == 'RGB' or vis == 'YCBCR':
                    st.image([img4], width=550)

        # case 'Webcam':
    elif entry_option == 'Webcam':

            vis = img3 = img4 = None
            image = st.image([])
            camera = cv.VideoCapture(0)

            text_frame2 = text_frame3 = text_frame4 = ''

            #Estrutura da imagem dinâmica
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            with col1:
                st.text("Imagem de entrada")
                frame = st.image([])
            with col2:
                text_frame2 = st.text("")
                frame2 = st.image([])
            with col3:
                text_frame3 = st.text("")
                frame3 = st.image([])
            with col4:
                text_frame4 = st.text("")
                frame4 = st.image([])

            if option == 'Limiarização':
                    
                threshold_value = bar.slider("Limiarização", min_value=-1, max_value=255, value=-1)
                while 'True' == 'True':
                    img_webcam(camera, frame, 'gray')
                    text_frame2.text("Imagem binarizada")
                    threshold_webcam(camera, frame2, threshold_value)

            elif option == 'Brilho':
                brightness_value = bar.slider("Brilho", min_value=0, max_value=255, value=0)
                
                while 'True' == 'True':
                    img_webcam(camera, frame, 'gray')
                    text_frame2.text("Imagem Saída")
                    brighten_webcam(camera, frame2, brightness_value)

            elif option == 'Contraste':
                contrast_value = bar.slider("Contraste", min_value=0.0, max_value=2.0, value=1.0)

                while 'True' == 'True':
                    img_webcam(camera, frame, 'gray')
                    text_frame2.text("Imagem Saída")
                    contrast_webcam(camera, frame2, contrast_value)

            elif option == 'Sobel':
                sobel_value_1 = bar.slider("Sobel X", min_value=0, max_value=2, value=1)
                sobel_value_2 = bar.slider("Sobel Y", min_value=0, max_value=2, value=1)
                
                while 'True' == 'True':
                    img_webcam(camera, frame, 'gray')

                    text_frame2.text("Imagem com operador Sobel em XY")
                    sobel_webcam(camera, frame2, sobel_value_1, sobel_value_2,'xy')

                    text_frame3.text("Imagem com operador Sobel em X")
                    sobel_webcam(camera, frame3, sobel_value_1, sobel_value_2, 'x')

                    text_frame4.text("Imagem com operador Sobel em Y")
                    sobel_webcam(camera, frame4, sobel_value_1, sobel_value_2, 'y')

            elif option == 'Canny':
                canny_value_1 = bar.slider("Limiar mínimo", min_value=0, max_value=255, value=0)
                canny_value_2 = bar.slider("Limiar máximo", min_value=0, max_value=255, value=0)
                
                while 'True' == 'True':
                    img_webcam(camera, frame, 'gray')
                    text_frame2.text("Imagem Saída")
                    canny_webcam(camera, frame2, canny_value_1, canny_value_2)

            elif option == 'Visualizar':
                    
                    vis = bar.selectbox('Selecione o formato de visualização:', ['Escala de Cinza','RGB', 'YCBCR'])
                    sobel_value_2 = canny_value_2 = bar.image([])
                    
                    if vis == 'Escala de Cinza':

                        while 'True' == 'True':
                            img_webcam(camera, frame, 'color')
                            text_frame2.text("Imagem em escala de cinza")
                            gray_scale(camera, frame2)

                    elif vis == 'RGB':
                        while 'True' == 'True':
                            img_webcam(camera, frame, 'color')
                            text_frame2.text("Componente Vermelha (R)")
                            channel_rgb_w(camera, frame2, 'r')
                            text_frame3.text("Componente Verde (G)")
                            channel_rgb_w(camera, frame3, 'g')
                            text_frame4.text("Componente Azul (B)")
                            channel_rgb_w(camera, frame4, 'b')

                    elif vis == 'YCBCR':
                        while 'True' == 'True':
                            img_webcam(camera, frame, 'color')
                            text_frame2.text("Componente Y")
                            channel_ycbcr_w(camera, frame2, 'y')
                            text_frame3.text("Componente Cb")
                            channel_ycbcr_w(camera, frame3, 'cb')
                            text_frame4.text("Componente Cr")
                            channel_ycbcr_w(camera, frame4, 'cr')

if __name__ == '__main__':
    main_loop()
