import os
data_path=r"store.txt"
def load_av_set(store_path=data_path):
    if not os.path.exists(store_path):
        return set()
    with open(store_path,'r') as f:
        av_set=set(f.read().splitlines())
    return av_set

def append_av_set(av,store_path=data_path):
    with open(store_path, 'a') as f:
        f.write(av+"\n")
def clear_store(store_path=data_path):
    if os.path.exists(store_path):
        os.remove(store_path)
if __name__ == '__main__':
    test=["abcd","1234","efgh","5678","1234"]
    for st in test:
        append_av_set(st)
    verify_test=load_av_set()
    print(verify_test)
    clear_store()
