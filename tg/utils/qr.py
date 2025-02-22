#!/usr/bin/python
# -*- coding: UTF-8 -*-



import qrcode
import io



def encode(data, out_type="png"):
#    file = qrcode.make(text).get_image().tobytes()
    file = io.BytesIO()
#        qrcode.make(text).get_image().save(file, format="png")
    # https://github.com/lincolnloop/python-qrcode#advanced-usage
    q = qrcode.QRCode(
            border=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5
            )
    q.add_data(data)
    q.make(fit=True)
#1    q.make_image().save(file, format="png")
    q.make_image().save(file, format=out_type)
#    file.seek(0)
#    img=file.read()
    img = file.getvalue()
    file.close()
    return img


# https://github.com/dlenski/python-zxing#usage
import zxing
zxing_reader = zxing.BarCodeReader()


def decode(path):
    "path: file path"

    barcode = zxing_reader.decode(path)
#    return barcode.raw
    return barcode





