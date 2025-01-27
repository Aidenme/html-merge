import os
from bs4 import BeautifulSoup

#In general images and text are in the book folder in a folder labeled "text" and another labled "images". If they aren't I can set the path relative to the main book folder here.
HTML_FOLDER = 'text'
IMAGE_FOLDER = 'images'
TEMPLATE_PATHNAME = 'assets\merge_template.html'
EXPORT_FOLDER = 'exports'
DEFAULT_PREPROCESSOR = 'calibre'

#Getting the directory for the first book in the "Books" folder. For the first version I'm just working with one book at a time, but I'm doing all this for possible upgrades later.
def get_book_directory():
    this_file_dir = os.path.dirname(__file__)
    all_books_dir = os.path.join(this_file_dir, 'books')
    #This has all the book folders. I'm only doing this with one book for now though.
    book_folders_list = os.listdir(all_books_dir)
    #See? I'm only referencing the first book here and returning that. And you didn't believe me...
    current_book_dir = os.path.join(all_books_dir, book_folders_list[0])
    return current_book_dir

def create_dict_from_html(book_folder_path):
    html_dict_list = []
    text_folder = os.path.join(book_folder_path, HTML_FOLDER)
    html_file_list = os.listdir(text_folder)

    for filename in html_file_list:
        html_file = {}
        html_file['name'] = filename
        html_file['pathname'] = os.path.join(text_folder, html_file['name'])
        html_file['soup'] = get_soup_from_file(html_file['pathname'])
        html_dict_list.append(html_file)

    return html_dict_list
    #print(html_file_list)

def get_soup_from_file(html_file_pathname):
    with open(html_file_pathname, encoding='utf-8', errors='replace') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    return soup

#This takes all the soups in the dictionaries and puts them between the <body></body> tags in the template html file.
def merge_in_soups(dicts_list, merge_in_template):
    merged_soup = merge_in_template
    for dict in dicts_list:
        merged_soup.body.append(dict['soup'])
    return merged_soup

#Finally outputs the soup generated from everything into an html file. I may need to make this simply export a giant string into an html file because there is some postprocessing I want to do that is easier with a giant string
#rather than BeautifulSoup. Remember BS is designed to deal with raw html files, but not necessarily create them.
def output_soup(input_soup):
    file_pathname = os.path.join(EXPORT_FOLDER, 'export1.html')
    f = open(file_pathname, 'w', encoding='utf-8', errors='replace')
    f.write(input_soup.prettify())
    f.close()

#This function exits to direct the html soups to different processors depending on the source. For now it's just calibre, but I may need to create a more general one later.
def process_dict_array(dict_array, processor=DEFAULT_PREPROCESSOR):
    new_array = []
    if processor == 'calibre':
        for dict in dict_array:
            dict = calibre_preprocessor(dict)
    return dict_array

def calibre_preprocessor(single_dict):
    new_soup = single_dict['soup'].body

    #Adds class "bodydiv" to the outer body so I can reference it. It is an extra div just lying around so I may want to use styles to get rid of it or something. Seems good to be able to reference it later.
    new_soup_class = new_soup.get("class")
    class_note = 'bodydiv'
    if new_soup_class:
        new_soup_class.append(class_note)
    else:
        new_soup_class = [class_note]
    new_soup['class'] = new_soup_class

    #replaces that body tag with a div FINALLY!
    new_soup.name = "div"
    single_dict['soup'] = new_soup
    return single_dict



print(os.getcwd())

html_dict_list = create_dict_from_html(get_book_directory())

template_soup = get_soup_from_file(TEMPLATE_PATHNAME)

processed_dict_list = process_dict_array(html_dict_list)

mixed_soup = merge_in_soups(processed_dict_list, template_soup)

output_soup(mixed_soup)

#print(mixed_soup.prettify())
