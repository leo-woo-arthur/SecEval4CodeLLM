from bs4 import BeautifulSoup
from utils.logger_factory import logger


def fetch_file_content(p_file_path, p_default_value=""):
    try:
        with open(p_file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"!!! File not found: {p_file_path}")
        return p_default_value


def fetch_xml_content(p_xml_path):
    return BeautifulSoup(fetch_file_content(p_xml_path), 'lxml')



