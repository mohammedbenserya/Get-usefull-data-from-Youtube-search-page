
from bs4 import BeautifulSoup as bs
import requests
import json
from selenium import webdriver #open webdriver for specific browser
from selenium.webdriver.common.keys import Keys   #for necessary browser action
import time #used for sleep function
from tkinter import *
import tkinter as tk
from tkinter.ttk import Progressbar
import lxml



def get_video_info(url):
    try:
        response = requests.get(url).text
            # download HTML code
        #response = session.get(url)
        # execute Javascript
        #response.html.render(timeout=60)
        # create beautiful soup object to parse HTML
        #soup = bs(response.html.html, "html.parser")
        soup = bs(response,'lxml')
        # open("index.html", "w").write(response.html.html)
        # initialize the result
        result = {}
        # video title
        result["title"] = soup.find("meta", itemprop="name")['content']

        result["videoId"] = soup.find("meta", itemprop="videoId")['content']
        result["thumbnail"] = soup.find("meta", property="og:image")['content']
        # video views
        result["views"] = soup.find("meta", itemprop="interactionCount")['content']
        # video description
        result["description"] = soup.find("meta", itemprop="description")['content']
        # date published
        result["date_published"] = soup.find("meta", itemprop="datePublished")['content']
        result["date_uplaoded"] = soup.find("meta", itemprop="uploadDate")['content']
        # get the duration of the video
        #result["duration"] = soup.find("span", {"class": "ytp-time-duration"}).text
        # get the video tags
        #result["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])




        #result["likes"] = ''.join([ c for c in text_yt_formatted_strings[0].attrs.get("aria-label") if c.isdigit() ])
        #result["likes"] = 0 if result['likes'] == '' else int(result['likes'])
        # number of dislikes
        #result["dislikes"] = ''.join([ c for c in text_yt_formatted_strings[1].attrs.get("aria-label") if c.isdigit() ])
        #result['dislikes'] = 0 if result['dislikes'] == '' else int(result['dislikes'])

        result["genre"] = soup.find("meta", itemprop="genre")['content']
        # channel details
        #channel_tag = soup.find("yt-formatted-string", {"class": "ytd-channel-name"}).find("a")
        # channel name
        #channel_name = channel_tag.text
        # channel URL
        #channel_url = f"https://www.youtube.com{channel_tag['href']}"
        # number of subscribers as str
        #channel_subscribers = soup.find("yt-formatted-string", {"id": "owner-sub-count"}).text.strip()
        #result['channel'] = {'name': channel_name, 'url': channel_url, 'subscribers': channel_subscribers}
        return result
    except Exception :
        print(Exception)
        return False

def get_infos(keyword):


        url=[]


        search = keyword.split(" ")
        query = '+'.join(str(x) for x in search)

        #response = requests.get(f"https://www.youtube.com/results?search_query={query}&persist_gl=1&gl=US").text
        #driver = webdriver.Chrome("./chromedriver.exe")
        driver = webdriver.Firefox()

        driver.get(f"https://www.youtube.com/results?search_query={query}&persist_gl=1&gl=US")

        time.sleep(1.5)

        for i in range(10):
            height = driver.execute_script("return document.body.scrollHeight")
            time.sleep(1.5)
            driver.find_element_by_tag_name('body').send_keys(Keys.END)            
        links = driver.find_elements_by_id("video-title")
        for x in links:

            if x.get_attribute("href")!= None:
                url.append(x.get_attribute("href"))

        driver.close()
        infos=[]
        win= tk.Tk()
        win.title('loading please wait')
        p = Progressbar(win,orient=HORIZONTAL,length=200,mode="determinate",takefocus=True,maximum=100)
        p.pack()
            
        for u in url:  
            data = get_video_info(u)
            if data is not False:

                p.step(100/len(url))            
                win.update()
                print(u+" --------------- done")
                
                infos.append({    
                    'id':data['videoId'],
                    'updatedAt':data["date_uplaoded"],
                    'createdAt':data['date_published'],
                    'title':data['title'],
                    'description':data['description'],
                    'url':u,
                    'thumbnail':data["thumbnail"],
                    'category':data['genre'],
                    'numViews':data['views'],
                })
            else:
                break

        win.destroy()
        
            #labelx=Label(text=u+" ------------- done !",fontsize=10).pack()
            #canvas1.create_window(200, 100, window=labelx)

        #label3=Label(text="json created",fontsize=10).pack()
        #canvas1.create_window(200, 100, window=label2)
        #
        print(len(url),len(infos))
        if len(url)==len(infos):
            with open("sample.json", "w",encoding="utf-8") as outfile:
                json.dump(infos, outfile,ensure_ascii=False)
            return True
        else:
            return False

def interface():


        root= tk.Tk()
        root.title("script")
        canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
        canvas1.pack()

        label1 = tk.Label(root, text='Youtube Scraping')
        label1.config(font=('helvetica', 14))
        canvas1.create_window(200, 25, window=label1)

        label2 = tk.Label(root, text='Type your Keyword:')
        label2.config(font=('helvetica', 10))
        canvas1.create_window(200, 100, window=label2)

        entry1 = tk.Entry (root) 
        canvas1.create_window(200, 140, window=entry1)

        def getSquareRoot ():
            
            x1 = entry1.get()
            
            if get_infos(x1) == True:
                    labelx = tk.Label(root, text='Json file has been created Seccussfully !')
                    labelx.config(font=('helvetica', 14))
                    canvas1.create_window(200, 240, window=labelx)
            else:
                    labely = tk.Label(root, text='Something went Wrong !')
                    labely.config(font=('helvetica', 14))
                    canvas1.create_window(200, 240, window=labely)

            label1 = tk.Label(root, text='Youtube Scraping')
            label1.config(font=('helvetica', 14))
            canvas1.create_window(200, 25, window=label1)


            
        button1 = tk.Button(text='Start Scraping ', command=getSquareRoot, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
        canvas1.create_window(200, 180, window=button1)

   
        root.mainloop()



if __name__ == '__main__':
    interface()