import os

def clear_cache_files():
    dir = './Cache'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

if __name__ == '__main__':
    clear_cache_files()