import json
with open('timeline_json.json','r') as time_json:
    result = json.load(time_json)

# print(result)

# for d in result['event_timeline']:
#     for k,v in d.items():
#         # print(k,'----',v)
#         if 'em'==k:
#             print('em present')
#         elif 'extr'==k:
#             print('extr presnt')

# for d in result['event_timeline']:
#     if d['name'] == 'VideoSessionStart':
#         print(d['em'],'----',d['extr'])

for d in result['event_timeline']:
    # print(d['timestamp'])
    if d['name']:
        print(d['name'])
        print(d['em'],'----',d['extr'])