import json
import os
from pathlib import Path
import random
import pandas as pd

from utils import check_json_format
from loader import DataLoader

random.seed(42)


class Dataset:
    def __init__(self, source, url, category, instruction=None, language='English', domain='Math'):
        self.filename = f"Collected_{source}_{category}"
        self.__generate_metadata(source, url, category, instruction, language, domain)
    
    def __generate_metadata(self, source, url, category, instruction, language, domain):
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
                language
            ],
            "Output_language": [
                language
            ],
            "Instruction_language": [
                language
            ],
            "Domains": [
                domain
            ]
        }


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
                # "input": self.__substitute_input(sample),
                # "output": self.__substitute_output(sample),
            })

        for i, instance in enumerate(data):
            instances.append({
                "id": f"{self.filename}-{i}",
                "input": self.__format_input(instance, input_key_dict),
                "output": [
                    self.__format_output(instance, output_key)
                ],
                # "input": self.__substitute_input(instance),
                # "output": [
                #     self.__substitute_output(instance)
                # ],
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
            output = '\n'.join((str(x) for x in instance[output_key]))
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
    
    # MAWPS
    def __substitute_input(self, instance):
        numbers = instance['Numbers'].split()
        number_dict = {f'number{i}': n for i, n in zip(range(len(numbers)), numbers)}
        input = instance['Question']
        for name, value in number_dict.items():
            input = input.replace(name, value)
        return input

    # MAWPS
    def __substitute_output(self, instance):
        numbers = instance['Numbers'].split()
        number_dict = {f'number{i}': n for i, n in zip(range(len(numbers)), numbers)}
        output = instance['Equation']
        for name, value in number_dict.items():
            output = output.replace(name, value)
        return output
    

    def __filter_data(self, data, filter_key, filter_value):
        return [x for x in data if x[filter_key] == filter_value]
        

    def output_json(self, data):
        save_path = os.path.join('./Collected_2', f"{self.filename}.json")
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def generate_coreset_data(self, file_path, input_key_dict, output_key, filter_key=None, filter_value=None, file_type='json', line_num=None):
        original_data = DataLoader(file_path).load_data(file_type, line_num)
        coreset_data = self.format_data(original_data, input_key_dict, output_key, filter_key, filter_value)
        valid, results = check_json_format(coreset_data)
        if valid:
            self.output_json(coreset_data)
            print('SUCCESS: ', self.filename)
        else:
            print(results)