import requests, subprocess, time, random, re, html

RTMP = "rtmp://a.rtmp.youtube.com/live2/1bkc-yr46-7yrj-ah1t-e13b"  # ← Replace with your stream key
count = 1252802
font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def get_person():
    while True:
        r = requests.get("https://en.wikipedia.org/w/api.php", params={
            "format":"json","action":"query","generator":"random",
            "grnnamespace":0,"grnlimit":1,"prop":"pageimages|extracts",
            "exintro":1,"piprop":"original","pilicense":"any"
        }).json()
        page = next(iter(r["query"]["pages"].values()))
        if "original" in page and re.search(r"\bBorn\b|\b(born|is)\b", html.unescape(page.get("extract","")), re.I):
            return page["title"], page["original"]["source"]

while True:
    try:
        name, img_url = get_person()
        img_data = requests.get(img_url, timeout=15).content
        with open("person.jpg","wb") as f: f.write(img_data)

        cmd = [
            "ffmpeg","-y","-loop","1","-i","person.jpg",
            "-stream_loop","-1","-i","bg_music.mp3",
            "-t","30",
            "-vf",f"drawtext=fontfile={font}:text='TOP {count} PEOPLE':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=40,"
                  f"drawtext=fontfile={font}:text='{name}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
            "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k",
            "-f","flv",RTMP
        ]
        p = subprocess.Popen(cmd); time.sleep(30); p.terminate(); count -= 1
    except Exception as e:
        print("error:",e); time.sleep(5)
