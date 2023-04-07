import pandas as pd

data = pd.read_excel("test.xlsx")

Contamination = data.iloc[0]
Plant = data.iloc[1]

Contamination = Contamination.values.tolist()
Plant = Plant.values.tolist()
# print(Contamination)
# print(Plant)

datas = data.iloc[2:]
list_datas = datas.values.tolist()
# print(len(list_datas))

pre_processed_name = "d__Archaea"

res = []
res_num = 0
for i in range(len(list_datas)):
    sample_data = list_datas[i]
    if sample_data[0].find(pre_processed_name) != -1:
        res.append(sample_data)

print(res)
print(len(res))

post_process_res = res[0]
for i in range(1, len(res)):
    for j in range(1, len(res[i])):
        post_process_res[j] += res[i][j]
print(post_process_res)


Contamination_data = [Contamination, post_process_res]
Plant_data = [Plant, post_process_res]

con_items = list(set(Contamination[1:]))
plant_items = list(set(Plant[1:]))
print(con_items)
print(plant_items)

Con_res = [0] * len(con_items)
Plant_res = [0] * len(plant_items)

con_dict = {item: 0 for item in con_items}
plant_dict = {item: 0 for item in plant_items}

for item, res in zip(Contamination, post_process_res):
    if item in con_dict:
        con_dict[item] += res

for item, res in zip(Plant, post_process_res):
    if item in plant_dict:
        plant_dict[item] += res

Con_res = list(con_dict.values())
Plant_res = list(plant_dict.values())

print(Con_res)
print(Plant_res)
