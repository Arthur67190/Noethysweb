from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

def add_watermark(document, text: str):
    pdf_reader = PdfReader(document.path)
    
    width = float(pdf_reader.pages[0].mediabox.width)
    height = float(pdf_reader.pages[0].mediabox.height)
    
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    
    text_width = can.stringWidth(text, "Helvetica", 20)
    x = (width - text_width) / 2
    y = height / 4
    
    x_center = width / 3
    y_center = height / 4
    
    print("width", width, "height", height,"text_width", text_width, "x", x, "y", y, "x_center", x_center, "y_center", y_center)
    
    can.saveState()
    
    can.translate(x_center, y_center)
    
    can.setFont("Helvetica", 20)
    can.rotate(45)
    can.setFillAlpha(0.3)
    can.drawString(0,0, text)
    can.restoreState()
    can.save()

    packet.seek(0)
    
    pdf_writer = PdfWriter()

    watermark_pdf = PdfReader(packet)
    watermark_page = watermark_pdf.get_page(0)

    for i in range(pdf_reader.get_num_pages()):
        page = pdf_reader.get_page(i)
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    pdf_writer.write(document.path)
