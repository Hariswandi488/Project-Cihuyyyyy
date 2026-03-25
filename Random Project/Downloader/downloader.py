import yt_dlp, sys
import loader as load

# ===== Download Logic =====
def download(url, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)

# ===== List Download =====
def format_list(formats):
    clean_list = []
    for f in formats:
        if (f.get("height") is not None and f.get("height") < 480) or (f.get("vcodec") == "none" and f.get("acodec") == "none"):
            continue

        clean_list.append({
            "id" : f.get("format_id"),
            "type" : "video" if f.get("vcodec") != "none" else "audio",
            "res" : f"{f.get('height')}p" if f.get("height") else "-",
            "vcodec" : f.get("vcodec"),
            "acodec" : f.get("acodec"),
            "bitrate" : f.get("vbr") or f.get("abr") or f.get("tbr"),
            "ext" : f.get("ext")
        })
    
    clean_list = sorted(clean_list, key=lambda x: (x["type"], x["res"], x["bitrate"] or 0))

    for c in clean_list:
        print(f'{c["id"]:>5} | {c["type"]:>5} | {c["res"]:>6} | {c["vcodec"]:<12} | {c["acodec"]:<12} | {c["bitrate"] or "-":>8} kbps | {c["ext"]}')

# ----- Loading Download Progress Logic -----
def progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()

        sys.stdout.write(f"\rDownloading {percent} | {speed} | ETA {eta}")
        sys.stdout.flush()
    
    elif d["status"] == "finished":
        load.start_loading("Merge Video + Audio", 0.2)
        load.stop_loading()

# ===== Filter Format Logic =====
def build_format(vext=None, aext=None, res=None, vcodec=None, acodec=None, vbr=None, abr=None):
    v_filter = []
    a_filter = []

    # ----- append video filter -----
    if vext:
        v_filter.append(f"[ext={vext}]")
    if res:
        v_filter.append(f"[height<={res}]")
    if vcodec:
        v_filter.append(f"[vcodec*={vcodec}]")
    if vbr:
        v_filter.append(f"[tbr<={vbr}]")
    
    # ----- append audio filter -----
    if acodec:
        a_filter.append(f"[acodec*={acodec}]")
    if abr:
        a_filter.append(f"[abr<={abr}]")
    if aext:
        a_filter.append(f"[ext={aext}]")

    v_str = f"[{''.join(v_filter)}]" if v_filter else ""
    a_str = f"[{''.join(a_filter)}]" if a_filter else ""

    return v_str, a_str