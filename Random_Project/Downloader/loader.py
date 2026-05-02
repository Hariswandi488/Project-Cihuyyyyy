import threading, time, sys

# ----- Loading Var -----
is_loading = False
Lock = threading.Lock()
Loading_Thread = None

# ----- Timer Var -----
Timer_Start = False
Total_Time = 0
Timer_Thread = None

# ===== Loading Logic =====
def loading_anim(Name, delay):
    spinner = ["/", "-", "\\", "|"]
    i = 0
    while is_loading:
        with Lock:
            sys.stdout.write("\rLoading " + Name + " " + spinner[i % len(spinner)])
            sys.stdout.flush()
        i += 1
        time.sleep(delay)

def start_loading(name, delay):
    global is_loading, Loading_Thread
    is_loading = True
    Loading_Thread = threading.Thread(target=loading_anim, args=(name,delay,))
    Loading_Thread.start()

def stop_loading():
    global is_loading, Loading_Thread
    is_loading = False
    if Loading_Thread and Loading_Thread.is_alive():
        Loading_Thread.join()

# ===== Timer Logic =====
def Timer():
    global Total_Time, Timer_Start
    while Timer_Start:
        time.sleep(0.1)
        Total_Time += 0.1

def Start_Timer():
    global Total_Time, Timer_Start, Timer_Thread
    Total_Time = 0
    Timer_Start = True
    Timer_Thread = threading.Thread(target=Timer)
    Timer_Thread.start()

def Stop_Timer():
    global Timer_Start, Timer_Thread
    Timer_Start = False
    if Timer_Thread and Timer_Thread.is_alive():
        Timer_Thread.join()