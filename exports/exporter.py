from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def export_txt(path, original, simplified, steps, minterms, verified):
    p = Path(path)
    with p.open("w", encoding="utf-8") as f:
        f.write("CALCULADORA DE SIMPLIFICACIÓN DE CIRCUITOS LÓGICOS\n\n")
        f.write(f"FUNCIÓN ORIGINAL\n{original}\n\n")
        f.write("PROCEDIMIENTO\n")
        for name, expr, law in steps:
            f.write(f"{name}: {expr}\n{law}\n\n")
        f.write(f"FUNCIÓN SIMPLIFICADA\n{simplified}\n\n")
        f.write(f"MINTERMS: {minterms}\n")
        f.write(f"VERIFICACIÓN DE EQUIVALENCIA: {'CORRECTA' if verified else 'INCORRECTA'}\n")

def export_pdf(path, original, simplified, steps, minterms, verified):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(path), pagesize=letter)
    story = [
        Paragraph("Calculadora de Simplificación de Circuitos Lógicos", styles["Title"]),
        Spacer(1, 12),
        Paragraph("<b>Función original</b>", styles["Heading2"]),
        Paragraph(str(original), styles["BodyText"]),
        Spacer(1, 10),
        Paragraph("<b>Procedimiento</b>", styles["Heading2"]),
    ]
    for name, expr, law in steps:
        story.append(Paragraph(f"<b>{name}</b>: {expr}", styles["BodyText"]))
        story.append(Paragraph(law, styles["BodyText"]))
        story.append(Spacer(1, 6))
    story.extend([
        Paragraph("<b>Función simplificada</b>", styles["Heading2"]),
        Paragraph(str(simplified), styles["BodyText"]),
        Spacer(1, 8),
        Paragraph(f"<b>Minterms:</b> {minterms}", styles["BodyText"]),
        Paragraph(f"<b>Verificación:</b> {'Funciones equivalentes' if verified else 'No equivalentes'}", styles["BodyText"]),
    ])
    doc.build(story)
