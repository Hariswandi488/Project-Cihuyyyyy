
# ===== Mapping Custom Option =====

video_resolution_option = {
    "1" : ("1080p (FHD)", 1080),
    "2" : ("720p (HD)", 720),
    "3" : ("480p (SD)", 480),
}

video_bitrate_option = {
    "1" : ("Low", 1000),
    "2" : ("Medium", 2000),
    "3" : ("High", 4000),
    "4" : ("Very High", 6000)
}

video_container_option = {
    "1" : "mp4",
    "2" : "mkv",
    "3" : "avi",
    "4" : "ogv",
    "5" : "webm"
}

video_codec_option = {
    # <id> : (<label>, <ffmpeg>, <ffprobe>)
    "1" : ("H.264", "libx264", "h264"),
    "2" : ("H.265", "libx265", "hevc"),
    "3" : ("Xvid", "libxvid", "mpeg4"),
    "4" : ("VP9", "libvpx-vp9", "vp9"),
    "5" : ("MPEG-4 Part 2", "mpeg4", "mpeg4"),
    "6" : ("AV1", "libaom-av1", "av1"),
    "7" : ("Best/Recomended", None)
}

audio_codec_option = {
    # <id> : (<label>, <ffmpeg>, <ffprobe>)
    "1" : ("AAC", "aac", "aac"),
    "2" : ("MP3", "libmp3lame", "mp3"),
    "3" : ("Opus", "libopus", "opus"),
    "4" : ("Vorbis", "libvorbis", "vorbis"),
    "5" : ("WAV", "pcm_s16le", "pcm_s16le"),
    "6" : ("AC3", "ac3", "ac3"),
    "7" : ("Best/Recomended", None)
}

audio_container_option = {
    "1" : "mp3",
    "2" : "m4a",
    "3" : "ogg",
    "4" : "wav"
}

audio_quality_option = {
    "1" : ("Very Low (64kbps)", 64),
    "2" : ("Low (96kbps)", 96),
    "3" : ("Medium (128kbps)", 128),
    "4" : ("high (192kbps)", 192)
}


# ===== Motede Download =====
mode_option = {
    "1" : "Pisah (Video + Audio terpisah)",
    "2" : "Gabung (Video + Audio di 1 file)",
    "3" : "Audio Only",
    "4" : "Video Only"
}

teknik_download = {
    "1" : "Cepat (Best Auto, no convert)",
    "2" : "Universal MP4 (H.264 + AAC/MP3)",
    "3" : "Audio Only",
    "4" : "Custom"
}