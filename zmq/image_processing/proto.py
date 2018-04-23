from image_pb2 import ImageMsg

def serialize_image(img):
    # Load data...
    img = load_image(path)
    msg = ImageMsg()
    msg.original_filename = path
    msg.width = img.width
    msg.height = img.height
    msg.image_data = img.data
    return msg.SerializeToString()
