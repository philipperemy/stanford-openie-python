from __future__ import print_function

import os

from main import stanford_ie

tmp_folder = 'tmp/'
if not os.path.exists(tmp_folder):
    os.makedirs(tmp_folder)

absolute_path = os.path.dirname(os.path.realpath(__file__)) + '/'


def texts_to_files(texts, prefix_tmp_filename=''):
    full_tmp_file_names = []
    count = 0
    for text in texts:
        tmp_filename = str(count) + '.txt'
        full_tmp_filename = '{}/{}'.format(prefix_tmp_filename + tmp_folder, tmp_filename).replace('//', '/')
        with open(full_tmp_filename, 'w') as f:
            f.write(text)
        full_tmp_file_names.append(full_tmp_filename)
        count += 1
    return full_tmp_file_names


def call_api_many(texts, pagination_parameter=10000, verbose=False, prefix_tmp_filename=''):
    reduced_results = []
    paginated_texts_list = [texts[i:i + pagination_parameter] for i in range(0, len(texts), pagination_parameter)]
    for paginated_texts in paginated_texts_list:
        tmp_file_names = texts_to_files(paginated_texts, prefix_tmp_filename)
        joint_filename = ','.join(tmp_file_names)
        results = stanford_ie(joint_filename, verbose=verbose, absolute_path=absolute_path)
        reduced_results.extend(results)
    return reduced_results


def call_api_single(text):
    if os.path.isfile(text):
        full_tmp_filename = text
    else:
        full_tmp_filename = absolute_path + texts_to_files([text])[0]
    results = stanford_ie(full_tmp_filename, verbose=False, absolute_path=absolute_path)
    return results


if __name__ == '__main__':
    print(len(call_api_many(['Barack Obama was born in Hawaii.'] * 30, pagination_parameter=100, verbose=True)))
