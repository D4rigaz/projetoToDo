from PIL import Image, ImageDraw, ImageFont
import datetime
import os

def generate_evidence(test_name, status, version):
    # Dimensões e cores do relatório visual do QA
    width, height = 800, 400
    bgcolor = (0, 0, 0) # Preto profundo
    accent_color = (0, 102, 255) # Azul Check-It
    success_color = (0, 255, 127) # Verde QA
    
    image = Image.new("RGB", (width, height), color=bgcolor)
    draw = ImageDraw.Draw(image)
    
    # Textos do Relatório
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = "CHECK-IT: RELATÓRIO DE EVIDÊNCIA QA"
    body_status = f"STATUS: {status}"
    body_test = f"TESTE: {test_name}"
    body_ver = f"VERSÃO: {version}"
    body_time = f"DATA/HORA: {timestamp}"
    
    # Desenhando elementos visuais básicos
    draw.rectangle([20, 20, 780, 380], outline=accent_color, width=5)
    draw.text((50, 50), header, fill=accent_color)
    draw.text((50, 120), body_status, fill=success_color)
    draw.text((50, 170), body_test, fill=(255, 255, 255))
    draw.text((50, 220), body_ver, fill=(255, 255, 255))
    draw.text((50, 320), body_time, fill=(150, 150, 150))
    
    # Salvar a evidência em JPG
    output_dir = "evidencias"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filename = f"evidencia_sucesso_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
    filepath = os.path.join(output_dir, filename)
    image.save(filepath, "JPEG")
    return filepath

if __name__ == "__main__":
    path = generate_evidence("Interface Estável", "SUCESSO", "v1.5_Final")
    print(f"Evidência JPG gerada em: {path}")
