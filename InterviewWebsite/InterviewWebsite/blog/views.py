import json, os, random

from datetime import datetime
from django.shortcuts import render
from .models import Comment, Author
from django.shortcuts import redirect


def get_content_json():
    with open(os.path.join(os.path.dirname(__file__), 'testData/content_api.json'), 'r', encoding='latin') as f:
        content_json = json.load(f)
    return content_json


def get_quote_json():
    with open(os.path.join(os.path.dirname(__file__), 'testData/quotes_api.json'), 'r', encoding='latin') as f:
        content_json = json.load(f)
    return content_json


def get_inst_details(instruments, quote_json):
    for inst in quote_json:
        if inst["InstrumentId"] in instruments.keys():
            instruments[inst["InstrumentId"]]["name"] = inst["CompanyName"]
            instruments[inst["InstrumentId"]]["exchange"] = inst["Exchange"]
            instruments[inst["InstrumentId"]]["ticker"] = inst["Symbol"]
            instruments[inst["InstrumentId"]]["last"] = inst["CurrentPrice"]["Amount"]
            instruments[inst["InstrumentId"]]["change"] = inst["Change"]["Amount"]
            instruments[inst["InstrumentId"]]["change_percent"] = inst["PercentChange"]["Value"]
    return instruments


def parse_json_base(json_data):
    data = {}
    data["headline"] = json_data["headline"]
    data["byline"] = json_data["byline"]
    data["promo"] = json_data["promo"]
    data["created"] = datetime.strptime(json_data["created"], '%Y-%m-%dT%H:%M:%SZ')
    data["modified"] = datetime.strptime(json_data["modified"], '%Y-%m-%dT%H:%M:%SZ')
    data["uuid"] = json_data["uuid"]
    for image in json_data["images"]:
        if image["featured"]:
            data["image"] = image["url"]
            break
    return data

def parse_json_details(json_data):
    data = parse_json_base(json_data)
    data["promo"] = json_data["promo"]
    data["body"] = json_data["body"].replace('Â', '').replace('{%sfr%}', '')
    data["disclosure"] = json_data["disclosure"]
    data["pitch"] = json_data["pitch"]["text"]
    for author in json_data["authors"]:
        if author["byline"] == data["byline"]:
            data["username"] = author["username"]
            break
    return data


def home(request):
    json_load = get_content_json()
    results = json_load["results"]
    find = False
    for result in results:
        for tag in result["tags"]:
            if "10-promise" == tag["slug"]:
                first = parse_json_base(result)
                find = True
                break
        if find:
            results.remove(result)
            break
    rest_results = random.sample(results, 3)
    rest = []
    for result in rest_results:
        rest.append(parse_json_base(result))
    return render(request, 'blog/home.html', {'first': first, 'rest': rest})


def load_date_for_article(uuid):
    content_json = get_content_json()
    results = content_json["results"]
    content = ''
    cur_result = ''
    for result in results:
        if uuid == result["uuid"]:
            cur_result = result
            content = parse_json_details(result)
            break
    quote_json = get_quote_json()
    instruments = {}
    for instrument in cur_result["instruments"]:
        instruments[instrument["instrument_id"]] = {}
    instruments = get_inst_details(instruments, quote_json)
    comments = Comment.objects.values('comment_text', 'pub_date', 'author_id__username', 'author_id__small_avatar_url').filter(article_id=uuid).order_by('-pub_date')[:5]
    author = Author.objects.get(author_id=1)
    data = {
        "content": content,
        "instruments": instruments,
        "comments": comments,
        "author": author
    }
    return data


def article(request, uuid):
    data = load_date_for_article(uuid)
    return render(request, 'blog/article.html', {'article': data["content"], 'insts': data["instruments"].values(), 'comments': data["comments"], 'author': data["author"]})


def new_comment(request, uuid):
    try:
        author = Author.objects.get(author_id=1)
        comment = Comment(comment_text=request.POST['comment'], article_id=uuid, pub_date=datetime.now(), author=author)
        comment.save()
    except:
        data = load_date_for_article(uuid)
        return render(request, 'blog/article.html', {'article': data["content"], 'insts': data["instruments"].values(), 'comments': data["comments"], 'error': "Comment is not valid.", })
    return redirect('../article/' + uuid + "#show_comments")
