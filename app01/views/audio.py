import os
from random import random

from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
import glob
from tqdm import tqdm

from app01.utils.utils import del_filedir,full_path
from app01.views.extract_audio import ffmpeg_extraction


@csrf_exempt
def audio(request):
    if request.method == "GET":
        return render(request, "audio.html")
    print(request.FILES.get("video"))
    file_object = request.FILES.get("video")
    print(file_object.name, "上传")
    # 视频上传至upload目录
    upload_dir = './app01/upload'
    #上传之前把记录的都删了
    """删除文件夹，使得推理结果始终在一个文件夹下"""
    del_filedir(upload_dir)

    file_path = os.path.join(upload_dir, file_object.name)
    # 检查目录是否存在，如果不存在就创建它
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    with open(file_path, "wb") as f_video:
        for chunk in file_object.chunks():
            f_video.write(chunk)
    f_video.close()
    return JsonResponse({'status': True})


def detect(request):
    videos_dir = './app01/upload'
    output_dir = './app01/static/extract_data/audios'
    """删除文件夹，使得推理结果始终在一个文件夹下"""
    del_filedir(output_dir)
    sample_rate = "24000"
    video_list = glob.glob(videos_dir + '/**/*.*', recursive=True)
    print("视频列表video_list: ", video_list)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    with tqdm(total=len(video_list)) as t_bar:
        for video in video_list:
            ffmpeg_extraction(video, os.path.join(output_dir, os.path.basename(video).split(".")[0] + ".wav"),
                              sample_rate)
            t_bar.update()

    name = full_path(output_dir)
    rate = random()
    kind = random()
    tips = random()
    path = "../static/extract_data/audios/"+ full_path(output_dir)

    result = {
        'status': True,
        'name': name,
        'rate': rate,
        'kind': 'wav音频',
        'tips': tips,
        'audio': path,
    }
    return JsonResponse(result)
