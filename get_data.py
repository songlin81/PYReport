import requests
from lxml import etree
import json
import re
import openpyxl


class Get_data():

    def get_version(self):
        return "2.0.1"

    def get_data(self):
        url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.149 Safari/537.36 '
        }
        response = requests.get(url, headers=headers)
        with open('html2.txt', 'w', encoding='utf-8') as file:
            file.write(response.text)

    def get_time(self):
        with open('html2.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        time_in = re.findall('"mapLastUpdatedTime":"(.*?)"', text)[0]
        time_out = re.findall('"foreignLastUpdatedTime":"(.*?)"', text)[0]
        print('国内疫情更新时间为 ' + time_in)
        print('国外疫情更新时间为 ' + time_out)
        return time_in, time_out

    def parse_data(self):
        with open('html2.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        html = etree.HTML(text)
        result = html.xpath('//script[@type="application/json"]/text()')
        result = result[0]
        result = json.loads(result)
        result = json.dumps(result['component'][0]['caseList'])
        with open('data2.json', 'w', encoding='utf-8') as file:
            file.write(result)
            print('数据已写入json文件...')
        response = requests.get("https://voice.baidu.com/act/newpneumonia/newpneumonia/")
        with open('html2.txt', 'w', encoding='utf-8') as file:
            file.write(response.text)
        time_in = re.findall('"mapLastUpdatedTime":"(.*?)"', response.text)[0]
        time_out = re.findall('"foreignLastUpdatedTime":"(.*?)"', response.text)[0]
        print(time_in)
        print(time_out)

        html = etree.HTML(response.text)
        result = html.xpath('//script[@type="application/json"]/text()')
        print(type(result))
        result = result[0]
        print(type(result))
        result = json.loads(result)
        print(type(result))
        # 以每个省的数据为一个字典
        data_in = result['component'][0]['caseList']
        for each in data_in:
            print(each)
            print("\n" + '*' * 20)

        data_out = result['component'][0]['globalList']
        for each in data_out:
            print(each)
            print("\n" + '*' * 20)

        '''
            area --> 大多为省份
            city --> 城市
            confirmed --> 累计
            died --> 死亡
            crued --> 治愈
            relativeTime --> 
            confirmedRelative --> 累计的增量
            curedRelative --> 治愈的增量
            curConfirm --> 现有确诊
            curConfirmRelative --> 现有确诊的增量
            diedRelative --> 死亡的增量
        '''

        wb = openpyxl.Workbook()
        ws_in = wb.active
        ws_in.title = "国内疫情"
        ws_in.append(['省份', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量', '死亡增量', '治愈增量', '现有确诊增量'])
        for each in data_in:
            temp_list = [each['area'], each['confirmed'], each['died'], each['crued'], each['curConfirm'],
                         each['confirmedRelative'], each['diedRelative'], each['curedRelative'],
                         each['curConfirmRelative']]
            for i in range(len(temp_list)):
                if temp_list[i] == '':
                    temp_list[i] = '0'
            ws_in.append(temp_list)

        for each in data_out:
            print(each)
            print("\n" + '*' * 20)
            sheet_title = each['area']
            ws_out = wb.create_sheet(sheet_title)
            ws_out.append(['国家', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量'])
            for country in each['subList']:
                list_temp = [country['country'], country['confirmed'], country['died'], country['crued'],
                             country['curConfirm'], country['confirmedRelative']]
                for i in range(len(list_temp)):
                    if list_temp[i] == '':
                        list_temp[i] = '0'
                ws_out.append(list_temp)

            wb.save('./dataMap.xlsx')

