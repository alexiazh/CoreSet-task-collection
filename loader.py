import json
import csv
import os
import re
import itertools


quote_chars = r"[“|”|‛|’|‘|`|´|″|′|']"
single_quote_chars = r"[‛|’|‘|`|´|′|']"
double_quote_chars = r"[“|”|″]"


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_data(self, file_type='json', line_num=None):
        if file_type == 'json':
            if os.path.isfile(self.file_path):
                if line_num:
                    return self._load_json_file_multiline(line_num)
                return self._load_json_file()
            if os.path.isdir(self.file_path):
                return self._load_json_dir()
        elif file_type ==  'csv':
            if os.path.isfile(self.file_path):
                return self._load_csv_file()
            if os.path.isdir(self.file_path):
                return self._load_csv_dir()
        elif file_type ==  'txt':
            return self._load_txt_file()
        else:
            raise ValueError(f'Invalid file type: {file_type}')
            
    def _load_txt_file(self):
        data = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
           for l1, l2 in itertools.zip_longest(*[f]*2):
               data.append({
                   'question': l1.strip(), 
                   'answer': l2.strip()
                })
        return data
    
    def _load_csv_file(self):
        with open(self.file_path, mode ='r', encoding='utf-8') as f:    
            data = csv.DictReader(f)
        return data
    
    def _load_csv_dir(self):
        csv_files = [f for f in os.listdir(self.file_path) if f.endswith('.csv')]
        data = []
        for file in csv_files:
            with open(os.path.join(self.file_path, file), 'r', encoding='utf-8') as f:
                data.extend(csv.DictReader(f))
        return data

    def _load_json_file(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = [json.loads(line) for line in f]
        except:
            raise ValueError(f'Unable to load file from {self.file_path}')
        return data


    def _load_json_file_multiline(self, line_num):
        try:
            data = []
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            json_str = ''
            for count, line in enumerate(lines, 1):
                json_str += line
                if count % line_num == 0:
                    example = json.loads(json_str)
                    data.append(example)
                    json_str = ''
            
            return data
        
        except:
            raise ValueError(f'Unable to load file from {self.file_path}')
    
    
    def _load_json_dir(self):
        json_files = [f for f in os.listdir(self.file_path) if f.endswith('.json')]
        data = []
        for file in json_files:
            with open(os.path.join(self.file_path, file), 'r', encoding='utf-8') as f:
                data.append(json.load(f))
        return data
    

    def __replace_quote_chars(self, str):
            parsed = re.sub(quote_chars, '"', str)
            return parsed