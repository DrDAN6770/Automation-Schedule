import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart # email內容載體
from email.mime.text import MIMEText # 用於製作文字內文
from time import sleep
from random import random

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def get_send_movies():
    def send_email_with_dataframe(df):
        # 傳送 & 接送資料 & 標題
        sender_email = 'sender email'
        receiver_email = 'receiver email'
        password = 'password'
        subject = 'Weekly Movies List'

        # 轉HTML表格
        df_html = df.to_html(index=True)
        df_html = df_html.replace('<th>', '<th style="text-align:center;">')
        
        # 建立郵件物件
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # 郵件內容
        message.attach(MIMEText(df_html, 'html'))

        # STMP連線
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
        except Exception as e:
            print('An error occurred while sending the email:', str(e))
        finally:
            server.quit()

    def main():
        movies_dict = {}
        pages = [1,2,3]
        # 不同頁
        for page in pages:
            url = f'https://movies.yahoo.com.tw/movie_thisweek.html?page={page}'
            response = requests.get(url)
            res = BeautifulSoup(response.text)
            Movies_list = res.select('#content_l > div.release_box > ul.release_list > li')
            sleep(0.5 + random())
            if Movies_list:
                # 每部的介紹頁面連結
                for movie in Movies_list:
                    # 爬進連結
                    link = movie.a['href']
                    response = requests.get(link)
                    res = BeautifulSoup(response.text)
                    
                    # 電影資料、期待度、主演
                    info = res.select_one('#content_l > div:nth-child(1) > div.l_box_inner > div > div > div.movie_intro_info_r')
                    leveltext = res.select_one('#content_l > div:nth-child(1) > div.l_box_inner > div').find('dl', class_='evaluatebox').find_all('span')
                    Main_Actors = info.find_all('span')[-1].find_all('a')

                    # 建立
                    ch = info.h1.text.strip()
                    en = info.h3.text if info.h3 else None
                    release_movie_time = info.select_one('span:contains("上映日期")').text.split('：')[1] if info.select_one('span:contains("上映日期")') else None
                    time = info.select_one('span:contains("片　　長")').text.split('：')[1] if info.select_one('span:contains("片　　長")') else None
                    IMDB = info.select_one('span:contains("IMDb分數")').text.split('：')[1] + ' / 10' if info.select_one('span:contains("IMDb分數")') else None
                    levelscore = f'{leveltext[1].text}% {leveltext[0].text}' if len(leveltext) >= 2 else None
                    Main_Actors = '、'.join([i.text.strip() for i in Main_Actors]) if [i.text.strip() for i in Main_Actors] else None

                    # 新增
                    movies_dict.setdefault('中文名稱', []).append(ch)
                    movies_dict.setdefault('英文名稱', []).append(en)
                    movies_dict.setdefault('上映日期', []).append(release_movie_time)
                    movies_dict.setdefault('片長', []).append(time)
                    movies_dict.setdefault('IMDB', []).append(IMDB)
                    movies_dict.setdefault('期待度', []).append(levelscore)
                    movies_dict.setdefault('主要演員', []).append(Main_Actors)
                    sleep(1 + random())
        # 轉DF
        df = pd.DataFrame(movies_dict)
        df.index += 1
        return df
    send_email_with_dataframe(main())


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 29),
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('YahooMovie_Weekly_webcrawler',
          default_args=default_args,
          schedule_interval = timedelta(days=7)
)

task = PythonOperator(
    task_id='YahooMovie_Weekly_webcrawler',
    python_callable=get_send_movies,
    dag=dag
)
