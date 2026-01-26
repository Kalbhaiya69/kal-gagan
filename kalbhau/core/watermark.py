
import io
import os
import asyncio
from PIL import Image
from pypdf import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def adjust_opacity(image_path, opacity=0.3):
    """
    Reads an image, adds alpha channel if needed, and reduces opacity.
    Returns a BytesIO object containing the PNG image.
    """
    try:
        img = Image.open(image_path).convert("RGBA")

        # Split the image into channels
        r, g, b, a = img.split()

        # Apply opacity to the alpha channel
        a = a.point(lambda p: int(p * opacity))

        # Merge back
        img.putalpha(a)

        output = io.BytesIO()
        img.save(output, format='PNG')
        output.seek(0)
        return output
    except Exception as e:
        print(f"Error adjusting opacity: {e}")
        return None

def create_watermark_pdf(width, height, image_stream):
    """
    Creates a single-page PDF in memory with the image centered.
    """
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(float(width), float(height)))

    # Load image from stream
    img = ImageReader(image_stream)
    img_width, img_height = img.getSize()

    # Calculate dimensions to fit 50% of width or height, whichever is smaller relative to page
    # Let's aim for the watermark to be about 60% of the page width
    page_width = float(width)
    page_height = float(height)

    scale_factor = (page_width * 0.6) / float(img_width)
    target_width = float(img_width) * scale_factor
    target_height = float(img_height) * scale_factor

    # Center the image
    x = (page_width - target_width) / 2
    y = (page_height - target_height) / 2

    # Draw image
    # mask='auto' uses the alpha channel for transparency
    c.drawImage(img, x, y, width=target_width, height=target_height, mask='auto', preserveAspectRatio=True)
    c.save()

    packet.seek(0)
    return packet

def apply_watermark_sync(input_pdf_path, watermark_image_path):
    """
    Applies the watermark image to every page of the input PDF.
    Returns the path to the output PDF.
    """
    try:
        # Prepare the transparent image
        image_stream = adjust_opacity(watermark_image_path, opacity=0.3)
        if not image_stream:
            print("Failed to process watermark image.")
            return input_pdf_path

        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        # Iterate through all pages
        for page in reader.pages:
            # Get page dimensions
            # mediaBox is usually [x, y, width, height]
            width = page.mediabox.width
            height = page.mediabox.height

            # Create a watermark PDF for this page size
            watermark_pdf_stream = create_watermark_pdf(width, height, image_stream)
            watermark_reader = PdfReader(watermark_pdf_stream)
            watermark_page = watermark_reader.pages[0]

            # Merge watermark onto the page
            page.merge_page(watermark_page)
            writer.add_page(page)

            # Reset stream position for next iteration
            image_stream.seek(0)

        # Output file path
        base, ext = os.path.splitext(input_pdf_path)
        output_pdf_path = f"{base}_watermarked{ext}"

        with open(output_pdf_path, "wb") as f:
            writer.write(f)

        # Cleanup original file
        if os.path.exists(input_pdf_path):
            os.remove(input_pdf_path)

        return output_pdf_path

    except Exception as e:
        print(f"Error applying watermark: {e}")
        return input_pdf_path

async def apply_watermark(input_pdf_path, watermark_image_path):
    return await asyncio.to_thread(apply_watermark_sync, input_pdf_path, watermark_image_path)
