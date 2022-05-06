import json


def read_document(doc_path):
    with open(doc_path) as doc:
        data_dict = json.load(doc)
        intents = data_dict['intents']
        # intents
        # - tag
        # - patterns
        # - responses
        # - context
    return intents


def write_document(doc_path, data):
    save_data = dict()
    save_data['intents'] = data
    backup_doc(doc_path)
    with open(doc_path, 'w') as doc:
        # pass
        json_obj = json.dumps(save_data, indent=4)
        doc.write(json_obj)


def backup_doc(full_path):
    path_list = str(full_path).split('\\')
    full_path_list = path_list
    file_name = full_path_list[len(full_path_list) - 1]
    file_name_list = file_name.split('.')
    extension = file_name_list[len(file_name_list) - 1]
    f_name = file_name_list[0]
    new_f_name = f_name + '_bkp.' + extension
    orig_data_list = read_document(full_path)
    orig_save_data = dict()
    orig_save_data['intents'] = orig_data_list
    # write the backup
    with open(new_f_name, 'w') as doc:
        json_obj = json.dumps(orig_save_data, indent=4)
        doc.write(json_obj)

# eof
