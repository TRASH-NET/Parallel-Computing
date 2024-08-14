import cv2
import time
import numpy as np


def read_image(image_path):
    
    img = cv2.imread(image_path)

    if image_path is None:
        print(f"Error: No se pudo cargar la imagen desde '{image_path}'")
        return None

    
    return img

def display_image(image, title):
    """
    Muestra una imagen manteniendo la relación de aspecto.

    :param image_path: Ruta de la imagen.
    :param title: Título de la ventana para mostrar la imagen.
    """
    max_width = 800
    max_height = 600
    
    if len(image.shape) == 3:
        height, width, _ = image.shape
    else:
        height, width = image.shape
        
    aspect_ratio = width / height

    if width > max_width or height > max_height:
        if width / max_width > height / max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        new_width = width
        new_height = height

    resized_image = cv2.resize(image, (new_width, new_height))

    cv2.imshow(title, resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def convert_to_grayscale(image):
    """
    Convierte una imagen a escala de grises a nivel de píxeles, con información de depuración.
    
    :param image: Imagen cargada (usando cv2.imread).
    :return: Imagen procesada en escala de grises.
    """
    # Verificar si la imagen ya está en escala de grises
    if len(image.shape) == 3:
        height, width, _ = image.shape
        total_pixels = height * width
        total_bytes = total_pixels

        # Crear una matriz para la imagen en escala de grises
        grayscale_image = np.zeros((height, width), dtype=np.uint8)

        print("Total Bytes: " + str(total_bytes))

        bytes_processed = 0

        start_time = time.time()
        for y in range(height):
            for x in range(width):
                
                #? Obtener los valores RGB del píxel
                b, g, r = image[y, x]
                print(image[y, x])
                
                # ? Convertir a escala de grises usando la fórmula
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                
                # Asignar el valor de gris a la imagen de salida
                grayscale_image[y, x] = gray
                bytes_processed += 1
                
                #? Imprimir progreso cada 10000 píxeles
                if bytes_processed % 10000 == 0:
                    print(f"Bytes procesados: {bytes_processed}/{total_bytes}")
        end_time = time.time()
    else:
        # ? La imagen ya está en escala de grises
        grayscale_image = image
        height, width = grayscale_image.shape
        total_pixels = height * width
        total_bytes = total_pixels
        bytes_processed = total_bytes
        start_time = time.time()
        print(f"Bytes procesados: {bytes_processed}/{total_bytes}")
        end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"Tiempo de procesamiento a nivel de píxeles: {elapsed_time:.2f} segundos")

    # ? Guardar y mostrar la imagen en escala de grises
    cv2.imwrite('grayscale_img.jpg', grayscale_image)
    display_image(grayscale_image, 'Imagen en Escala de Grises')

    return grayscale_image


if __name__ == '__main__':
    
    display_image(read_image('img2.jpg'), 'Imagen Original')
    img = read_image('img2.jpg')
    grayscale_image = convert_to_grayscale(img)
    