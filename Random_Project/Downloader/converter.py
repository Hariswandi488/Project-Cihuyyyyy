import os, subprocess, json

ffmpeg_path = os.path.abspath("D:/VSCode Folder/Project Cihuyyyyy/Random Project/Downloader/ffmpeg/ffmpeg.exe")
ffprobe_path = os.path.abspath("Random Project/Downloader/ffmpeg/ffprobe.exe")

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

    cmd += ["-c:v", check_helper(media_data["vcodec_ok", vcodec])]
    cmd += ["-c:a", check_helper(media_data["acodec_ok", acodec])]
    cmd += ["-b:a", check_helper(media_data["a_bitrate_ok", bitrate])]
    cmd += ["-crf", check_helper(media_data["crf_ok", crf])]
    cmd += ["-vf", check_helper(media_data["resolution_ok", f"scale={resolution}"])]

    output_file = make_output(input_file, output_ext)

    cmd.append(output_file)

    subprocess.run(cmd)

def get_media_data(input_file):
    cmd = [
        ffprobe_path,
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        input_file
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def is_valid(info, targets):
    media_data = {
        "vcodec_ok" : False,
        "acodec_ok" : False,
        "out_ext_ok" : False,
        "resolustion_ok" : False,
        "crf_ok" : False,
        "a_bitrate_ok" : False
    }

    for stream in info["streams"]:
        if stream["codec_type"] == "video":
            if stream["codec_name"] == targets["vcodec"]:
                media_data["vcodec_ok"] = True
            if stream["height"] == targets["resolution"]:
                media_data["resolustion_ok"] = True
        
        if stream["codec_type"] == "audio":
            if stream["codec_name"] == targets["acodec"]:
                media_data["acodec_ok"] = True
            if stream["bit_rate"] == targets["a_bitrate"]:
                media_data["a_bitrate_ok"] = True
    
    if not targets["crf"]:
        media_data["crf_ok"] = True

    full_path_target = info["format"]["filename"]
    filename = os.path.basename(full_path_target)
    name, ext = os.path.split(filename)

    if ext == targets["out_ext"]:
        media_data["out_ext_ok"] = True

    return media_data

def check_helper(is_ok, data):
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

def make_output(input_file, new_ext):
    base = os.path.splitext(input_file)[0]
    return base + f".{new_ext}"
