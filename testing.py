def build_format(ext=None, res=None, vcodec=None, acodec=None, vbr=None, abr=None):
    v_filter = []
    a_filter = []

    if ext:
        v_filter.append(f"ext={ext}")
    if res:
        v_filter.append(f"height<={res}")
    if vcodec:
        v_filter.append(f"vcodec*={vcodec}")
    if vbr:
        v_filter.append(f"tbr<={vbr}")
    
    if acodec:
        a_filter.append(f"acode")
    if abr:
        a_filter.append(f"abr<={abr}")

    v_str = f"[{'&'.join(v_filter)}]" if v_filter else ""
    a_str = f"[{'&'.join(a_filter)}]" if a_filter else ""

    return v_str, a_str

def main():

    v_filter, a_filter =build_format(ext="mp4", res=720, vbr=1000, abr= 192)
    print(v_filter)
    print(a_filter)

    Video_Format = f"bestvideo{v_filter}"
    Audio_Format = f"bestaudio{a_filter}"

    print(f"{Video_Format}+{Audio_Format}")

main()