import os

from mindee import Client
from credentials import credentialss
from mindee.product import PassportV1
from mindee.input import LocalInputSource
from mindee.product.generated import GeneratedV1


def mindee_mock():
    mindee_client = Client(api_key=credentialss('MINDEE_TOKEN'))
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    upload_dir = os.path.join(project_root, 'uploaded_files')
    fin_res = []
    for file in os.listdir(upload_dir):
        full_path = os.path.join(upload_dir, file)
        if os.path.isfile(full_path):
            try:
                input_doc = mindee_client.source_from_path(full_path)
                result = mindee_client.parse(PassportV1, input_doc)
                fin_res.append(str(result.document.inference.prediction))
            except:
                print('not supported format')
        else:
            print('No data, try again!')

    return '\n\n.'.join(fin_res)