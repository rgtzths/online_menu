import qrcode
from qrcode.image.styledpil import StyledPilImage
import PIL
from PIL import Image, ImageDraw
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, GappedSquareModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask

def style_inner_eyes(img):
  img_size = img.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((60, 60, 90, 90), fill=255) #top left eye
  draw.rectangle((img_size-90, 60, img_size-60, 90), fill=255) #top right eye
  draw.rectangle((60, img_size-90, 90, img_size-60), fill=255) #bottom left eye
  return mask

def style_outer_eyes(img):
  img_size = img.size[0]
  eye_size = 70 #default
  quiet_zone = 40 #default
  mask = Image.new('L', img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((40, 40, 110, 110), fill=255) #top left eye
  draw.rectangle((img_size-110, 40, img_size-40, 110), fill=255) #top right eye
  draw.rectangle((40, img_size-110, 110, img_size-40), fill=255) #bottom left eye
  draw.rectangle((60, 60, 90, 90), fill=0) #top left eye
  draw.rectangle((img_size-90, 60, img_size-60, 90), fill=0) #top right eye
  draw.rectangle((60, img_size-90, 90, img_size-60), fill=0) #bottom left eye  
  return mask  

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

url='https://rgtzths.github.io/online_menu/'
logo="images/logo.jpg"
rounded_logo = "images/rounded_logo.png"
qr_code='images/qr_code_black.png'
color = False


im = Image.open(logo)
im = add_corners(im, 50)
im.save(rounded_logo)

if not hasattr(PIL.Image, 'Resampling'):
  PIL.Image.Resampling = PIL.Image

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(url)



if color:

  qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=RoundedModuleDrawer(),
                            color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(218, 174, 103)))

  qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=RoundedModuleDrawer(),
                            color_mask=SolidFillColorMask(front_color=(88, 63, 58)))   

  qr_img = qr.make_image(image_factory=StyledPilImage,
                        module_drawer=RoundedModuleDrawer(),
                        color_mask=SolidFillColorMask(front_color=(88, 63, 58)),
                        embeded_image_path=rounded_logo)
  qr_img.save(qr_code)


  eye_size = 50  # Adjust this size as needed
  eye_radius = 10  # Radius for rounded corners
  eye_color = (0, 0, 0, 255)  # Color of the eyes


  inner_eye_mask = style_inner_eyes(qr_img)
  outer_eye_mask = style_outer_eyes(qr_img)
  intermediate_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)
  final_image = Image.composite(qr_outer_eyes_img, intermediate_img, outer_eye_mask)
  final_image.save(qr_code)
else:
  qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=RoundedModuleDrawer(),
                            color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 0, 0)))

  qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                            eye_drawer=RoundedModuleDrawer(),
                            color_mask=SolidFillColorMask(front_color=(0, 0, 0)))
     
  qr_img = qr.make_image(image_factory=StyledPilImage,
                        module_drawer=GappedSquareModuleDrawer(),
                        color_mask=SolidFillColorMask(front_color=(0, 0, 0)),
                        embeded_image_path=rounded_logo)
  qr_img.save(qr_code)


  eye_size = 50  # Adjust this size as needed
  eye_radius = 10  # Radius for rounded corners
  eye_color = (0, 0, 0, 255)  # Color of the eyes


  inner_eye_mask = style_inner_eyes(qr_img)
  outer_eye_mask = style_outer_eyes(qr_img)
  intermediate_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)
  final_image = Image.composite(qr_outer_eyes_img, intermediate_img, outer_eye_mask)
  final_image.save(qr_code)