import time
import requests
import hashlib
import json
import re
import os

class KuGouDownloader:
    def __init__(self):
        self.search_url = 'https://complexsearch.kugou.com/v2/search/song'
        self.info_url = 'https://wwwapi.kugou.com/play/songinfo'
        self.hash_salt = 'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://www.kugou.com/"
        }
        # 公共参数
        self.common_params = {
            "mid": "03ac0822019ff78d1a7392ec36531bbc",
            "uuid": "03ac0822019ff78d1a7392ec36531bbc",
            "dfid": "3f0boF2vfm4o1UoV0B23LTN6",
            "appid": "1014",
            "srcappid": "2919",
            "token": "2b4a7b2f9250d17077b7b8568d52a16760e7384380402dab092f9f40d03f6de9",
            "userid": "2537388275"
        }

    def _generate_signature(self, params_dict):
        """生成酷狗签名的通用方法"""
        # 1. 按照参数名排序（这是酷狗这类API的常规逻辑，但此处遵循你提供的特定拼接顺序）
        # 如果顺序不对，API会返回签名错误。这里采用你代码中的拼接方式：
        # Salt + 拼接字符串 + Salt
        concat_str = "".join([f"{k}={v}" for k, v in params_dict.items()])
        sign_str = f"{self.hash_salt}{concat_str}{self.hash_salt}"
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    def search_songs(self, keyword):
        """搜索歌曲并返回列表"""
        timestamp = str(int(time.time() * 1000))
        params = {
            "callback": "callback123",
            "keyword": keyword,
            "page": "1",
            "pagesize": "30",
            "bitrate": "0",
            "isfuzzy": "0",
            "inputtype": "0",
            "platform": "WebFilter",
            "iscorrection": "1",
            "privilege_filter": "0",
            "filter": "10",
            "clientver": "1000",
            "clienttime": timestamp,
            **self.common_params
        }
        # 注意：拼接顺序必须严格一致，这里按你提供的顺序手动校对
        # 为了保证100%成功，直接使用你之前的逻辑构建sign
        sign_params = ['appid', 'bitrate', 'callback', 'clienttime', 'clientver', 'dfid', 'filter', 'inputtype', 'iscorrection', 'isfuzzy', 'keyword', 'mid', 'page', 'pagesize', 'platform', 'privilege_filter', 'srcappid', 'token', 'userid', 'uuid']
        sorted_concat = "".join([f"{k}={params[k]}" for k in sorted(sign_params)])
        params['signature'] = hashlib.md5((self.hash_salt + sorted_concat + self.hash_salt).encode('utf-8')).hexdigest()

        try:
            resp = requests.get(self.search_url, params=params, headers=self.headers)
            # 正则提取 JSON
            json_str = re.search(r'callback123\((.*)\)', resp.text).group(1)
            data = json.loads(json_str)
            return data.get('data', {}).get('lists', [])
        except Exception as e:
            print(f"搜索失败: {e}")
            return []

    def get_song_details(self, emix_id):
        """获取歌曲播放地址"""
        timestamp = str(int(time.time() * 1000))
        params = {
            "album_audio_id": "", # 部分接口需要
            "clienttime": timestamp,
            "clientver": "20000",
            "dfid": "3f0boF2vfm4o1UoV0B23LTN6",
            "encode_album_audio_id": emix_id,
            "mid": "03ac0822019ff78d1a7392ec36531bbc",
            "platid": "4",
            "srcappid": "2919",
            "token": "2b4a7b2f9250d17077b7b8568d52a16760e7384380402dab092f9f40d03f6de9",
            "userid": "2537388275",
            "uuid": "03ac0822019ff78d1a7392ec36531bbc",
            "appid": "1014"
        }
        
        # 详情接口签名拼接顺序
        keys = sorted(params.keys())
        concat_str = "".join([f"{k}={params[k]}" for k in keys])
        params['signature'] = hashlib.md5((self.hash_salt + concat_str + self.hash_salt).encode('utf-8')).hexdigest()

        try:
            resp = requests.get(self.info_url, params=params, headers=self.headers)
            return resp.json().get('data', {})
        except Exception as e:
            print(f"获取详情失败: {e}")
            return {}

    def download_song(self, song_info):
        """执行下载"""
        play_url = song_info.get('play_url')
        if not play_url:
            print("错误：该歌曲可能需要付费或无版权，无法获取播放链接。")
            return

        file_name = f"{song_info.get('audio_name', '未知')}.mp3"
        # 简单过滤非法字符
        file_name = re.sub(r'[\\/:*?"<>|]', '_', file_name)

        print(f"正在下载: {file_name}...")
        try:
            content = requests.get(play_url, headers=self.headers).content
            with open(file_name, 'wb') as f:
                f.write(content)
            print(f"下载成功！文件保存为: {os.path.abspath(file_name)}")
        except Exception as e:
            print(f"文件保存失败: {e}")

def main():
    api = KuGouDownloader()
    keyword = input("请输入要搜索的歌曲名: ")
    songs = api.search_songs(keyword)

    if not songs:
        print("未找到相关歌曲。")
        return

    print(f"\n{'序号':<4} {'歌名':<30} {'歌手':<20}")
    print("-" * 60)
    for i, song in enumerate(songs):
        print(f"{i+1:<4} {song.get('SongName', 'Unknown'):<30} {song.get('SingerName', 'Unknown'):<20}")

    try:
        choice = int(input("\n请输入要下载的歌曲序号 (0退出): "))
        if choice == 0: return
        
        selected_song = songs[choice-1]
        emix_id = selected_song.get('EMixSongID')
        
        print("\n正在获取播放地址...")
        details = api.get_song_details(emix_id)
        api.download_song(details)
        
    except (ValueError, IndexError):
        print("输入无效。")

if __name__ == "__main__":
    main()