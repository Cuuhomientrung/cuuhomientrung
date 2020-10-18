from app.models import BadCase, BadTopic, Policy, Publisher, YoutubeClip
from app.celery_app import app
from app.browser_crawler import BrowserCrawler
from app.lib.utils import print_exception, check_keyword_filter
import datetime
import django
from django.conf import settings
from lxml import etree
import json
import random
import re
import requests_html
import requests
from torrequest import TorRequest
import subprocess

def check_publisher_available(html):
    html_tree = etree.HTML(html)

    # check if tai khoan bi xoa
    elements = html_tree.xpath("//node()[contains(text(),'Tài khoản này đã bị chấm dứt do vi phạm Điều khoản dịch vụ của YouTube')]")
    if elements:
        print("Channel này đã bị gỡ ")
        return False

    elements = html_tree.xpath("//node()[contains(text(),'chưa có trên miền của quốc gia này do có khiếu nại pháp lý của chính phủ')]")
    if elements:
        print("Channel này không hiển thị được ở Việt Nam")
        return False

    elements = html_tree.xpath("//node()[contains(text(),'Video không có sẵn')]")
    if elements:
        print("Channel này đã bị khoá ")
        return False

    return True


def reset_tor_IP():
    with TorRequest(proxy_port=9050, ctrl_port=9051, password=None) as tr:
        tr.reset_identity()

def get_tor_session():
    session = requests_html.HTMLSession()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session


def check_youtube_bad_content(clip):
    """Check for bad content in Youtube clip"""
    """
        @Return:
            - True: if found bad content. Bad content are created for item objects
            - False: this clip is ok
    """
    sentences = clip.content.split('.')
    clip_length = len(sentences)

    detected = False
    for index, sentence in enumerate(sentences, 1):
        lower_sentence = sentence.lower()
        all_filter = Policy.objects.all()
        for filter in all_filter:
            if filter.check_violate(lower_sentence):
                detected = True
                violation, _ = BadCase.objects.get_or_create(
                    item = item,
                    sentence = sentence,
                    position = str(int(index/clip_length * 100)) + "%",
                    violate = filter
                )
    if detected:
        clip.contain_bad_content = 1
        item.save()
    else:
        clip.contain_bad_content = 2
        item.save()
    return detected


def download_youtube_mp3(item, duration=1):
    """Download youtube mp3 file to /media/xxx.mp3 file for further processing"""
    """
        @Args:
            item: youtubeclip object
            duration: length of clip after downloaded
        @Return:
            True: success
            False: fail
    """

    # below command use youtube-dl to extract audio from youtube link and rename it to item.pk
    command = f"youtube-dl --extract-audio --audio-format mp3 { item.url } --postprocessor-args " + f'"-ss 00:00:00.00 -t 00:{duration}:00.00"' + " --exec 'mv {} " + f"{ item.pk }.mp3 '"
    print(command)
    subprocess.run(command, shell=True, cwd=settings.MEDIA_ROOT)

    #TODO: check result here
    return True

def parse_audio_to_text(item):
    """Use FPT.AI service to parse mp3 file to text"""
    """
        @Return
            text if success. And item.content is change with text
            False if need slow down
            None if fsh ail
    """
    print(f"Parsing youtube clip {item.url} ({item.title}) to text")
    url = 'https://api.fpt.ai/hmi/asr/general'
    full_path = settings.MEDIA_ROOT + '/' + str(item.pk) + '.mp3'
    payload = open(full_path, 'rb').read()
    headers = {
        'api-key': 'OMZL6bXNHHAOTk0AjG5KktWUNtfvZ6CO'
    }
    response = requests.post(url=url, data=payload, headers=headers, timeout=900)
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 0:
            text = result['hypotheses'][0]['utterance']
            item.content = text
            print(f"Content: {text}")
            item.save()
            print("OK")
            return text
        else:
            print("Task failed")
            print(f"Task status: {result['status']}")
            return None
    elif response.status_code == 429: # too many request
        print("FPT AI Too Many Request Error")
        return False
    else:
        print("FPT AI Request Error")
        print(f"Status Code: {response.status_code}")
        return None


def parse_view(view_text):
    result = re.match(r'([\d\.]+) (.*)', view_text)
    if result:
        views = int(result.group(1).replace('.', ''))
        return views
    else:
        print(f"Can't parse views from {view_text}")
        return None

def parse_publish_date(date_text):
    now = django.utils.timezone.localtime()
    result = re.match(r'(.*)(\d+) (.*)', date_text)
    if result:
        duration = int(result.group(2))
        date_type = result.group(3)

        if "năm" in date_type:
            publish_date = now - datetime.timedelta(days=duration*365)
        elif "tháng" in date_type:
            publish_date = now - datetime.timedelta(days=duration*30)
        elif "tuần" in date_type:
            publish_date = now - datetime.timedelta(days=duration*7)
        elif "ngày" in date_type:
            publish_date = now - datetime.timedelta(days=duration)
        elif "giờ" in date_type:
            publish_date = now - datetime.timedelta(hours=duration)
        elif "phút" in date_type:
            publish_date = now - datetime.timedelta(minutes=duration)
        else:
            print(f"Can't parse publish date with {date_type}")
            return None

        return publish_date
    else:
        print(f"Can't parse publish date with {date_text}")
        return None


def parse_length(length_text):
    """Parse Youtube length from text"""
    time = length_text.split(':')
    if len(time) == 2: # minute and second
        duration = int(time[0]) * 60 + int(time[1])
    elif len(time) == 3: # hour, minute and second
        duration = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
    else:
        print(f"Unknown time format {length_text}")
        return None
    return duration

def get_search_videos(keyword):
    """Get videos from Youtube search"""
    if True:
        session = get_tor_session()

        videos = []

        search_url = "https://www.youtube.com/results?search_query=" + '+'.join(keyword.split())

        result = session.get(search_url,  timeout=30)

        if result.status_code == 200:
            # print("Connect successfully")
            script = 'JSON.stringify(window["ytInitialData"].contents.twoColumnSearchResultsRenderer.primaryContents.sectionListRenderer.contents[0].itemSectionRenderer.contents)'
            html = str(result.html.render(script=script, timeout=20))
            data = json.loads(html)

            for item in data:
                if 'videoRenderer' in item:
                    video = item['videoRenderer']
                    title = video['title']['runs'][0]['text']
                    url = "https://www.youtube.com/watch?v=" + video['videoId']

                    try:
                        views_text = video['viewCountText']['simpleText']
                        views = parse_view(views_text)
                    except:
                        views_text = ''
                        views = 0
                    try:
                        publish_date = video['publishedTimeText']['simpleText']
                        publish_date = parse_publish_date(publish_date)
                    except:
                        publish_date = None

                    try:
                        length_text  = video['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['simpleText']
                        length = parse_length(length_text)
                    except:
                        length_text = ''
                        length = 0

                    try: # get channel name and url
                        publisher_url = "https://youtube.com" + video['ownerText']["runs"][0]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]['url']
                        publisher_name = video['ownerText']["runs"][0]["text"]
                    except:
                        publisher_name = None
                        publisher_url = None

                    # append result
                    videos.append(
                        {
                            'title': title,
                            'url': url,
                            'views': views,
                            "views_text": views_text,
                            "length": length,
                            "length_text": length_text,
                            "publish_date": publish_date,
                            "publisher_name": publisher_name,
                            "publisher_url": publisher_url
                        }
                    )

        elif result.status_code == 429: # too many requests
            print("Current IP has been blocked. Change IP")
            reset_tor_IP()
            # reset tor to get new IP
            pass
        else:
            print(f"Unknow error: {result.status_code}")
    # except:
    #     print_exception()
    #     print(f"Can't track videos for publisher {channel_url}")
    #     return None

    return videos


def get_publisher_videos(channel_url):
    try:
        session = get_tor_session()


        videos = []

        if channel_url[-1] == '/':
            channel_url = channel_url + 'videos?view=0&sort=dd&flow=grid'
        else:
            channel_url = channel_url + '/videos?view=0&sort=dd&flow=grid'

        result = session.get(channel_url,  timeout=30)

        if result.status_code == 200:
            # print("Connect successfully")
            script = 'JSON.stringify(window["ytInitialData"].contents.twoColumnBrowseResultsRenderer.tabs[1].tabRenderer.content.sectionListRenderer.contents[0].itemSectionRenderer.contents[0].gridRenderer.items)'
            html = str(result.html)

            if not check_publisher_available(html): # channel not available
                return None

            html = str(result.html.render(script=script, timeout=20))
            data = json.loads(html)

            for item in data:
                if 'gridVideoRenderer' not in item:
                    return None

                video = item['gridVideoRenderer']
                title = video['title']['runs'][0]['text']
                url = "https://www.youtube.com/watch?v=" + video['videoId']

                try:
                    views_text = video['viewCountText']['simpleText']
                    views = parse_view(views_text)
                except:
                    views_text = ''
                    views = 0

                publish_date = video['publishedTimeText']['simpleText']
                publish_date = parse_publish_date(publish_date)

                try:
                    length_text  = video['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['simpleText']
                    length = parse_length(length_text)
                except:
                    length_text = ''
                    length = 0

                # append result
                videos.append(
                    {
                        'title': title,
                        'url': url,
                        'views': views,
                        "views_text": views_text,
                        "length": length,
                        "length_text": length_text,
                        "publish_date": publish_date
                    }
                )

        elif result.status_code == 429: # too many requests
            print("Current IP has been blocked. Change IP")
            reset_tor_IP()
            # reset tor to get new IP
            pass
        else:
            print(f"Unknow error: {result.status_code}")
    except:
        print_exception()
        print(f"Can't track videos for publisher {channel_url}")
        return None

    return videos


@app.task(name='track_publisher')
def track_publisher(max_publisher=10, min_duration=60):
    """Check random publisher for new videos"""
    """
        @Args:
            max_publisher: number of publisher to check
            min_duration : min time passed from last track to re track publisher channel
        @Return:
            [{
                'publisher': publisher pk,
                'videos':[
                    {
                        'title':
                        'url':
                        'publish_date':
                        'length':
                    }
                ]
            }]
    """

    random_publishers = random.choices(Publisher.objects.filter(tracking=True).all(), k=max_publisher)
    now = django.utils.timezone.now()

    result = []

    for publisher in random_publishers:
        print(f"Tracking publisher {publisher.name}")
        time_pass = int((now - publisher.last_track_date).total_seconds() / 60)
        if time_pass >= 60: # 1 hous
            publisher.last_track_date = now
            publisher.save()

            channel_url = publisher.url
            videos = get_publisher_videos(channel_url)

            if videos:
                # append video to database
                print(f"Finding {len(videos)} videos from this publisher")
                count = 0
                for clip in videos:
                    video, created = YoutubeClip.objects.get_or_create(
                        title = clip['title'],
                        url   = clip['url'],
                        views = clip['views'],
                        views_text= clip['views_text'],
                        length = clip['length'],
                        length_text= clip['length_text'],
                        # publish_date= clip['publish_date'],
                        publisher = publisher
                    )
                    if created:
                        # fix publish_date error
                        video.publish_date = clip['publish_date']
                        video.save()

                        count += 1
                    else:
                        # fix publish_date error
                        if video.publish_date != clip['publish_date']:
                            video.publish_date = clip['publish_date']
                            video.save()

                print(f"Adding {count} new video from this publisher")
                print()

                # append to result
                result.append({
                    'publisher': publisher.pk,
                    'videos': videos
                }
                )

    return result

@app.task(name='track_topic')
def track_topic(max_topic=10, min_duration=60):
    """Check random topic for new videos"""
    """
        @Args:
            max_topic: number of topic to check
            min_duration : min time passed from last track to re track publisher channel
        @Return:
            [{
                'topic': topic pk,
                'videos':[
                    {
                        'title':
                        'url':
                        'publish_date':
                        'length':
                        'publisher_name',
                        'publisher_url'
                    }
                ]
            }]

            Note:
                - auto add video into database. Check topic criteria on title before add into database
                - auto create publisher if doesn't have
    """

    random_topics = random.choices(BadTopic.objects.filter(tracking=True).all(), k=max_topic)
    now = django.utils.timezone.now()

    result = []

    for topic in random_topics:
        print(f"Tracking topic {topic.name}")
        time_pass = int((now - topic.last_track_date).total_seconds() / 60)
        if time_pass <= 60: # 1 hous
            topic.last_track_date = now
            topic.save()

            search_keyword = topic.search_keyword
            videos = get_search_videos(search_keyword)

            if videos:
                # append video to database
                print(f"Finding {len(videos)} videos from this topic")
                count = 0
                for clip in videos:

                    # check criteria
                    if topic.result_filter:
                        if not check_keyword_filter(topic.main_keyword, topic.support_keyword, topic.exclude_keyword):
                            continue # ignore this video

                    # check publisher
                    publisher = Publisher.objects.filter(
                            url = clip['publisher_url']
                        ).first()

                    if not publisher: # new publisher
                        if topic.auto_add_publisher: # add to database
                            publisher = Publisher.objects.create(
                                name = clip['publisher_name'],
                                url = clip['publisher_url']
                            )

                    video, created = YoutubeClip.objects.get_or_create(
                        title = clip['title'],
                        url   = clip['url'],
                        views = clip['views'],
                        views_text= clip['views_text'],
                        length = clip['length'],
                        length_text= clip['length_text'],
                        # publish_date= clip['publish_date'],
                        publisher = publisher,
                    )

                    if created:
                        # fix publish_date error
                        video.publish_date = clip['publish_date']
                        video.topic = topic
                        video.save()
                        count += 1
                    else:
                        # fix publish_date error
                        if video.publish_date != clip['publish_date']:
                            video.publish_date = clip['publish_date']
                            video.save()

                print(f"Adding {count} new video from this topic")
                print()

                # append to result
                result.append({
                    'publisher': publisher.pk,
                    'videos': videos
                }
                )

    return result


@app.task(rate_limit='20/m')
def check_youtube_link(item_pk):
    """Check youtube link status by parsing html"""
    """
        @return
            change item.status with value:
                0: chưa xử lý
                1: đang xử lý
                2: video không có sẵn do tài khoản bị khoá
                3: video bị gỡ
                4: video bình thường
                5: link bị lỗi, không mở được
    """
    item = YoutubeClip.objects.filter(pk=item_pk).first()

    if not item:
        print(f"Can't find item {item_pk}")
        return None

    print(f"Checking youtube url {item.url}")

    session = get_tor_session()
    result = session.get(item.url,data=None, timeout=30)

    if result.status_code == 200:
        html = result.text
        html_tree = etree.HTML(html)

        # check if tai khoan bi xoa
        elements = html_tree.xpath("//node()[contains(text(),'tài khoản YouTube được kết hợp với video này đã bị chấm dứt')]")
        if elements:
            item.live_status = 2
            item.save()
            return None

        elements = html_tree.xpath("//node()[contains(text(),'chưa có trên miền của quốc gia này do có khiếu nại pháp lý của chính phủ')]")
        if elements:
            item.live_status = 3
            item.save()
            return None

        elements = html_tree.xpath("//node()[contains(text(),'Video không có sẵn')]")
        if elements:
            item.live_status = 0
            item.save()
            return None

        item.live_status = 4
        item.save()
    elif result.status_code == 429: # too many requests
        print(f"Too many requests. Can't check url {item.url} now ")
        reset_tor_IP()
    else:
        item.live_status = 5
        item.save()


@app.task(name='check_youtube_live_status')
def check_youtube_live_status():
    undone_task = YoutubeClip.objects.filter(live_status=0) | YoutubeClip.objects.filter(live_status=3) | YoutubeClip.objects.filter(live_status=1)# unchecked or still alived link
    for item in undone_task:
        if item.live_status == 0: # uncheck yet
            item.live_status = 1 # change to checking
            item.save()
        check_youtube_link(item.pk)


@app.task(name='parse_youtube_clip_to_text')
def parse_youtube_clip_to_text(max_clip=5, duration=3):
    """Parse videocip voice to text for further analysis"""
    """
        @Note: only parse video that mentions to VIP (to save API money). Priotiry on lastest video
    """
    # uu tien boc lastest video & mention to VIP
    clips = YoutubeClip.objects.filter(bad_content_status=0, mentions__isnull=False).all().order_by('-publish_date') # unchecked yet
    choices = clips[:max_clip]
    # choices = random.choices(clips, k=max_clip)

    for clip in choices:
        download_youtube_mp3(clip, duration=3)
        result = parse_audio_to_text(clip)
        if result:
            clip.bad_content_status = 1 # parse voice to text
            clip.save()
        elif result == False: # too many request, need slow down
            time.sleep(30)
        else: # error
            pass


@app.task(name='check_VIP_mention')
def check_VIP_mention():
    """Check clip for VIP mentions"""

    # check mention for unchecked clip (check with title)
    check_clips = YoutubeClip.objects.filter(mention_status=0)
    for clip in check_clips:
        clip.check_VIP_mention(level=1)
        clip.mention_status = 1 # finish check mention in title
        clip.save()

    # check mention for checked clip with finish parse audio to text
    check_clips = YoutubeClip.objects.filter(mention_status=1, bad_content_status__gt=1)
    for clip in check_clips:
        clip.check_VIP_mention(level=2)
        clip.mention_status = 2 # finish check mention in content
        clip.bad_content_status = 2 # finish check VIP mention
        clip.save()
