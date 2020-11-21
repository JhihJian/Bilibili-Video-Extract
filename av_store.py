import os
data_path=r"av_set.txt"
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
    test=[585337686]
    verify_test=load_av_set()
    print('already download av size:' + str(len(verify_test)))
    for av in test:
        if str(av) not in verify_test:
            print("ok")
        else:
            print("already download av "+str(av)+",jump it")
