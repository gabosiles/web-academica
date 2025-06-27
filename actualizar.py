import os
import subprocess
import re

# Ruta carpeta de PDFS
pdf_folder = "pdfs"
pdf_files = sorted([f for f in os.listdir(pdf_folder) if f.endswith(".pdf")])

# Generar el HTML de la lista
pdf_list_html = "\n".join([
    f'      <li><a href="{pdf_folder}/{pdf}" download>{pdf}</a></li>' for pdf in pdf_files
])

# Reemplazar el bloque <ul>...</ul> en index.html
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

start_tag = "<!-- START AUTO PDF LIST -->"
end_tag = "<!-- END AUTO PDF LIST -->"

new_block = f"{start_tag}\n    <ul>\n{pdf_list_html}\n    </ul>\n  {end_tag}"

updated_content = re.sub(f"{start_tag}.*?{end_tag}", new_block, content, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(updated_content)

# Hacer commit y push automático
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Actualización automática de PDFs"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("✅ Cambios subidos a GitHub correctamente.")
except Exception as e:
    print("⚠️ Hubo un error al hacer push:", e)