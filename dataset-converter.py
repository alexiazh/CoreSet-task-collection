import json
import os
from pathlib import Path
import random
import pandas as pd
import re

from utils import check_json_format


random.seed(42)


quote_chars = r"[“|”|‛|’|‘|`|´|″|′|']"
single_quote_chars = r"[‛|’|‘|`|´|′|']"
double_quote_chars = r"[“|”|″]"


class Dataset:
    def __init__(self, source, url, category, instruction=None, domain='Math'):
        self.filename = f"Collected_{source}_{category}"
        self.__generate_metadata(source, url, category, instruction, domain)
    
    def __generate_metadata(self, source, url, category, instruction, domain):
        if instruction is None:
            definition = []
        else:
            definition = [instruction]

        self.metadata = {
            "Contributors": [
                "CoreInst"
            ],
            "Source": [
                source
            ],
            "URL": url,
            "Categories": [
                category
            ],
            "Definition": definition,
            "Input_language": [
                "English"
            ],
            "Output_language": [
                "English"
            ],
            "Instruction_language": [
                "English"
            ],
            "Domains": [
                domain
            ]
        }

    def load_json(self, json_path, line_num=None):
        if not os.path.exists(json_path):
            raise ValueError(f"Path doesn't exist: {json_path}")
        if os.path.isfile(json_path):
            if line_num:
                return self._load_json_file_multiline(json_path, line_num)
            return self._load_json_file(json_path)
        if os.path.isdir(json_path):
            return self._load_json_dir(json_path)  


    def _load_json_file(self, json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = [json.loads(line) for line in f]
            except:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = [json.loads(line) for line in f.read().splitlines()]
        except:
            raise ValueError(f'Unable to load file from {json_path}')
        return data


    def _load_json_file_multiline(self, json_path, line_num):
        try:
            data = []
            with open(json_path, 'r', encoding='utf-8') as f:
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
            raise ValueError(f'Unable to load file from {json_path}')
    
    
    def _load_json_dir(self, json_dir):
        json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
        data = []
        for file in json_files:
            with open(os.path.join(json_dir, file), 'r') as f:
                data.append(json.load(f))
        return data
    

    def __replace_quote_chars(self, str):
            parsed = re.sub(quote_chars, '"', str)
            return parsed


    def format_data(self, original_data, input_key_dict, output_key, filter_key=None, filter_value=None):

        examples = []
        instances = []

        data = original_data
        if filter_key and filter_value:
            data = self.__filter_data(original_data, filter_key, filter_value)

        sampled = random.sample(data, 2)

        for sample in sampled:
            data.remove(sample)
            examples.append({
                "input": self.__format_input(sample, input_key_dict),
                "output": self.__format_output(sample, output_key),
            })

        for i, instance in enumerate(data):
            instances.append({
                "id": f"{self.filename}-{i}",
                "input": self.__format_input(instance, input_key_dict),
                "output": [
                    self.__format_output(instance, output_key)
                ],
            })
        
        content = {
            "Positive Examples": examples,
            "Instances": instances,
        }
        
        return {**self.metadata, **content}
    

    def __format_input(self, instance, input_key_dict):
        if len(input_key_dict) == 0:
            raise ValueError('No input keys provided.')
        if len(input_key_dict) == 1:
            value = instance[list(input_key_dict.keys())[0]]
            # if isinstance(value, dict):
            #     input_lst = []
            #     input_lst.append(value['stem'])
            #     input_lst.extend([f"{choice['label']}. {choice['text']}" for choice in value['choices']])
            #     input = '\n'.join(input_lst)
            # else:
            input = str(value)
        else:
            input_lst = []
            for key, prefix in input_key_dict.items():
                value = instance[key]
                if isinstance(value, str):
                    if prefix:
                        input_lst.append(f'{prefix}: {value}')
                    else:
                        input_lst.append(value)
                if isinstance(value, list):
                    if prefix:
                        input_lst.append(f'{prefix}:')
                    input_lst.extend(value)
            input = '\n'.join(input_lst)
        return input
    
    def __format_output(self, instance, output_key):
        if isinstance(instance[output_key], list):
            output = '\n'.join(instance[output_key])
        # elif isinstance(instance[output_key], dict):
        #     if instance[output_key]['number']:
        #         output = str(instance[output_key]['number'])
        #     elif instance[output_key]['spans']:
        #         output = ', '.join(instance[output_key]['spans'])
        #     else:
        #         output = ', '.join([v for v in instance[output_key]['date'].values() if v])
        else:
            output = str(instance[output_key])
        return output
    

    def __filter_data(self, data, filter_key, filter_value):
        return [x for x in data if x[filter_key] == filter_value]
        

    def output_json(self, data):
        save_path = os.path.join('./Collected', f"{self.filename}.json")
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def generate_coreset_data(self, json_path, input_key_dict, output_key, filter_key=None, filter_value=None, line_num=None):
        original_data = self.load_json(json_path, line_num)
        coreset_data = dataset.format_data(original_data, input_key_dict, output_key, filter_key, filter_value)
        valid, results = check_json_format(coreset_data)
        if valid:
            dataset.output_json(coreset_data)
            print('SUCCESS')
        else:
            print(results)
        

if __name__ == '__main__':
    json_path = './Math23K/math23k_train.json'
    source = 'Math23K'
    url = 'https://ai.tencent.com/ailab/nlp/dialogue/#datasets'
    
    category = 'Math_Word_Problem_Solving_Answer'
    instruction = '给定一个代数问题，给出最终的数字作为答案。'

    input_key_dict = {
        'original_text': None
    }
    output_key = 'ans'
    filter_key = None
    filter_value = None
    line_num = 7

    dataset = Dataset(source, url, category, instruction, domain='Math')
    dataset.generate_coreset_data(json_path, input_key_dict, output_key, filter_key, filter_value, line_num)