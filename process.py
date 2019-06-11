import os
from zipfile import ZipFile
from xml_parser import parse

def process(base_path: str) -> None:
    count = 0
    for path, _, names in os.walk(base_path):
        for name in names:
            if name.endswith('.zip'):
                fzip = ZipFile(os.path.join(path, name))
                for zipName in fzip.namelist():
                    if 'TOC' not in zipName and '.xml' in zipName:
                        count += 1
                        if count % 1000 == 0:
                            print(count)
                        xml = fzip.read(zipName)
                        try:
                            parse(xml)
                        except Exception as e:
                            print(zipName, e)
    print(count)

if __name__ == '__main__':
    path = 'C:/EPRTBJV1978000051001001'
    process(path)
