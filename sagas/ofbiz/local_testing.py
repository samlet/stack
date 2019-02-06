import os
import sagas.ofbiz

if __name__ == '__main__':
    print(os.getcwd())
    root_dir=os.path.dirname(sagas.ofbiz.__file__).replace("sagas/ofbiz","")
    print(root_dir)

    # for i in range(1,10):
    #    print(i)

