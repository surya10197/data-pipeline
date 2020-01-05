import requests
import random
from html.parser import HTMLParser
from enums.SizeUnit import SizeUnit
from utils.Utils import get_file_size
from constants.Constants import *
from config.Config import *
import logging
import threading
from datetime import datetime
from zipfile import ZipFile
# from s3upload.s3upload import UploadToS3

logging.basicConfig(format='%(asctime)s %(message)s', filename='pipeline.log', level=logging.INFO)
image_path = os.getcwd() + '/Images/'

class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        if SEARCH_STRING in data:
            data = data.split()
            global image_url
            image_url = data[-1]
            return


def downloadImage(image_path):
    try:
        with open(image_path, WRITE_MODE) as file:
            file.write(image.content)
    except Exception as e:
        logging.info('Some error occurred while dowling file: %s', image_path)
        logging.error('Some Error occurred while dowling file: %s', e)


def zip_file(file_path, image_name):
    try:
        zip_file_path = file_path + image_name.split('.')[0] + ZIP_FILE_EXTENSION
        logging.info('Zip file path:%s', zip_file_path)
        with ZipFile(zip_file_path, 'w') as zip:
            zip.write(file_path + image_name)
        return zip_file_path
    except Exception as e:
        logging.error('Some error occured while zipping: %s', e)


def start_scrap(parser, random_number):
    global image
    url = base_url + str(random_number)
    logging.info('Random url:%s', url)
    logging.info('Parsing html response to get Image url...')
    try:
        response = requests.get(url)
        parser.feed(response.text)
    except Exception as e:
        logging.error('Some error occured while parsing: %s', e)
    logging.info('Image url:%s', image_url)
    image_name = image_url.split('/')[-1]
    logging.info('Image name : %s', image_name)
    image = requests.get(image_url)
    downloadImage(image_path + image_name)
    size = get_file_size(image_path, SizeUnit.KB)
    if size > MAX_SIZE:
        save_image_to_db_path = zip_file(image_path, image_name)
    else:
        save_image_to_db_path = image_path + image_name
    # upload to s3
    # UploadToS3(save_image_to_db_path, image_name)
    # saveToDB
    # save/update cache
    # stream to webhook API
    logging.info('Size of file: %s %s', size, 'KB')


def run(parser):
    procesing_image_count = 0
    process_completed = 0
    event = threading.Event()
    while True:
        logging.info("===================================================================")
        logging.info('Processing image count= %s', procesing_image_count + 1, )
        random_number = random.randint(start, end)
        logging.info("Current Time = %s", datetime.now().strftime("%H:%M:%S"))
        thread = threading.Thread(target=start_scrap, args=(parser, random_number,))
        thread.start()
        thread.join(2)
        if thread.is_alive():
            logging.info("Killing the thread...as processing is taking more than 2 second..")
            event.set()
        else:
            logging.info('Process Completed Count=%s', process_completed + 1)
            process_completed = process_completed + 1
        procesing_image_count = procesing_image_count + 1


if __name__ == "__main__":
    logging.info('Process started...')
    parser = MyHTMLParser()
    run(parser)
    logging.info('Process Stopped...')
