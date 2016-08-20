from __future__ import print_function

import os

from main import stanford_ie

tmp_folder = '/tmp/openie/'
if not os.path.exists(tmp_folder):
    os.makedirs(tmp_folder)


def texts_to_files(texts):
    full_tmp_file_names = []
    count = 0
    for text in texts:
        tmp_filename = str(count) + '.txt'
        full_tmp_filename = '{}/{}'.format(tmp_folder, tmp_filename).replace('//', '/')
        with open(full_tmp_filename, 'w') as f:
            f.write(text)
        full_tmp_file_names.append(full_tmp_filename)
        count += 1
    return full_tmp_file_names


def call_api_many(texts, pagination_param=10000, verbose=False):
    reduced_results = []
    paginated_texts_list = [texts[i:i + pagination_param] for i in range(0, len(texts), pagination_param)]
    for paginated_texts in paginated_texts_list:
        tmp_file_names = texts_to_files(paginated_texts)
        joint_filename = ','.join(tmp_file_names)
        results = stanford_ie(joint_filename, verbose=verbose)
        reduced_results.extend(results)
    return reduced_results


def call_api_single(text):
    if os.path.isfile(text):
        full_tmp_filename = text
    else:
        full_tmp_filename = texts_to_files([text])[0]
    results = stanford_ie(full_tmp_filename, verbose=False)
    return results


if __name__ == '__main__':
    print(len(call_api_many(['Barack Obama was born in Hawaii.'] * 30, pagination_param=100, verbose=True)))
