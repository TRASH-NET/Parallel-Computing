import subprocess
import platform
from PIL import Image, ImageFilter
import numpy as np
from datetime import datetime
from threading import Thread
import time
import os

def read_img(path):
    img = Image.open(path)
    if img is None:
        raise ValueError("Image not found")
    return img

def apply_gaussian_blur(img, start_row, end_row, radius, result, index):
    """
    Apply a Gaussian blur filter to a cropped section of an image.

    Args:
        img (Image.Image): The image to be processed.
        start_row (int): The starting row of the section to crop (top boundary).
        end_row (int): The ending row of the section to crop (bottom boundary).
        radius (float): The radius of the Gaussian blur.
        result (list): A list where the blurred image will be stored.
        index (int): The index in the result list where the blurred image will be stored.

    Returns:
        None
    """
    cropped_img = img.crop((0, start_row, img.width, end_row))
    result[index] = cropped_img.filter(ImageFilter.GaussianBlur(radius))

def resize_image(img, size):
    return img.resize(size, Image.Resampling.LANCZOS)

def compress_image(img_path, max_size=(400, 200), quality=85):
    with Image.open(img_path) as img:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        compressed_path = "compressed_" + os.path.basename(img_path)
        img.save(compressed_path, "JPEG", quality=quality)
    return compressed_path

def get_image_info(img_path):
    img = Image.open(img_path)
    img_size = os.path.getsize(img_path)
    img_dimensions = img.size
    return img_size, img_dimensions

def serial_image_blur(img, radius=30):  
    height = img.height
    result = [None]
    apply_gaussian_blur(img, 0, height, radius, result, 0)
    return result[0]

def parallel_image_blur(img, radius=30):
    """
    Applies Gaussian blur to an image in parallel using multiple threads.

    The image is divided into segments based on the number of available CPU cores.
    Each segment is processed by a separate thread to apply the Gaussian blur.

    Args:
        img (PIL.Image.Image): The image to be processed.
        radius (float, optional): The radius of the Gaussian blur. Defaults to 20.

    Returns:
        PIL.Image.Image: A new image with Gaussian blur applied in parallel.

    Raises:
        ValueError: If an error occurs during image processing.
    """
    
    num_cores = os.cpu_count()
    height = img.height
    chunk_size = height // num_cores
    threads = []
    results = [None] * num_cores

    for i in range(num_cores):
        start_row = i * chunk_size
        end_row = height if i == num_cores - 1 else (i + 1) * chunk_size
        thread = Thread(target=apply_gaussian_blur, args=(img, start_row, end_row, radius, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    blurred_img = Image.new('RGB', img.size)
    current_height = 0
    for part in results:
        blurred_img.paste(part, (0, current_height))
        current_height += part.height

    return blurred_img


def perform_tests(img_path, sizes, radius=30):
    img = read_img(img_path)
    results = []
    
    for size in sizes:
        resized_img = resize_image(img, size)
        
        serial_path = f"serial_blur_{size[0]}x{size[1]}.jpg"
        parallel_path = f"parallel_blur_{size[0]}x{size[1]}.jpg"
        
        print(f"Testing with size: {size}")
        
        start_time = time.time()
        serial_blurred_img = serial_image_blur(resized_img, radius)
        end_time = time.time()
        serial_time = end_time - start_time
        serial_blurred_img.save(serial_path)
        
        start_time = time.time()
        parallel_blurred_img = parallel_image_blur(resized_img, radius)
        end_time = time.time()
        parallel_time = end_time - start_time
        parallel_blurred_img.save(parallel_path)
        
        results.append({
            'size': size,
            'serial_time': serial_time,
            'parallel_time': parallel_time,
            'serial_path': serial_path,
            'parallel_path': parallel_path
        })
    
    return results

def generate_report(img_path, results):
    
    date = datetime.now().strftime("%Y-%m-%d")
    img_size, img_dimensions = get_image_info(img_path)
    compressed_image_path = compress_image(img_path)
    
    img_size_kb = img_size / 1024
    img_info = f"Size: {img_size_kb:.2f} KB, Dimensions: {img_dimensions[0]}x{img_dimensions[1]}"

    sizes = []
    serial_times = []
    parallel_times = []
    serial_paths = []
    parallel_paths = []
    
    for result in results:
        sizes.append(f"{result['size'][0]}x{result['size'][1]}")
        serial_times.append(f"{result['serial_time']:.4f}")
        parallel_times.append(f"{result['parallel_time']:.4f}")
        serial_paths.append(result['serial_path'])
        parallel_paths.append(result['parallel_path'])
    
    table_data = np.array([sizes, serial_times, parallel_times, serial_paths, parallel_paths]).T
    

    qmd_content = f"""
---
title: "Analysis of Serial VS Parallel Image Processing Using Threaded Shared Memory."
author: "Emmanuel Silva Diaz"
date: {date}
format: pdf
jupyter: python3
---

# Introduction

Image processing is a fundamental task in a variety of applications, from computer vision to graphics editing. In this report, two approaches to image processing are explored: serial processing and parallel processing using threads. The comparison is made using a Gaussian blur effect applied to images of different sizes. The objective is to analyze the performance and efficiency of each method, as well as the challenges associated with the use of shared memory in a multithreaded environment.

# Objective

The objective of this report is to evaluate and compare the performance of serial versus parallel image processing using Python threads. It is intended to determine the differences in execution time and efficiency between the two approaches when applying a Gaussian blur effect to images of different sizes. In addition, the challenges associated with shared memory management in parallel processing will be examined and possible solutions to improve performance will be proposed.

# Metodology

The following methodology was used to carry out this analysis:

1. **Image Selection**: A high resolution image was chosen for testing. The image was compressed and resized to fit different sizes.

2. **Implementation of Processing Functions**:
   - **read_img()**: A function was implemented to open and return an image from a specified file path.
   ```python
    
    def read_img(path):
    img = Image.open(path)
    if img is None:
        raise ValueError("Image not found")
    return img
    
   ```

   - **apply_gaussian_blur**: A function was developed that applies a Gaussian blur filter to a cropped section of an image.
   ```python
   def apply_gaussian_blur(img, start_row, end_row, radius, result, index):
    
    # Apply a Gaussian blur filter to a cropped section of an image.

    # Args:
        # img (Image.Image): The image to be processed.
        # start_row (int): The starting row of the section to crop (top boundary).
        # end_row (int): The ending row of the section to crop (bottom boundary).
        # radius (float): The radius of the Gaussian blur.
        # result (list): A list where the blurred image will be stored.
        # index (int): List where the blurred image will be stored.

    # Returns:
        # None

    cropped_img = img.crop((0, start_row, img.width, end_row))
    result[index] = cropped_img.filter(ImageFilter.GaussianBlur(radius))
   ```

    - **resize_image()**: is responsible for resizing an image to a specific size.
    ```python
    def resize_image(img, size):
        return img.resize(size, Image.Resampling.LANCZOS)
    ```
    - **compress_image()**: Compresses an image by resizing it to a specified maximum size and adjusting its quality to reduce the file size, in order to render it in the report.
    ```python
    def compress_image(img_path, max_size=(400, 200), quality=85):
        with Image.open(img_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            compressed_path = "compressed_" + os.path.basename(img_path)
            img.save(compressed_path, "JPEG", quality=quality)
        return compressed_path
    ```

    - **get_image_info()**: Obtains detailed information from an image.
    ```python
    def get_image_info(img_path):
        img = Image.open(img_path)
        img_size = os.path.getsize(img_path)
        img_dimensions = img.size
        return img_size, img_dimensions
    ```


    - **serial_image_blur()**: Applies a Gaussian blur to an image in a single step, sequentially.
    ```python
    def serial_image_blur(img, radius=20):  
        height = img.height
        result = [None]
        apply_gaussian_blur(img, 0, height, radius, result, 0)
        return result[0]
    ```
    - **parallel_image_blur()**: Applies a Gaussian blur to an image in parallel using multiple threads .
    ```python
    def parallel_image_blur(img, radius=20):
    # Applies Gaussian blur to an image in parallel using multiple threads.
    # The image is divided into segments based on the number of available CPU cores.
    # Each segment is processed by a separate thread to apply the Gaussian blur.
    # Args:
        # img (PIL.Image.Image): The image to be processed.
        # radius (float, optional): The radius of the Gaussian blur. Defaults to 20.

    # Returns:
        # PIL.Image.Image: A new image with Gaussian blur applied in parallel.

    # Raises:
        # ValueError: If an error occurs during image processing.

        
        num_cores = os.cpu_count()
        height = img.height
        chunk_size = height // num_cores
        threads = []
        results = [None] * num_cores

        for i in range(num_cores):
            start_row = i * chunk_size
            end_row = height if i == num_cores - 1 else (i + 1) * chunk_size
            thread = Thread(target=apply_gaussian_blur, args=(img, start_row, end_row, radius, results, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        blurred_img = Image.new('RGB', img.size)
        current_height = 0
        for part in results:
            blurred_img.paste(part, (0, current_height))
            current_height += part.height

        return blurred_img
    ```

   - **perform_tests()**: Prepares tests to compare the processing time between serial and parallel Gaussian blur on images of different sizes.
    ```python
    def perform_tests(img_path, sizes, radius=20):
    
        img = read_img(img_path)

        for size in sizes:
            resized_img = resize_image(img, size)
            
            start_time = time.time()
            serial_blurred_img = serial_image_blur(resized_img, radius)
            end_time = time.time()
            serial_time = end_time - start_time
            
            start_time = time.time()
            parallel_blurred_img = parallel_image_blur(resized_img, radius)
            end_time = time.time()
            parallel_time = end_time - start_time
    
    ```
# Test Results: 

The tests were executed with images of different sizes to compare the processing time between serial and parallel Gaussian blur. The results are summarized in the table below:

| Size (Width x Height) | Serial Processing Time (seconds) | Parallel Processing Time (seconds) | Serial Blurred Image | Parallel Blurred Image |
|-----------------------|---------------------------------|-----------------------------------|----------------------|------------------------|
"""

    # Append each row of the table to the Markdown content
    for row in table_data:
        size, serial_time, parallel_time, serial_path, parallel_path = row
        qmd_content += f"| {size} | {serial_time} | {parallel_time} | ![Serial]({serial_path}) | ![Parallel]({parallel_path}) |\n"

    qmd_content += """

# Analysis and Discussion

The processing time for applying a Gaussian blur filter varies significantly with image size. As the image size increases, the processing time also increases. This is because the algorithm must perform operations on a larger number of pixels. In serial processing, the entire image is processed at once, which can result in very long processing times for large images.

1. **Serial Processing**: 
In serial processing, the entire image is processed sequentially. This approach can be inefficient for large images due to the amount of data that must be handled and processed in a single step. However, for smaller images, serial processing may be a more suitable option. This is because the Gaussian blur function, which performs a radial blur, is smoothly applied to the entire image. Since the blur is evenly distributed from the center to the edges, there is no distortion in the image. In contrast, when using parallel processing and dividing the image into rectangular sections, the radial blur effect may not align perfectly when recombining the sections, which may result in visible distortion at the edges of the sections.

2. **Parallel Processing**: 
El procesamiento en paralelo distribuye el trabajo entre múltiples hilos, cada uno encargado de procesar una sección diferente de la imagen simultáneamente. Este enfoque es especialmente beneficioso para imágenes grandes, ya que permite reducir el tiempo total de procesamiento al dividir la carga de trabajo. No obstante, es crucial manejar adecuadamente la recomposición de la imagen para evitar distorsiones. La implementación de múltiples hilos permite procesar diferentes segmentos de la imagen al mismo tiempo, lo que resulta en una disminución significativa del tiempo de procesamiento en comparación con el enfoque secuencial. Sin embargo, es importante considerar las implicaciones del efecto radial del desenfoque y aplicar correcciones si es necesario para mantener la calidad de la imagen final.


# Conclusion

1. **Effectiveness of Serial Processing**:
Serial processing, where the entire image is processed at once, proves to be efficient for small images. The Gaussian blur effect, applied radially from the center, blends smoothly across the image, avoiding noticeable distortions. This approach works well due to the uniform nature of the blur effect. However, as the image size increases, the processing time grows substantially, making this method less suitable for large images, where the computational load becomes a bottleneck.

2. **Advantages of Parallel Processing**:
Parallel processing demonstrates significant advantages, especially with large images. By distributing the image into smaller segments and processing each segment simultaneously with multiple threads, the total processing time is substantially reduced. This method takes advantage of multi-core processors to handle the workload more efficiently. Despite these advantages, careful management of image recomposition is necessary to prevent artifacts and ensure that the radial blur effect remains consistent throughout the entire image.

3. **Challenges and Solutions**:
    - **Handling Large Images**: Processing very large images can lead to excessive memory usage and increase the risk of errors such as `DecompressionBombError`. To address these issues, resizing and compressing images prior to processing can help mitigate memory concerns and reduce the risk of errors.
    - **Image Distortion in Parallel Processing**: The radial nature of Gaussian blur can lead to visible distortions when images are split into rectangular sections and then recombined. This problem can be partially mitigated by using overlapping techniques or by refining the blur effect at the recombination stage to ensure consistency.

   """
    with open("informe.qmd", "w", encoding="utf-8") as file:
        file.write(qmd_content)

    subprocess.run(["quarto", "render", "informe.qmd", "--to", "pdf"])

    pdf_file = "informe.pdf"
    if platform.system() == "Darwin":
        subprocess.run(["open", pdf_file])
    elif platform.system() == "Windows":
        subprocess.run(["start", pdf_file], shell=True)
    else:
        subprocess.run(["xdg-open", pdf_file])

if __name__ == "__main__":


    Image.MAX_IMAGE_PIXELS = None

    img_path = "img.jpg"
    img = read_img(img_path)

    test_sizes = [
        (600, 400),
        (1200, 800),
        (2400, 1600),
        (3000, 2000),
        (img.width, img.height)
    ]
    results = perform_tests(img_path, test_sizes)
    

    generate_report(img_path, results)









