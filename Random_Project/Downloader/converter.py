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

    cmd += ["-c:v", check_codec(media_data["vcodec_ok"], vcodec)]
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

    result = subprocess.run(cmd, capture_output=True, text=True)

    if not result.stdout:
        raise Exception("ffprbe output empty")
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
    
    video_stream = None
    audio_stream = None
    for stream in info.get("streams", []):
        if stream.get("codec_type") == "video" and not video_stream:
            video_stream = stream
        elif stream.get("codec_type") == "audio" and not audio_stream:
            audio_stream = stream

        if video_stream:
            if video_stream.get("codec_name") == targets["vcodec"]:
                media_data["vcodec_ok"] = True

            width = video_stream.get("width")
            height = video_stream.get("height")
            aspect_ratio = width / height
            target_width = calc_resolution(aspect_ratio, height)

            if height == targets["resolution"] and width == target_width:
                media_data["resolustion_ok"] = True
        if audio_stream:
            if audio_stream.get("codec_name") == targets["acodec"]:
                media_data["acodec_ok"] = True
            if int(audio_stream.get("bit_rate", 0)) == int(targets["a_bitrate"]):
                media_data["a_bitrate_ok"] = True
    
    if not targets["crf"]:
        media_data["crf_ok"] = True

    full_path_target = info["format"]["filename"]
    filename = os.path.basename(full_path_target)
    _, ext = os.path.splitext(filename)

    if ext == targets["out_ext"]:
        media_data["out_ext_ok"] = True

    return media_data

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
