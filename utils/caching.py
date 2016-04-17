import json
import glob

def load_cache_file_to_json(location='cache.txt'):

    inf = open(location, 'r')
    jsons = map(lambda x: json.loads(x.strip()), inf.readlines())
    return jsons

def cache(results, address, abv, cached_list=[]):
    tuple_check = (address, abv)
    if tuple_check not in cached_list:
        to_cache = {' '.join(tuple_check): results}
        if glob.glob('cache.txt'):
            with open('cache.txt', 'a') as outf:
                outf.write('\n' + json.dumps(to_cache))
        else:
            with open('cache.txt', 'a') as outf:
                outf.write(json.dumps(to_cache))
        cached_list.append(tuple_check)
