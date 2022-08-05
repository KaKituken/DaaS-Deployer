import pandas as pd
import zipfile

IMG = ['jpg', 'png']
TXT = ['txt', 'json']


def preprocess_zip(zip):
    res = []
    z = zipfile.ZipFile(zip, "r")
    for i in z.namelist():
        data = z.read(i)
        _, ext = i.split('.')
        print(ext)
        if ext in IMG:
            res.append(preprocess_img(data))
        elif ext in TXT:
            res.append(preprocess_txt(data, ext))
        else:
            pass
    return res

def preprocess_csv(csv):
    return pd.read_csv(csv)

def preprocess_img(img):
    return 'img'

def preprocess_txt(txt, ext):
    if ext == 'txt':
        return 'txt'
    elif ext == 'json':
        pass
    else:
        return ""
