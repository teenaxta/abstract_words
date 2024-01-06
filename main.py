import utils
import pandas as pd
import os
from tqdm import tqdm

def main(file_path: str) -> dict:
    
    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            
            url = line.strip()
            urls.append(url)

        for url in urls:
            titles, page_urls = utils.get_paper_titles_and_urls(url)
            conference_name = utils.get_conference_name(url)
            
            print(f'Currently scrapping {conference_name}')

            abstract_word_count_dict={}
            title_word_count_dict={}

            for title, paper_url in tqdm(zip(titles, page_urls)):

                abstract = utils.get_paper_abstract(paper_url)

                abstract_word_count = utils.get_word_count(abstract)
                title_word_count = utils.get_word_count(title)

                abstract_word_count_dict = utils.compare_and_add_dicts\
                    (abstract_word_count_dict, abstract_word_count)
                title_word_count_dict = utils.compare_and_add_dicts\
                    (title_word_count_dict, title_word_count)

            utils.make_csv_from_dict(abstract_word_count_dict, f'results/abstract/{conference_name}')     
            utils.make_csv_from_dict(abstract_word_count_dict, f'results/title/{conference_name}')


if __name__=='__main__':
    file_path = 'urls.txt'
    main(file_path)