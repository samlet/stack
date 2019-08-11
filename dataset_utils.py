import io
import json

def write_dataset(obj, dataset_name):
    filename="./sagas/dataset/{}.json".format(dataset_name)
    text=json.dumps(obj, indent=4, ensure_ascii=False)
    with io.open(filename, 'w', encoding="utf-8") as f:
        f.write(text)

