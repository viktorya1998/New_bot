import urllib.request
import json
import config


def get_text(file):
    params = "&".join([
        "topic=general",
        "folderId=%s" % config.FOLDER_ID,
        "lang=ru-RU"
    ])
    #
    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=file)
    url.add_header("Authorization", "Bearer %s" % config.IAM_TOKEN)

    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    decodedData = json.loads(responseData)

    if decodedData.get("error_code") is None:
        return decodedData.get("result")
