import codecs

import textract

textract_text = textract.process(f'../../../Desktop/kplc/Interruptions - 30.06.2022.pdf')
textract_str_text = codecs.decode(textract_text)
with open(f'content.txt', 'w') as f:
    f.write(textract_str_text.strip('\n'))
