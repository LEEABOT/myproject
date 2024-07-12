import requests
from bs4 import BeautifulSoup
import pymysql
import concurrent.futures
import time

def 抓取食谱(url, headers):
    try:
        response = requests.get(url=url, headers=headers)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'lxml')
        else:
            return None
    except requests.exceptions.RequestException as e:
        print('请求失败：', e)
        return None

def 插入食谱(data, conn_details):
    conn = pymysql.connect(**conn_details)
    cursor = conn.cursor()
    sql = 'INSERT INTO foods(id, foodname, picsrc, url, foodmaterial, foodstep, fooddoor) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    try:
        cursor.execute(sql, data)
        conn.commit()
    except Exception as e:
        print('插入数据失败：', e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def 处理页面(page, headers, conn_details):
    url = f'https://home.meishichina.com/recipe-{page}.html'
    soup = 抓取食谱(url, headers)
    if soup:
        foods = soup.select('.recipe_De_title')
        material = soup.find_all('div', attrs={'class': 'recipeCategory_sub_R'})
        step = soup.find_all('div', attrs={'class': 'recipeStep_word'})
        smalldoor = soup.find_all('div', attrs={'class': 'recipeTip'})
        picture = soup.select('.recipe_De_imgBox')

        if foods and material and step and smalldoor and picture:
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
                插入食谱(data, conn_details)

def 抓取并插入食谱():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }

    conn_details = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'db': 'spiderdb',
        'port': 3306,
        'charset': 'utf8'
    }

    pages = range(1400, 80000)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(处理页面, page, headers, conn_details) for page in pages]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

    print("数据抓取和插入完成。")

if __name__ == '__main__':
    抓取并插入食谱()
