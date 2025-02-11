from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
import pandas as pd

class ReportePDF:
    def __init__(self, ruta_csv, ruta_grafico1, ruta_grafico2, salida_pdf):
        self.ruta_csv = ruta_csv
        self.ruta_grafico1 = ruta_grafico1
        self.ruta_grafico2 = ruta_grafico2
        self.salida_pdf = salida_pdf

    def generar_pdf(self):
        try:
            # Leer el archivo CSV
            df = pd.read_csv(self.ruta_csv)

            # Crear un documento PDF en orientación horizontal para más espacio
            doc = SimpleDocTemplate(self.salida_pdf, pagesize=landscape(letter))
            elements = []
            styles = getSampleStyleSheet()

            # Título del documento
            title = Paragraph("Reporte de Análisis de Datos", styles["Title"])
            elements.append(title)
            elements.append(Spacer(1, 20))

            # Definir estilos de celdas para la tabla
            cell_style = ParagraphStyle(
                "CellStyle",
                fontSize=8,
                leading=10,
                alignment=1,  # Centrar el texto
                wordWrap='CJK'  # Permitir ajuste de palabras largas
            )

            # Crear encabezados y datos con ajuste de texto
            data = [[Paragraph(str(col), cell_style) for col in df.columns]]  # Encabezados
            for row in df.values.tolist():
                data.append([Paragraph(str(cell), cell_style) for cell in row])

            # Calcular ancho de columnas proporcionalmente
            col_widths = [doc.width / len(df.columns)] * len(df.columns)

            table = Table(data, colWidths=col_widths, repeatRows=1)

            # Aplicar estilos a la tabla
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20))

            # Agregar salto de página antes de los gráficos
            elements.append(PageBreak())

            # Agregar gráficos al PDF si existen
            if os.path.exists(self.ruta_grafico1):
                img1 = Image(self.ruta_grafico1, width=600, height=300)
                elements.append(img1)
                elements.append(Spacer(1, 20))

            if os.path.exists(self.ruta_grafico2):
                img2 = Image(self.ruta_grafico2, width=600, height=300)
                elements.append(img2)

            # Construir el PDF con los elementos
            doc.build(elements)
            print(f"PDF generado exitosamente en: {self.salida_pdf}")

        except Exception as e:
            print(f"Ocurrió un error al generar el PDF: {e}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(BASE_DIR, "archivocsv/palabras.csv")
    ruta_grafico1 = os.path.join(BASE_DIR, "static/images/frecuencia_palabras.png")
    ruta_grafico2 = os.path.join(BASE_DIR, "static/images/clasificaciones_palabras.png")
    salida_pdf = os.path.join(BASE_DIR, "static/reports/reporte_analisis.pdf")

    # Crear la carpeta de salida si no existe
    os.makedirs(os.path.dirname(salida_pdf), exist_ok=True)

    # Crear una instancia de ReportePDF y generar el PDF
    reporte = ReportePDF(ruta_csv, ruta_grafico1, ruta_grafico2, salida_pdf)
    reporte.generar_pdf()