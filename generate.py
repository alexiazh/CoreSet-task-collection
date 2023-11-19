import os
from dataset import Dataset
from utils import *

def generate_methematics_dataset():
    dataset_dir = './mathematics_dataset-v1.0/train-easy'
    files = [f for f in os.listdir(dataset_dir) if f.endswith('.txt')]
    file_type = 'txt'

    source = 'Mathematics_Dataset'
    url = 'https://github.com/google-deepmind/mathematics_dataset'
    instruction = 'Give the answer to the mathematical problem.'

    input_key_dict = {
        'question': None
    }
    output_key = 'answer'
    filter_key = None
    filter_value = None
    line_num = None
    
    for file in files:
        file_path = os.path.join(dataset_dir, file)
        task, subtask = file.split('.')[0].split('__', 1)
        category = f'Easy_{task.capitalize()}_{subtask}'

        dataset = Dataset(source, url, category, instruction, language='English', domain='Math')
        dataset.generate_coreset_data(file_path, input_key_dict, output_key, filter_key, filter_value, file_type, line_num)


def generate_dataset():
    file_path = './DRAW-1K/draw-train.json'
    file_type = 'json'
    source = 'DRAW-1K'
    url = 'https://www.microsoft.com/en-au/download/details.aspx?id=52628'
    
    category = 'Algebraic_Word_Problems_Solution'
    instruction = 'Given an algebraic problem, give the final numerical solutions.'

    input_key_dict = {
        'sQuestion': None
    }
    output_key = 'lSolutions'
    filter_key = None
    filter_value = None
    line_num = None

    dataset = Dataset(source, url, category, instruction, language='English', domain='Math')
    dataset.generate_coreset_data(file_path, input_key_dict, output_key, filter_key, filter_value, file_type, line_num)


if __name__ == '__main__':
    generate_dataset()