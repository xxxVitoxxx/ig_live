# -*- coding: utf-8 -*-
import pygsheets
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler

# load google sheet
def openGoogleSheets(url):
    gc = pygsheets.authorize(service_file='/Users/vito/Project/count_clothes/credentials.json')
    sht = gc.open_by_url(url)
    return sht

# 計算商品各標號數量
def countCommodity(sht):
    count = {}
    
    for i in df.index:
        # if column A has label, add data to dictionary 
        if df['標籤'][i] != '' and df['標籤'][i][0] == '標':
            count[df['標籤'][i]] = {}
            count[df['標籤'][i]][df['商品名稱'][i]] = {}

            if df['店面'][i] != '' and df['工作室'][i] != '':
                count[df['標籤'][i]][df['商品名稱'][i]][df['顏色/尺寸'][i]] = df['店面'][i] + df['工作室'][i]
            elif df['店面'][i] == '' and df['工作室'][i] != '':
                count[df['標籤'][i]][df['商品名稱'][i]][df['顏色/尺寸'][i]] = df['工作室'][i]
            elif df['店面'][i] != '' and df['工作室'][i] == '':
                count[df['標籤'][i]][df['商品名稱'][i]][df['顏色/尺寸'][i]] = df['店面'][i]
            else:
                count[df['標籤'][i]][df['商品名稱'][i]][df['顏色/尺寸'][i]] = 0

        # if column C has a value & column D or column E  , add data to dictionary
        if df['標籤'][i] == '' or df['標籤'][i][0] != '標':
            for x, y in count.items():
                # 檢查商品名稱已在 dictionary 內
                if df['商品名稱'][i] in y.keys():
                    # 檢查店面和工作室的欄位是不是空白
                    if df['店面'][i] != '' and df['工作室'][i] != '':
                        count[x][df['商品名稱'][i]][df['顏色/尺寸'][i]] = df['店面'][i] + df['工作室'][i]
                    elif df['店面'][i] == '' and df['工作室'][i] != '':
                        count[x][df['商品名稱'][i]][df['顏色/尺寸'][i]] = df['工作室'][i]
                    elif df['店面'][i] != '' and df['工作室'][i] == '':
                        count[x][df['商品名稱'][i]][df['顏色/尺寸'][i]] = df['店面'][i]
                    else:
                        count[x][df['商品名稱'][i]][df['顏色/尺寸'][i]] = 0
    # output:
    # {'標1': {'高領長版針衣': {'桔': 8, '深灰': 3, '白': 11}}, '標2': {'藍莓優格小澎袖毛衣': {'深藍': 5}}, '標3': {'滾邊鋪棉背心': {'白': 2, '綠': 2, '咖': 4}}, '標4': {'菱格v針織上衣': {'紅': 3}}, '標5': {'針織側開上衣 桔5': {'': 0}}, '標6': {'撞色排釦毛衣 藍3': {'': 0}}, '標7': {'高領坑文寬鬆毛衣 黃 1+9': {'': 0}}, '標8': {'格子高腰開岔褲 3': {'': 0}}, '標9': {'撞色針織外 杏8': {'': 0}}, '標10': {'小香針衣 黑 1+33': {'': 0}}, '標11': {'圓領捲邊針織上衣 咖4': {'': 0}}, '標12': {'熊寶寶皮背心 咖 1+25': {'': 0}}, '標13': {'菱格排釦針織外套 藍5': {'': 0}}, '標14': {'直筒牛仔褲 S1+4': {'': 0}}, '標15': {'針織裙 黑5': {'': 0}}, '標16': {'鬆緊奶奶褲 黑2': {'': 0}}, '標17': {'皮帶老爺褲 黑 1+25': {'': 0}}, '標18': {'皮短外 杏 1+9': {'': 0}}, '標19': {'坑文針織套裝 黑 1+2': {'': 0}}, '標20': {'激瘦皮短裙 深咖10': {'': 0}}, '標21': {'大圍巾 黑1+4': {'': 0}}, '標22': {'四扣長針外 子': {'': 0}}, '標23': {'黑白馬海毛': {'': 0}}, '標24': {'冬日奶霜坑紋長裙 黑': {'': 0}}, '標25': {'長褲燕麥': {'': 0}}, '標26': {'翻領POLO 黑': {'': 0}}, '標27': {'灰色裙子': {'': 0}}, '標28': {'V領長版': {'': 0}}, '標29': {'圓領奶茶': {'': 0}}, '標30': {'坑文 深藍': {'': 0}}, '標31': {'背心 咖': {'': 0}}, '標32': {'前短後長 白': {'': 0}}, '標33': {'高領燕麥上衣': {'': 0}}, '標34': {'長裙 灰': {'': 0}}, '標35': {'麻花園領上衣': {'': 0}}, '標36': {'杏色針織罩衫': {'': 0}}, '標37': {'黑白菱格 黑': {'': 0}}, '標38': {'熊熊拖鞋': {'': 0}}, '標39': {'包包 杏': {'': 0}}, '標40': {'帽子 黑': {'': 0}}, '標41': {'36/咖毛毛拖鞋': {'': 0}}}
    return count

# 統計各標號顏色下單的客人名單
def orderCustomerList(df):
    count = {}

    for i in df.index:
        print('df i: ', i)
        # 檢查 A 欄是標號的
        if df['標籤'][i] != '' and df['標籤'][i][0] == '標':
            # print('name-------: ', df['標籤'][i], '-', df['顏色/尺寸'][i])
            count[df['標籤'][i]] = {}
            count[df['標籤'][i]][df['商品名稱'][i]] = {}

            if (df['店面'][i] != '' or df['工作室'][i] != '') :
                account_list = []
                for j in range(1, 11):
                    # 檢查是否有帳號
                    if  df['IG account'+str(j)][i] != "":
                        account_list.append(str(df['IG account'+str(j)][i]))
                    else:
                        break
                
                count[df['標籤'][i]][df['商品名稱'][i]][df['顏色/尺寸'][i]] = account_list
        # 檢查 A 欄不是標號
        elif (df['標籤'][i] == '' or df['標籤'][i].strip()[0] != '標'):
            # 檢查商品名稱沒空白
            if any(df['商品名稱'][i]):
                alist = []
                # 在 count 找出商品名稱
                for x, y in count.items():
                    if df['商品名稱'][i] in y.keys():
                        
                        for row in range(5):
                            if i+row < df['IG account1'].count() and any(str(df['IG account1'][i])):
                                # if any(str(df['商品名稱'][i+row])):
                                #     break
                                # if any(str(df['IG account1'][i+row])):
                                for j in range(1, 11):
                                    # 如果 IG account 有帳號繼續加帳號清單，沒有就離開
                                    if any(str(df['IG account'+str(j)][i+row])):
                                        alist.append(str(df['IG account'+str(j)][i+row]))
                                        
                                    else:
                                        break
                        count[x][df['商品名稱'][i]][df['顏色/尺寸'][i]] = alist
                        # print('alist: ', alist)
                        # if df['商品名稱'][i] == '大圍巾' and df['顏色/尺寸'][i] == '灰':
                        #     print("x: ", x, 'i: ', i)
                        #     print('名稱： ', df['商品名稱'][i], 'color: ', df['顏色/尺寸'][i])
                        #     print("checkkkkkkkk: ", count)

            # 如果商品名稱空白但 IG account1有帳號
            # if not any(df['商品名稱'][i]) and any(df['IG account1'][i]): 
            #     # 將原本帳號清單指定給變數
            #     print('cccc: ', count)
            #     ll = []
                
            #     # for j in range(1, 11):
            #     #     # 檢查是否有帳號
            #     #     if  df['IG account'+str(j)][i] != "":
            #     #         ll.append(str(df['IG account'+str(j)][i]))

            #     # 從該行開始，往上最多回搜 4 行
            #     for row in range(5):
            #         print('i: {}, row: {}'.format(i, row))
            #         if df['商品名稱'][i-row] != '' and df['顏色/尺寸'][i-row] != '':
            #             break
                    
            #         if i-row >= 0 and df['商品名稱'][i-row] == '' and df['顏色/尺寸'][i-row] == '':
            #             for j in range(1, 11):
            #                 # 檢查是否有帳號
            #                 if  df['IG account'+str(j)][i-row] != "":
            #                     ll.append(str(df['IG account'+str(j)][i-row]))

            #     print('ll: ', ll)
            #     print('name: ', name)
            #     print('color: ', color)

            #             # 找
            #     for x, y in count.items():
            #         # print('xy: ', df['商品名稱'][i-row])
            #         # print('x: ', x)
            #         # print('y: ', y)
            #         # print('bool: ',df['商品名稱'][i-row] in y.keys())
            #         if name in y.keys():

            #             for v in ll:
            #                 count[x][name][color].append(v)
            #     print('ll count: ', count)

    return count

def check(df, ws, count, order):
    # print(count)
    # print('-----')
    # k -> 標號
    for k, v in order.items():
        # i -> 商品名稱
        for i, j in v.items():
            # x -> 顏色/尺寸
            # y -> 下單名單 list
            for x, y in j.items():
                sum = count[k][i][x]
                # print(k, '-', i, '-', x, '===', y, 'total: ', sum)
                # print('len(y)', len(y))
                # print('sum: ', sum)
                # 標1 - 高領長版針衣 - 白 === ['tiny_ashleyyyeee ']
                if len(y) == 0:
                    df.loc[ (df['商品名稱'] == i) & (df['顏色/尺寸'] == x), '上限'] = False
                    df.loc[ (df['商品名稱'] == i) & (df['顏色/尺寸'] == x), '通知'] = ''

                if len(y) > 0 and len(y) < sum:
                    df.loc[ (df['商品名稱'] == i) & (df['顏色/尺寸'] == x), '上限'] = False
                    print("haa: ", len(y), sum)
                    buy = ', '.join(y)
                    df.loc[ (df['商品名稱'] == i) & (df['顏色/尺寸'] == x), '通知'] = '{} {} 得標者: {}'.format(k, x, buy)
                    print('-ddddfffe: ', '{} {} 得標者: {}'.format(k, x, buy))

                if len(y) == sum:
                    df.loc[ (df['商品名稱'] == i) & (df['顏色/尺寸'] == x), '上限'] = True
                    buy = ', '.join(y)
                    df.loc[ (df['商品名稱'] == i) & (df['顏色/尺寸'] == x), '通知'] = '{} {} 得標者: {}'.format(k, x, buy)

                if len(y) > sum:
                    df.loc[ (df['商品名稱'] == i) & (df['顏色/尺寸'] == x), '上限'] = True
                    buy = ', '.join(y[:sum])
                    cant_buy = ', '.join(y[sum:])
                    # print('join: ', y[sum:-1])
                    # print("buy: ", buy)
                    # print("cant buy: ", cant_buy)
                    df.loc[ (df['商品名稱'] == i) & (df['顏色/尺寸'] == x), '通知'] = '{} {} 得標者: {}\n候補: {}'.format(k, x, buy, cant_buy)
                    # print('{} {} 得標者: {}\n候補: {}'.format(k, x, buy, cant_buy))
                    # print(df.loc[ (df['商品名稱'] == i) & (df['顏色/尺寸'] == x), '通知'])
    print('df: ', df)
    print('-------------------')
    # 不知道怎麼將更新過的 df 更新到 sheets 上，所以暫用迴圈賦值
    for i in df.index:
        # print(i)
        # # print(df['商品名稱'][i], df['顏色/尺寸'])
        # print('name: ', df['商品名稱'][i])
        # print(ws.get_value('B'+str(i+2)))
        # print('---')
        # print('color: ', df['顏色/尺寸'][i])
        # print(ws.get_value('C'+str(i+2)))

        print()
        if any(df['商品名稱'][i]) and any(df['顏色/尺寸'][i]):
            print(i)
            ck = pd.notnull(df.iloc[i,19])
            print(df.iloc[i,19])
            # ck = pd.notnull(df.iloc[i,19]) and any(df.iloc[i,19])
            print("ck: ", ck)
            if ck:
                ws.update_value('T'+ str(i+2), df['上限'][i]) # df['上限'][i]
                print('上限', df['上限'][i])
            ok = pd.notnull(df.iloc[i,20])
            # ok = pd.notnull(df.iloc[i,20]) and any(df.iloc[i,20])
            # print('yy: ', yy)
            if ok:
                ws.update_value('U'+ str(i+2), df['通知'][i])
                print('通知', df['通知'][i])
        # print(i)
        # print(df.isnull(df.iloc[i,'上限']))
    print('----------------------------------------------------------------')

    # print(df)
                    
                


if __name__ == '__main__':
    url = 'https://docs.google.com/spreadsheets/d/11tHWJh-Dp7SdS9BokrPABPWi9eIjKc8qL9NZ3g_tDgc/edit#gid=1243175386'
    # 'https://docs.google.com/spreadsheets/d/1RIxH4n5lPw734xynrK9xEGB37ftmniKqY7Mx8CixHog/edit#gid=1243175386'
    sht = openGoogleSheets(url)
    df = pd.DataFrame(sht.worksheet_by_title('商品').get_all_records())
    print(df['IG account1'].count())
    # print(countCommodity(sht))
    # print("dddd:", orderCustomerList(sht))
    # print(df.loc[ df['標籤'] == '標10'])
    c = countCommodity(df)
    o = orderCustomerList(df)
    ws = sht.worksheet_by_title('商品')
    check(df, ws, c, o)
    print(df['商品名稱'][140], df['顏色/尺寸'][140])
    print(any(df['商品名稱'][140]))


    # scheduler = BlockingScheduler()
    # scheduler.add_job(ppp, "interval", seconds=5)
    # scheduler.start()