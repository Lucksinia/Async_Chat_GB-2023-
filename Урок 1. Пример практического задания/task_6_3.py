
from chardet import detect

#with open('test.txt', encoding='utf-8') as file:
    #for line in file.read():
        #print(line)
#file.close()

# UnicodeDecodeError: 'utf-8' codec can't decode
# byte 0xf0 in position 0: invalid continuation byte


def encoding_convert():
    """Конвертация"""
    with open('test.txt', 'rb') as f_obj:
        content_bytes = f_obj.read()
    detected = detect(content_bytes)
    print(detected)
    encoding = detected['encoding']
    content_text = content_bytes.decode(encoding)
    with open('test.txt', 'w', encoding='utf-8') as f_obj:
        f_obj.write(content_text)

encoding_convert()

# открываем файл в правильной кодировке
with open('test.txt', encoding='utf-8') as file:
    CONTENT = file.read()
print(CONTENT)
