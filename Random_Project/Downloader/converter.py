import os, subprocess, json

ffmpeg_path = os.path.abspath("Random_Project/Downloader/ffmpeg/ffmpeg.exe")
ffprobe_path = os.path.abspath("Random_Project/Downloader/ffmpeg/ffprobe.exe")

def convert_media(
        input_file,
        output_ext,
        media_data=None,
        vcodec=None,
        acodec=None,
        bitrate=None,
        crf=None,
        resolution=None
):
    cmd = [ffmpeg_path, "-i", input_file]

    if vcodec and acodec:
        cmd += ["-c:v", check_codec(media_data["vcodec_ok"], vcodec)]
        cmd += ["-c:a", check_codec(media_data["acodec_ok"], acodec)]
    elif vcodec and not acodec:
        cmd += ["-c:v", check_codec(media_data["vcodec_ok"], vcodec)]
    elif acodec and not vcodec:
        cmd += ["-c:a", check_codec(media_data["acodec_ok"], acodec)]
        


    if not media_data["a_bitrate_ok"] and bitrate:
        cmd += ["-b:a", bitrate]
    
    if not media_data["crf_ok"] and crf:
        cmd += ["-crf", str(crf)]

    if not media_data["resolution_ok"] and resolution:
        cmd += ["-vf", f"scale=-1:{resolution}"]

    output_file = make_output(input_file, output_ext)

    cmd.append(output_file)

    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise Exception("ffmpeg error")

def get_media_data(input_file):
    cmd = [
        ffprobe_path,
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams", "-show_format",
        input_file
    ]

    result = subprocess.run(cmd,
                            capture_output=True,
                            text=True,
                            encoding="utf-8",
                            errors="replace"
)

    if not result.stdout:
        raise Exception("ffprobe output empty")
    
    return json.loads(result.stdout)

def is_valid(info, targets):
    media_data = {
        "vcodec_ok" : False,
        "acodec_ok" : False,
        "out_ext_ok" : False,
        "resolution_ok" : False,
        "crf_ok" : False,
        "a_bitrate_ok" : False
    }

    is_data_valid = True
    streams = info.get("streams", [])
    
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    if video_stream:
        if targets["vcodec"] and video_stream.get("codec_name") == targets["vcodec"]:
            media_data["vcodec_ok"] = True

        width = video_stream.get("width")
        height = video_stream.get("height")

        if width and height:
            aspect_ratio = width / height

            target_height = targets["resolution"]
            target_width = calc_resolution(aspect_ratio, target_height)

        if height == targets["resolution"] and width == target_width:
            media_data["resolution_ok"] = True

    if audio_stream:
        if  targets["acodec"] and audio_stream.get("codec_name") == targets["acodec"]:
            media_data["acodec_ok"] = True

        if targets["a_bitrate"]:
            if int(audio_stream.get("bit_rate", 0)) == int(targets["a_bitrate"]):
                media_data["a_bitrate_ok"] = True
    
    if not targets["crf"]:
        media_data["crf_ok"] = True

    full_path_target = info["format"]["filename"]
    filename = os.path.basename(full_path_target)
    _, ext = os.path.splitext(filename)

    if targets["out_ext"] and ext == targets["out_ext"]:
        media_data["out_ext_ok"] = True
    
    for media,is_ok in media_data.items():
        print(f"{media} : {is_ok}")
        if is_ok == False:
            is_data_valid = False

    return media_data, is_data_valid

def check_codec(is_ok, data):
    if not is_ok and data:
        return data
    return "copy"

def setup_target(
        acodec=None, vcodec=None,
        out_ext=None, resolution=None,
        crf=None, a_bitrate=None
):
    targets = {
        "vcodec" : vcodec,
        "acodec" : acodec,
        "resolution" : resolution,
        "out_ext" : out_ext,
        "crf" : crf,
        "a_bitrate" : a_bitrate
    }

    return targets

def calc_resolution(aspect_ratio, height):
    return int(height * aspect_ratio)

def make_output(input_file, new_ext):
    base = os.path.splitext(input_file)[0]
    return base + f".{new_ext}"
