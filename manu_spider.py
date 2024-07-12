import requests
import pymysql
import time
from bs4 import BeautifulSoup

def 抓取食谱(url, headers, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url=url, headers=headers)
            response.encoding = 'utf-8'
            return BeautifulSoup(response.text, 'lxml')
        except requests.exceptions.RequestException as e:
            print('请求失败：', e)
            print(f'重试次数: {attempt+1}/{retries}')
            time.sleep(2)  # 等待一段时间后再次尝试
            attempt += 1
    print('请求失败，达到最大重试次数。')
    return None

def 插入食谱(cursor, sql, data, conn):
    try:
        cursor.execute(sql, data)
        conn.commit()
    except Exception as e:
        print('插入数据失败：', e)
        conn.rollback()

def 抓取并插入食谱():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }

    conn = pymysql.connect(host='localhost', user='root', password='123456', db='spiderdb', port=3306, charset='utf8')
    cursor = conn.cursor()

    sql = 'INSERT INTO foods(id, foodname, picsrc, url, foodmaterial, foodstep, fooddoor) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    for page in range(2777, 80000):
        url = f'https://home.meishichina.com/recipe-{page}.html'
        soup = 抓取食谱(url, headers)

        foods = soup.select('.recipe_De_title')
        material = soup.find_all('div', attrs={'class': 'recipeCategory_sub_R'})
        step = soup.find_all('div', attrs={'class': 'recipeStep_word'})
        smalldoor = soup.find_all('div', attrs={'class': 'recipeTip'})
        picture = soup.select('.recipe_De_imgBox')

        for food in foods:
            urls = food.find('a')
            name = urls.get_text()
            link = urls["href"]

            food_material = [c.text.strip().replace('\n', '') for mat in material for c in mat.find_all('li')]
            str1 = ','.join(food_material)

            str2 = ','.join(ste.text for ste in step)

            img_link = picture[0].find('img')["src"]
            door = smalldoor[0].text.strip().replace('\n', '').replace('\r', '')

            data = (page, name, img_link, link, str1, str2, door)
            插入食谱(cursor, sql, data, conn)

        print("抓取网页：", page)
        time.sleep(2)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    抓取并插入食谱()
    print("数据抓取和插入完成。")
