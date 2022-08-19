import json

def join_duplicate_keys(ordered_pairs):
    d = {}
    for k, v in ordered_pairs:
        if k in d:
           if type(d[k]) == list:
               d[k].append(v)
           else:
               newlist = []
               newlist.append(d[k])
               newlist.append(v)
               d[k] = newlist
        else:
           d[k] = v
    return d

raw_post_data = '{"a":1, "b":{"b1":1,"b2":2}, "b": { "b1":3, "b2":2,"b4":8} }'
newdict = json.loads(raw_post_data, object_pairs_hook=join_duplicate_keys)
print (newdict)