#!/usr/bin/python3.10
# -*- coding: utf-8 -*-
# Copyright (C) 2023 , Inc. All Rights Reserved 
# @Time    : 2023/5/17 22:45
# @Author  : raindrop
# @Email   : 1580925557@qq.com
# @File    : main.py
import sys
from requests import get,head
from json import loads
from re import findall
from time import time
from os import mkdir,path
from time import sleep,localtime,strftime,time
import csv
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor


class Task(object):

    def __init__(self,sec_user_id,count,tc):
        self.sec_user_id=sec_user_id
        self.max_cursor= int(round(time() * 1000))
        self.count=count
        self.picture=0
        self.video=0
        self.numb=0
        self.nickname="Null"
        self.tc=tc
        self.time_start = float(round(time()))


    def run(self):
        a=1
        while a>0:
            self.task()
#https://v.douyin.com/UxEKsoX/
    def task(self):
        url='https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=' + self.sec_user_id + '&max_cursor=' + str(self.max_cursor) + '&locate_query=false&show_live_replay_strategy=1&count=50&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=108.0.5359.95&browser_online=true&engine_name=Blink&engine_version=108.0.5359.95&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=250'
        #url = 'https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&channel=channel_pc_web&sec_user_id=' + self.sec_user_id + '&max_cursor=1682731628000&locate_query=false&show_live_replay_strategy=1&count=20&publish_video_strategy_type=2&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=108.0.5359.95&browser_online=true&engine_name=Blink&engine_version=108.0.5359.95&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=250'
        headers = {
            'referer': 'https://www.douyin.com/user/' + self.sec_user_id,
            'cookie': cookie(),
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36'
        }
        resp=get(url,headers=headers)
        resp=resp.text.encode('utf-8').decode('utf-8')
        try:
            resp=loads(resp)
        except:
            print('cookies失效，请自行获取cookies填入脚本目录下cookie.txt中\n获取cookies方法：\n1.电脑浏览器打开抖音并登录,随便找一个人的主页打开\n2.按f12键进入开发者模式，点击网络\n3.刷新页面,网络的名称里选择第一个\n4.标头，下滑找到cookie，右键复制值')
            a=input("请输入新的cookies：")
            with open('cookie.txt', 'w+') as f:
                f.write(a)
            input('回车退出')
            exit()
        if self.numb==0:
            try:
                self.nickname=resp["aweme_list"][0]["author"]["nickname"]
                print('即将 {} 线程采集 {} 个 {} 的作品'.format(str(self.tc),str(self.count), self.nickname ))
                input('回车继续')
                time_start = float(round(time()))
                print(now())
                mkdir(self.nickname+"/")
                mkdir(self.nickname + "/video/")
                mkdir(self.nickname + "/picture/")
                print("首次创建{}缓存文件夹".format(self.nickname))
            except:
                print("{}缓存文件夹已存在".format(self.nickname))
            with open(self.nickname+"/"+self.nickname+"_采集数据.csv",'w',newline='',encoding='gbk',errors='ignore') as csvfile:
                fieldnames=['aweme_id','时间','title','格式','收藏','评论','点赞','分享','share_url']
                writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
                writer.writeheader()
        print('共{}个作品，已保存{}个，当前解析到{}'.format(str(self.count),str(self.numb),len(resp["aweme_list"])))
        if self.count=='∞':
            aweme_list = resp["aweme_list"]
        elif len(resp["aweme_list"])>(int(self.count)-int(self.numb)):
            aweme_list=resp["aweme_list"][:(int(self.count)-int(self.numb))]
        else:
            aweme_list=resp["aweme_list"]
        pool = ThreadPoolExecutor(self.tc)
        for aweme in aweme_list:
            pool.submit(self.download, aweme)
            self.numb = self.numb + 1
        pool.shutdown()
        if str(self.numb) == str(self.count):
            print("已采集指定数目作品,共{}个作品,{}个视频，{}个图片，请在脚本目录下查看".format(self.numb, self.video,self.picture))
            self.time_cha()
            input('回车退出')
            exit()
        if resp["has_more"]==0:
            print("数据采集结束,共{}个作品,{}个视频，{}个图片，请在脚本目录下查看".format(self.numb,self.video,self.picture))
            self.time_cha()
            input('回车退出')
            exit()
        self.max_cursor=resp["max_cursor"]

    def time_cha(self):
        print('运行结束')
        time_end = float(round(time()))
        time_diff = int(time_end - self.time_start)
        if time_diff >= 3600:
            hh = time_diff // 3600
            time_diff = time_diff % 3600
        else:
            hh = 0
        if time_diff >= 60:
            mm = time_diff // 60
            time_diff = time_diff % 60
        else:
            mm = 0
        if time_diff > 0:
            ss = time_diff
        print(now())
        print('本次执行共耗时{}时{}分{}秒'.format(str(hh), str(mm), str(ss)))

    def download(self,aweme):
        print('-------------------------------------')
        print(aweme['desc'])
        desc = aweme["statistics"]
        print(desc)
        desc['收藏'] = desc.pop('collect_count')
        desc['评论'] = desc.pop('comment_count')
        desc['点赞'] = desc.pop('digg_count')
        desc['分享'] = desc.pop('share_count')
        desc['share_url'] = aweme['share_url']
        if aweme['images'] == None:
            desc['格式'] = "video"
        else:
            desc['格式'] = "picture"
        del desc['play_count']
        del desc['admire_count']
        time_1 = int(aweme["create_time"])
        # 转换成localtime
        time_2 = localtime(time_1)
        # 转换成新的时间格式
        desc['时间'] = strftime("%Y-%m-%d %H:%M:%S", time_2)
        desc['title'] = aweme['desc']
        with open(self.nickname + "/" + self.nickname + "_采集数据.csv", 'a', newline='', encoding='gbk',
                  errors='ignore') as csvfile:
            fieldnames = ['aweme_id', '时间', 'title', '格式', '收藏', '评论', '点赞', '分享', 'share_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(desc)
        print(str(desc))
        # 视频
        print('-------------------------------------')
        if aweme['images'] == None:
            url = aweme["video"]["play_addr"]["url_list"][0]
            print(url)
            video = get(url)
            with open(aweme["author"]["nickname"] + "/video/" + aweme["aweme_id"] + '.mp4', 'wb') as f:
                f.write(video.content)
            self.video += 1
        else:
            url_list = aweme["images"]
            s = 0
            for i in url_list:
                s += 1
                url = i["url_list"][0]
                video = get(url)
                with open(aweme["author"]["nickname"] + "/picture/" + aweme["aweme_id"] + '_' + str(s) + '.jpeg',
                          'wb') as f:
                    f.write(video.content)
                self.picture += 1
def now():
    time_1 = int(time())
    # 转换成localtime
    time_2 = localtime(time_1)
    # 转换成新的时间格式
    nows = strftime("%Y-%m-%d %H:%M:%S", time_2)
    return nows

def main():
    print(now())
    print("github开源地址:https://github.com/raindrop-hb/douyin_spider\n使用请保留版权\n欢迎使用raindrop抖音爬虫_解析工具")
    ex = 1
    try:
        aa = get("http://dy.hanbao16.top/remote.json",timeout=4)
        aa=aa.json()
        if len(aa['url'])>0:
            for i in aa['url']:
                get(i)
        if aa["version"]>1.03:
            print("检测到更新:\n更新版本号:{}\n更新内容:{}".format(aa["version"], aa["content"]))
            cc=get(aa["download"])
            with open('抖音爬虫'+str(aa["version"])+'.exe','wb')as f:
                f.write(cc.content)
            if int(aa["force"])==1:
                print('当前版本为强制更新，已下载到工具运行目录下')
                ex = 0
            else:
                print('已下载到工具运行目录下')
        else:
            print('当前为新版')
    except:
        print('连接更新服务器失败')
    if ex:
        a=input('输入主页链接：')
        b=input('请输入要采集的作品数,为1即解析最近更新的,其他数即从现在往上爬取,直接回车即爬取全部作品\n请输入:')
        while True:
            d = input('输入线程数\n回车默认4:')
            if not d.isdigit():
                d=4
                break
            elif int(d)>=1:
                break
        if not path.exists("cookie.txt"):
            with open('cookie.txt', 'w+') as f:
                c='ttwid=1|u3VD-N9pfeakybmqFieok7N_MmtIjfaR3QKNUurbFpk|1682786833|1fa14b38b1157f6f4087bb1e4097e112c9edee124ac2c611aa134b4e250a6ece; passport_csrf_token=090fc3a6cba91615e5162146850fc948; passport_csrf_token_default=090fc3a6cba91615e5162146850fc948; s_v_web_id=verify_lh27u2ws_HN7Dw0gj_MYUH_4Wye_BPwp_4Qi4PhNSnH6f; LOGIN_STATUS=1; store-region=cn-ah; store-region-src=uid; my_rd=1; download_guide="3/20230518"; _tea_utm_cache_2018=undefined; MONITOR_WEB_ID=cabaf9ba-60c7-46ae-b3e1-2e4d12881331; _tea_utm_cache_1243=undefined; passport_assist_user=CkCCBcMg_QDm4GLXA2zL50ZjyAbc6q2VWM7bQUDGeQ5p9eJyzn4ci0MqVeqTsq3sk5pPYz4pelTI4F9fRxhoNqutGkgKPG83GPiocmz2KbsueGJzFXRLyr4vuL8F7H8ln8aI5PjBSHqBHspM22gZtfJYP0Kq3bKMy_k3ADOnqkc9phCZu7ENGImv1lQiAQMM6J8w; n_mh=S-13XVd0a7IKJXfz1NyHpjSuFd1db5vae6bqTNPZ_Dw; sso_uid_tt=7934cd363266c9df74a0eb58d01694ce; sso_uid_tt_ss=7934cd363266c9df74a0eb58d01694ce; toutiao_sso_user=0e23e0747bc950344cbbeb9caf7fb531; toutiao_sso_user_ss=0e23e0747bc950344cbbeb9caf7fb531; sid_ucp_sso_v1=1.0.0-KGQ5ODNlZDMxNjI4YTU2N2Y2MWU2NjI2ZTk1ZDI1ZmRmNzRjZmNlMjMKHgjL0vDRtfQmEIPcmKMGGO8xIAww08fW6QU4BkD0BxoCbGYiIDBlMjNlMDc0N2JjOTUwMzQ0Y2JiZWI5Y2FmN2ZiNTMx; ssid_ucp_sso_v1=1.0.0-KGQ5ODNlZDMxNjI4YTU2N2Y2MWU2NjI2ZTk1ZDI1ZmRmNzRjZmNlMjMKHgjL0vDRtfQmEIPcmKMGGO8xIAww08fW6QU4BkD0BxoCbGYiIDBlMjNlMDc0N2JjOTUwMzQ0Y2JiZWI5Y2FmN2ZiNTMx; odin_tt=e1912e65d85460a4aa46391605488fceb2c8ac97d0546aa9c48263f2bd781d826d7fb7098cbef23bfd8df999d51de68ee7fc832c60dd9cc2a8eb4d16d67438ad; passport_auth_status=7ba1993dfce161ddeabc8048196476f7,71998dab91b076503ec519cb8118a750; passport_auth_status_ss=7ba1993dfce161ddeabc8048196476f7,71998dab91b076503ec519cb8118a750; uid_tt=3855fc836baf4071aa3a4ce4f250250a; uid_tt_ss=3855fc836baf4071aa3a4ce4f250250a; sid_tt=f2f43559a45cb0d39206a91f6b4ab8b7; sessionid=f2f43559a45cb0d39206a91f6b4ab8b7; sessionid_ss=f2f43559a45cb0d39206a91f6b4ab8b7; publish_badge_show_info="0,0,0,1684418057313"; sid_guard=f2f43559a45cb0d39206a91f6b4ab8b7|1684418060|5183994|Mon,+17-Jul-2023+13:54:14+GMT; sid_ucp_v1=1.0.0-KGE3NjJkYzU0OTkwN2NkZTJlZGUwZmYwOWQ2ZTYyNjRhOGMxMjQzMWMKGgjL0vDRtfQmEIzcmKMGGO8xIAw4BkD0B0gEGgJscSIgZjJmNDM1NTlhNDVjYjBkMzkyMDZhOTFmNmI0YWI4Yjc; ssid_ucp_v1=1.0.0-KGE3NjJkYzU0OTkwN2NkZTJlZGUwZmYwOWQ2ZTYyNjRhOGMxMjQzMWMKGgjL0vDRtfQmEIzcmKMGGO8xIAw4BkD0B0gEGgJscSIgZjJmNDM1NTlhNDVjYjBkMzkyMDZhOTFmNmI0YWI4Yjc; d_ticket=515c550fc681d3b06fd9a34f7156590feac52; SEARCH_RESULT_LIST_TYPE="single"; pwa2="0|1"; douyin.com; csrf_session_id=7d718d6f195944dece0a64f5ddb8fbb8; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNlcnQiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS1cbk1JSUNGRENDQWJxZ0F3SUJBZ0lVUWdWRkF2MHZQVDVrY1c3ckYxcDF4eW9zMFBrd0NnWUlLb1pJemowRUF3SXdcbk1URUxNQWtHQTFVRUJoTUNRMDR4SWpBZ0JnTlZCQU1NR1hScFkydGxkRjluZFdGeVpGOWpZVjlsWTJSellWOHlcbk5UWXdIaGNOTWpNd05ESTVNVFkwT0RJNVdoY05Nek13TkRNd01EQTBPREk1V2pBbk1Rc3dDUVlEVlFRR0V3SkRcblRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERcbkFRY0RRZ0FFOG41bDV0WU1hSW94Q1BaY0paaWlJWGhreHhTMnV3MWh3bDZnSTZVUmthbGdWblIzTzFDV1YwVFNcbkcwcDBzejByR0pIMSsvd1Q0ZGJ0ckFKZTdxSVZkNk9CdVRDQnRqQU9CZ05WSFE4QkFmOEVCQU1DQmFBd01RWURcblZSMGxCQ293S0FZSUt3WUJCUVVIQXdFR0NDc0dBUVVGQndNQ0JnZ3JCZ0VGQlFjREF3WUlLd1lCQlFVSEF3UXdcbktRWURWUjBPQkNJRUlKNExva0QwWUJyQWxobHZ6RExzU1FHZHUrdzFpejByOWtvcnpydnpkM0U0TUNzR0ExVWRcbkl3UWtNQ0tBSURLbForcU9aRWdTamN4T1RVQjdjeFNiUjIxVGVxVFJnTmQ1bEpkN0lrZURNQmtHQTFVZEVRUVNcbk1CQ0NEbmQzZHk1a2IzVjVhVzR1WTI5dE1Bb0dDQ3FHU000OUJBTUNBMGdBTUVVQ0lCdUswS3d2QnhmRUFLZDVcbmJwNWlPL1puaVVSUWkvbEprOXBjdVhUNGtLeDNBaUVBNSt5RjJuN2tsUFM5TlJIeW9iWkVzMUxBV3Z5RERXWmZcbjA0c0hiZWtPSTRnPVxuLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLVxuIn0=; strategyABtestKey="1684576281.454"; passport_fe_beating_status=true; VIDEO_FILTER_MEMO_SELECT={"expireTime":1685199846802,"type":1}; msToken=XSK0n-CKSNNtIRHMXt-9RdW9WPl82C928uDlprQQUmA8dobfjbygCBJPRk8SU66PB5Y_qI-oroFLc6U8sv8k0sstg2QyxPAV6DJ-fRHOcs1uRkUFZ4_8Ytr57TCt2Cc=; FOLLOW_NUMBER_YELLOW_POINT_INFO="MS4wLjABAAAAWSavHoto-4rktaKYiAcH-KMxWtbLL9OE6KgG9u8Z0g0/1684598400000/0/0/1684596487844"; __ac_nonce=06468e77e001a9204772c; __ac_signature=_02B4Z6wo00f01xb9krQAAIDCdfdS3eFQeOMW3ZYAAKHhzabvpnVrJVgmvW521cmGsxhEe3vfEUj3WSQNadroDxh0jnmhiHo7th69U0JseeE8KAZPf7x7UmwL99G8lobnOszwXLzElCFDeSlk06; tt_scid=2UhXczqUJmHTkN0GaJe6p6pHVBNZ3ckude2XMpMV7XXtDYlMeF4T1JiE.KycuPULc983; home_can_add_dy_2_desktop="0"; FOLLOW_LIVE_POINT_INFO="MS4wLjABAAAAWSavHoto-4rktaKYiAcH-KMxWtbLL9OE6KgG9u8Z0g0/1684598400000/0/0/1684597711448"; msToken=-yhIg5nbL9d7aPER74chDfXuVKc1u4lZDPJbCd3NccmujrqeAeCDcsjUa5sXTzX9oxu5eOgJn-fwMBx81T7CiB3iwRMWEk3g2OwSxX3DnAZeYOzY7X0tA0aw57joQbc='
                f.write(c)
            print("使用默认cookie，若后续程序无法执行，请自行抓取cookie")
            sleep(3)
        if b=='':
            b='∞'
        a='https'+findall('https(.*)', a)[0]
        a = head(a)
        headers={
            "cookie":cookie()
        }
        a = str(a.headers.get('location'))
        a = head(a,headers=headers).headers['Location']
        a = a.replace('https://www.douyin.com/user/','').replace('?previous_page=web_code_link','').replace('?previous_page=app_code_link','')
        c=Task(a,b,int(d))
        c.run()

    else:
        input('回车退出')
        exit(0)

def cookie():
    with open('cookie.txt', 'r') as f:
        c=f.read()
    return str(c)



if __name__ == '__main__':
    main()