import yt_dlp, os, time, re, subprocess
import mapping_data as map_data
import loader as load
import downloader
import converter

# ===== Initial Var =====
# ----- Path Var ----
base_path = os.path.dirname(os.path.abspath(__file__))
Output_file = os.path.join(base_path, "Output_Downloader")
print(base_path, Output_file)
ffmpeg_path = os.path.join(base_path, "ffmpeg/ffmpeg.exe")

# ===== Get Formats Url =====
def get_info(url):
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["formats"]

# ===== Choose Custom Setting Logic For Download =====      
def list_option(title, option):
    print(f"\nPilih {title} :")
    for i,j in option.items():
        print(f"{i}. {j if isinstance(j, str) else j[0]}")
    return input("Pilih : ")

# ===== Open Folder =====
def open_folder(file_path):
    if os.path.exists(f"{file_path}"):
        subprocess.run(['explorer', '/select,', file_path])
    else:
        print("Path Not Exist")

def ask_convert(text):
    ask = input(f"Output File {text} Not Valid\nWant Convert? (y/n):")
    if ask.lower() == "y":
        return True
    else:
        return False

# ===== Main Logic CLI =====
def main():
    url = input("Masukan Url : ")
    teknik = list_option("Teknik Download", map_data.teknik_download)
    vr = list_option("Resolusi", map_data.video_resolution_option)
    vb = list_option("Video Quality", map_data.video_bitrate_option)

    if teknik == "2":
        vc = "1"     # H.264 (VCodec)
        ve = "1"    # MP4 (VExt)
        aq = "2"    # Low (96kbps)
        ac = "2"    # MP3 (ACodec)
        ae = "1"    # MP3 (AExt)
        mode = "2"  # (Audio + Video In 1)

    elif teknik == "4":
        show_list = input("\nLihat List Download (y/n) : ")
        if show_list.lower() == "y":
            load.start_loading("Req List Download", 0.2)
            formats = get_info(url)
            print("")
            downloader.format_list(formats)
            load.stop_loading()
        
            input("")

        vc = list_option("Video Codec", map_data.video_codec_option)
        ve = list_option("Video Format", map_data.video_container_option)
        aq = list_option("Audio Quality", map_data.audio_quality_option)
        ac = list_option("Audio Codec", map_data.audio_codec_option)
        ae = list_option("Audio Format", map_data.audio_container_option)
        mode = list_option("Output Download", map_data.mode_option)

    if (aq not in map_data.audio_quality_option) or (vb not in map_data.video_bitrate_option) or (vr not in map_data.video_resolution_option) or (vc not in map_data.video_codec_option) or (ve not in map_data.video_container_option) or (ac not in map_data.audio_codec_option) or (ae not in map_data.audio_container_option) :
        print("Pilihan Nguawur , Masukan Ulang")
        return
    
    Video_Resolution = map_data.video_resolution_option[vr][1]
    Video_Bitrate = map_data.video_bitrate_option[vb][1]
    Video_Codec = map_data.video_codec_option[vc][1]
    Video_Ext = map_data.video_container_option[ve]
    Audio_Bitrate = map_data.audio_quality_option[aq][1]
    Audio_Codec = map_data.audio_codec_option[ac][1]
    Audio_Ext = map_data.audio_container_option[ae]


    print(f"""
Data File:
Mode File : {map_data.mode_option[mode]}
Video Resolusi : {Video_Resolution}p
Video Bitrate : {Video_Bitrate}kbps
Video Codec : {Video_Codec} ({map_data.video_codec_option[vc][0]})
Video Ext : {Video_Ext}
Audio Quality : {Audio_Bitrate}kbps
Audio Codec : {Audio_Codec} ({map_data.audio_codec_option[ac][0]})
Audio Ext : {Audio_Ext}

""")
    
    load.start_loading("Start Download", 0.1)
    load.Start_Timer()

    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        title = info["title"]
    
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    Folder_Name = f"{Output_file}/{safe_title}"
    Output_Video_File = f"{Folder_Name}/Video {Video_Resolution}p.%(ext)s"
    Output_Audio_File = f"{Folder_Name}/Audio.%(ext)s"
    Output_Merge_File = f"{Folder_Name}/Video {Video_Resolution}p + Audio.%(ext)s"

    os.makedirs(Folder_Name, exist_ok=True)

    v_filter, a_filter = downloader.build_format(vext=Video_Ext, aext=Audio_Ext, res=Video_Resolution, vcodec=Video_Codec, acodec=Audio_Codec, vbr=Video_Bitrate, abr=Audio_Bitrate)

    Video_Format = f"bestvideo{v_filter}"
    Audio_Format = f"bestaudio{a_filter}"
    print(f"{Video_Format}+{Audio_Format}")

    Video_opts = {
        "format" : f"{Video_Format}/bestvideo[height<={Video_Resolution}]",
        "progress_hooks" : [downloader.progress_hook],
        "quiet" : True,
        "no_warnings" : True,
        "ffmpeg_location" : ffmpeg_path,
        "restrictfilenames" : True,
        "outtmpl" : Output_Video_File
    }

    Audio_opts = {
        "format" : f"{Audio_Format}/bestaudio",
        "progress_hooks" : [downloader.progress_hook],
        "quiet" : True,
        "no_warnings" : True,
        "ffmpeg_location" : ffmpeg_path,
        "restrictfilenames" : True,
        "outtmpl" : Output_Audio_File
    }

    Merge_opts = {
        "format" : f"{Video_Format}+{Audio_Format}/bestvideo[height<={Video_Resolution}]+bestaudio",
        "merge_output_format" : "mp4",
        "progress_hooks" : [downloader.progress_hook],
        "quiet" : True,
        "no_warnings" : True,
        "ffmpeg_location" : ffmpeg_path,
        "restrictfilenames" : True,
        "outtmpl" : Output_Merge_File
    }

    load.stop_loading()

    if mode == "1":
        file_path_v = downloader.download(url, Video_opts)
        file_path_a = downloader.download(url, Audio_opts)
        a_ext_target = Audio_Ext
        v_ext_target = Video_Ext
        open_folder(file_path_v)

    elif mode == "2":
        file_path = downloader.download(url, Merge_opts)
        file_type = "Audio + Video"
        ext_target = Video_Ext
        open_folder(file_path)

    elif mode == "3":
        file_path = downloader.download(url, Audio_opts)
        file_type = "Audio"
        Video_Codec = None
        ext_target = Audio_Ext
        open_folder(file_path)

    elif mode == "4":
        file_path = downloader.download(url, Video_opts)
        file_type = "Video"
        Audio_Codec = None
        ext_target = Video_Ext
        open_folder(file_path)

    else:
        print("Mode Gak Jelas, Ganti Mode Yang Tepat")
        return

    load.stop_loading()
    load.Stop_Timer()
    print(f"\n\nDone in {int(load.Total_Time)}s")
    
    load.start_loading("Validation", 0.2)
    target_acodec = map_data.audio_codec_option[ac][2]
    target_vcodec = map_data.video_codec_option[vc][2]
    if mode == "1":
        info_media_a = converter.get_media_data(file_path_a)
        info_media_v = converter.get_media_data(file_path_v)

        a_target = converter.setup_target(acodec=target_acodec, vcodec=target_vcodec, out_ext=a_ext_target, resolution=Video_Resolution, a_bitrate=Audio_Bitrate)
        v_target = converter.setup_target(acodec=target_acodec, vcodec=target_vcodec, out_ext=v_ext_target, resolution=Video_Resolution, a_bitrate=Audio_Bitrate)

        media_data_a, is_a_valid = converter.is_valid(info_media_a, a_target)
        media_data_v, is_v_valid = converter.is_valid(info_media_v, v_target)
        load.stop_loading()
        if not is_a_valid and not is_v_valid:
            convert = ask_convert("Audio + Video")
            if convert:
                converter.convert_media(input_file=file_path_a, output_ext=a_ext_target, media_data=media_data_a, acodec=Audio_Codec)
                converter.convert_media(input_file=file_path_v, output_ext=v_ext_target, media_data=media_data_v, vcodec=Video_Codec)
        
        elif is_a_valid and not is_v_valid:
            convert = ask_convert("Video")
            if convert:
                converter.convert_media(input_file=file_path_a, output_ext=v_ext_target, media_data=media_data_v, vcodec=Video_Codec)
        elif is_v_valid and not is_a_valid:
            convert = ask_convert("Audio")
            if convert:
                converter.convert_media(input_file=file_path_a, output_ext=a_ext_target, media_data=media_data_a, acodec=Audio_Codec)
    else:
        info_media = converter.get_media_data(file_path)
        target = converter.setup_target(acodec=target_acodec, vcodec=target_vcodec, out_ext=ext_target, resolution=Video_Resolution, a_bitrate=Audio_Bitrate)
        media_data, is_valid = converter.is_valid(info_media, target)

        if not is_valid:
            convert = ask_convert(file_type)
            if convert:
                converter.convert_media(input_file=file_path, output_ext=ext_target, media_data=media_data, acodec=Audio_Codec, vcodec=Video_Codec)

    print("Convert Done")
                
    
main()