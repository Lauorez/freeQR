from flask import Flask, request, Response, make_response
import qrcode, base64, io, os, subprocess
from PIL import Image, ImageDraw
from PIL.Image import Resampling


app = Flask(__name__)

@app.route("/")
def index():
    page = open("index.html", "r")
    return page.read()


@app.route("/get_qr", methods=['POST'])
def get_qr():
    if request.method == 'POST':
        # Get the Request body as JSON
        json = request.get_json()

        # Parse JSON to variables
        url = json['url']
        version = int(json['version'])
        file = json['logo'] if 'logo' in json else None
        box_size = int(json['box_size'])
        border = int(json['border'])
        error = int(json['error'])

        # Generate QR Code
        qr = qrcode.QRCode(version=version, error_correction=error, box_size=box_size, border=border)
        qr.add_data(url)
        img = qr.make_image().get_image()
        image = Image.new("RGBA", img.size, (255, 255, 255))
        

        if file is not None:
            # Parse uploaded image base64 to PIL Image
            logo = Image.open(io.BytesIO(base64.b64decode(file)))

            # Modify the QR Code to have a background for the logo
            width, height = img.size
            logo_width, logo_height = logo.size
            Lwidth = 0
            Lheight = 0
            resolution = logo_width / logo_height
            if resolution > 1.5:
                Lwidth = int(width/2)
                Lheight = int(Lwidth*(logo_height/logo_width))
            else:
                Lwidth = int(width/5)
                Lheight = int(Lwidth*(logo_height/logo_width))
            logo.thumbnail((Lwidth, Lheight))
            logo_x, logo_y = (int(width/2) - int(Lwidth/2), int(height/2) - int(Lheight/2))
            draw = ImageDraw.Draw(img)
            draw.ellipse((logo_x - int(Lwidth/6) - int(box_size/2), logo_y - int(Lheight/6) - int(box_size/2), logo_x + Lwidth + int(Lwidth/6) + int(box_size/2), logo_y + Lheight + int(Lheight/6) + int(box_size/2)), fill="WHITE")
            image.paste(img, None)
            image.paste(logo, (logo_x, logo_y), logo if has_transparency(logo) else None)
        else:
            image.paste(img, None)
        

        # Encode generated QR Image and send response
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        resp = base64.b64encode(img_byte_arr)
        return resp

# Function to check whether the uploaded logo has an alpha channel 
def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False