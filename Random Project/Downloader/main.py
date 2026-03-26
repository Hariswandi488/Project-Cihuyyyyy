import yt_dlp, os, time, re, subprocess
import mapping_data as map_data
import loader as load
import downloader

# ===== Initial Var =====
# ----- Path Var ----
Parent_file = os.path.abspath(r"D:\VSCode Folder")
Output_file = os.path.join(Parent_file, "Output_Downloader")
print(Parent_file, Output_file)
ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")

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
    Output_Video_File = f"{Folder_Name}/Video {Video_Resolution}p {safe_title}.%(ext)s"
    Output_Audio_File = f"{Folder_Name}/Audio {safe_title}.%(ext)s"
    Output_Merge_File = f"{Folder_Name}/{safe_title}.%(ext)s"

    os.makedirs(Folder_Name, exist_ok=True)

    v_filter, a_filter = downloader.build_format(vext=Video_Ext, aext=Audio_Ext, res=Video_Resolution, vcodec=Video_Codec, acodec=Audio_Codec, vbr=Video_Bitrate, abr=Audio_Bitrate)

    Video_Format = f"bestvideo{v_filter}"
    Audio_Format = f"bestaudio{a_filter}"
    print(f"{Video_Format}+{Audio_Format}")

    Video_opts = {
        "format" : f"{Video_Format}/bestvideo",
        "progress_hooks" : [downloader.progress_hook],
        "quiet" : True,
        "no_warnings" : True,
        "ffmpeg_location" : ffmpeg_path,
        "outtmpl" : Output_Video_File
    }

    Audio_opts = {
        "format" : f"{Audio_Format}/bestaudio",
        "progress_hooks" : [downloader.progress_hook],
        "quiet" : True,
        "no_warnings" : True,
        "ffmpeg_location" : ffmpeg_path,
        "outtmpl" : Output_Audio_File
    }

    Merge_opts = {
        "format" : f"{Video_Format}+{Audio_Format}/best",
        "merge_output_format" : "mp4",
        "progress_hooks" : [downloader.progress_hook],
        "quiet" : True,
        "no_warnings" : True,
        "ffmpeg_location" : ffmpeg_path,
        "outtmpl" : Output_Merge_File
    }

    time.sleep(0.5)
    load.stop_loading()

    if mode == "1":
        file_path_v = downloader.download(url, Video_opts)
        file_path_a = downloader.download(url, Audio_opts)
        open_folder(file_path_v)

    elif mode == "2":
        file_path = downloader.download(url, Merge_opts)
        open_folder(file_path)

    elif mode == "3":
        file_path = downloader.download(url, Audio_opts)
        open_folder(file_path)

    elif mode == "4":
        file_path = downloader.download(url, Video_opts)
        open_folder(file_path)

    else:
        print("Mode Gak Jelas, Ganti Mode Yang Tepat")
        return

    load.stop_loading()
    load.Stop_Timer()
    print(f"\n\nDone in {int(load.Total_Time)}s")


main()