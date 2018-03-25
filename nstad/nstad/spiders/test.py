import re

value = "{pid:'20145783',cgmc:'特大跨度多肋钢桁拱桥设计与施工关键技术研究',cgdywcdw:'重庆高速公路集团有限公司渝东建设分公司',lxtime:'7/10/2015'}"

p_id_str = 'pid\s*:\s*\'(.*?)\''
p_date_str = 'lxtime\s*:\s*\'(.*?)\''

p_id = re.compile(p_id_str)
p_date = re.compile(p_date_str)

_id = p_id.search(value).group(0)
date = p_date.search(value).group(0)

print(_id)
print(date)