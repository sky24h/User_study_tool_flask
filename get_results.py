import os
import glob
import xlwt

def init_dict():
    res = {}
    for i in methods:
        for j in methods:
            if i != j:
                res[str(i)+'_'+str(j)] = 0
    return res

def calculate_from_txts(results_dir):
    res = init_dict()
    lines = []
    for txt_path in glob.glob(os.path.join(results_dir, '*.txt')):
        with open(txt_path, 'r') as r:
            lines += r.read().splitlines()
    for line in lines:
        win, lose, _ = line.split('_')
        res[win+'_'+lose] += 1
    return res


if __name__ == "__main__":
    methods = os.listdir('./static/images')
    methods.sort()

    # get results from txts
    results_dir = './results'
    res = calculate_from_txts(results_dir)

    # initialize the results sheet
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('res')
    for i in range(len(methods)):
        sheet.write(0, i+1, methods[i])
        sheet.write(i+1, 0, 'vs_'+methods[i])

    # calculate the results in percentage
    for i in methods:
        for j in methods:
            if i != j:
                per = "{:.2%}".format(res[i+'_'+j] / (res[i+'_'+j] + res[j+'_'+i]))
                sheet.write(methods.index(j)+1, methods.index(i)+1, float(per[:-1]))
                if i == 'ours':
                    print(i+'_'+j, per)

    # save it to excel
    wb.save('results.xls')
