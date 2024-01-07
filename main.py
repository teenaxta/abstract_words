import utils
import pandas as pd
import os
from tqdm import tqdm
import concurrent.futures


def get_word_sets(title: str, paper_url:str) -> (dict, dict):
    abstract_word_count_dict={}
    title_word_count_dict={}
    
    abstract = utils.get_paper_abstract(paper_url)

    abstract_word_count_set = utils.get_word_count(abstract.split())
    title_word_count_set = utils.get_word_count(title.split())
    
    return abstract_word_count_set, title_word_count_set

def get_word_sets_wrapper(args):
    return tuple(get_word_sets(*args))

def main(file_path: str) -> dict:
    
    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            
            url = line.strip()
            urls.append(url)
            
        abstract_word_count_dict={}
        title_word_count_dict={}

        for url in urls:
            titles, page_urls = utils.get_paper_titles_and_urls(url)
            conference_name = utils.get_conference_name(url)
            conference_year = url[34:38]
            
            print(f'Currently scrapping {conference_name} of year {conference_year}')

            # Create a list of tuples pairing titles and page_urls
            data = list(zip(titles, page_urls))
            
            with concurrent.futures.ProcessPoolExecutor(max_workers=40) as executor:
                results = (executor.map(get_word_sets_wrapper, (data)))

            print('Complete')
            out1, out2 = zip(*results)
            for abstract_word_count_set, title_word_count_set in zip(out1, out2):
                abstract_word_count_dict = utils.update_dict_with_set\
                    (abstract_word_count_dict, abstract_word_count_set)
                title_word_count_dict = utils.update_dict_with_set\
                    (title_word_count_dict, title_word_count_set)

            utils.make_csv_from_dict(abstract_word_count_dict, f'results/abstract/{conference_name}_{conference_year}.csv')     
            utils.make_csv_from_dict(title_word_count_dict, f'results/title/{conference_name}_{conference_year}.csv')


if __name__=='__main__':
    file_path = 'urls.txt'
    main(file_path)