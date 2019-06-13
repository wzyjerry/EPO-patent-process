import os
import argparse
from datetime import datetime
from multiprocessing import Pool
from zipfile import ZipFile

from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import BulkWriteError

from xml_parser import parse

magic_folder_name = 'DOC'
parser = argparse.ArgumentParser()
parser.add_argument('--source', help='EP patent folder', type=str)
parser.add_argument('--target', help='Unzip target folder', type=str)
args = parser.parse_args()

def fetch_db() -> Database:
    client = MongoClient('192.168.6.208', 27017)
    db = client['patent']
    db.authenticate('kegger_patent', 'jingjieweiwu2016')
    return db

def fetch_meta(db: Database) -> Collection:
    meta = db['epo_meta']
    meta.create_index([('attr.id', ASCENDING)], unique=True)
    return meta

def process(params: list) -> list:
    db = fetch_db()
    meta = fetch_meta(db)
    doc = params[0]
    target = params[1]
    count = 0
    exceptions = []
    documents = []
    print(datetime.now(), doc, 'Begin')
    for path, _, names in os.walk(doc):
        for name in names:
            if name.endswith('.zip'):
                kind = os.path.join(target, os.path.split(path)[-1])
                fzip = ZipFile(os.path.join(path, name))
                target_folder = os.path.join(kind, name[:-4])
                fzip.extractall(target_folder)
                for zipName in os.listdir(target_folder):
                    if 'TOC' not in zipName and '.xml' in zipName:
                        count += 1
                        if count % 1000 == 0:
                            print(datetime.now(), doc, count)
                        with open(os.path.join(target_folder, zipName), 'rb') as f:
                            try:
                                patent = parse(f.read())
                                documents.append(patent)
                            except Exception as e:
                                exceptions.append((zipName, e))
    print(datetime.now(), doc, count)
    print(datetime.now(), doc, 'Begin insert')
    try:
        result = meta.insert_many(documents, False)
        print(datetime.now(), doc, len(result.inserted_ids))
    except BulkWriteError as e:
        print(datetime.now(), doc, 'writeErrors', len(e.details['writeErrors']))
        exceptions.append((doc, 'writeErrors', len(e.details['writeErrors'])))
    print(datetime.now(), doc, 'End')
    exceptions.append((doc, count))
    return exceptions

def dispatcher(source: str, target: str) -> list:
    tasks = []
    for path, folders, _ in os.walk(source):
        for name in folders:
            if name == magic_folder_name:
                tasks.append(os.path.join(path, name))
    print(tasks)
    exceptions = []
    with Pool() as p:
        for exception in p.map(process, zip(tasks, [target] * len(tasks))):
            exceptions.extend(exception)
    return exceptions    

if __name__ == '__main__':
    source = args.source
    target = args.target
    for exception in dispatcher(source, target):
        print(exception)
