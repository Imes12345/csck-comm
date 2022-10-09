import pickle
import xml
from datetime import datetime
import json
import dicttoxml as dicttoxml
import xmltodict as xmltodict
from app_config import AppConfig
from csck_exceptions import CsckException


class DataService:
    @staticmethod
    def read_file_as_bytes(path):
        absolute_path = path.abspath(path)
        file_exists = path.exists(absolute_path)
        if not file_exists:
            raise CsckException(f"File {absolute_path} does not exist")
        file = open(path, "rb")
        byte_data = file.read()
        file.close()
        return byte_data

    @staticmethod
    def get_sample_dictionary():
        return {
            'name': 'Betelgeuse',
            'mtype': 'M1-2',
            'diameter': 0.047,
            'distance': 548,
            'constellation': 'Orion',
            'is-home': True,
            'local_time': datetime.now()
        }

    @staticmethod
    def serialize(obj, data_type:AppConfig.DictionarySerializationMethod):
        if data_type == AppConfig.DictionarySerializationMethod.Binary:
            return pickle.dumps(obj)
        elif data_type == AppConfig.DictionarySerializationMethod.JSON:
            return json.dumps(obj, indent=4, default=str)
        elif data_type == AppConfig.DictionarySerializationMethod.XML:
            dicttoxml.set_debug(False)
            return dicttoxml.dicttoxml(obj, attr_type=False)
        else:
            raise CsckException("Unknown data type")

    @staticmethod
    def deserialize(obj, data_type:AppConfig.DictionarySerializationMethod):
        if data_type == AppConfig.DictionarySerializationMethod.Binary:
            return pickle.loads(obj)
        elif data_type == AppConfig.DictionarySerializationMethod.JSON:
            return json.loads(obj)
        elif data_type == AppConfig.DictionarySerializationMethod.XML:
            return xmltodict.parse(obj)['root']
        else:
            raise CsckException("Unknown data type")
