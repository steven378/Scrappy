# Adam Lopez
# Desktop buddy

import base64
import time
import json
import urllib.error
import urllib.parse
import urllib.request


import os
import random
import tkinter as tk
from PIL import Image, ImageTk
import time 

SCRAPPY_IDLE = "scrappy_demoidle.gif"
SCRAPPY_ISLEEP = "scrappy_demoidle_tosleep.gif"
SCRAPPY_SLEEPI = "scrappy_demosleep_toidle.gif"
SCRAPPY_LEFTROLL = "scrappy_demoroll_left.gif"
SCRAPPY_RIGHTROLL = "scrappy_demoroll_right.gif"
SCRAPPY_SLEEP = "scrappy_sleep.gif"
ASSET_DIR = r"C:\Steven\Cat-images"
SLEEP_DELAY_MS = 10000
# Dont forget to change your directory
root = tk.Tk()
root.title("Scrappy!")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "black")
root.attributes("-alpha", 0.98)
root.configure(bg="black")

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = max(20, screen_w - 180)
y = max(20, screen_h - 180)
return_x = x
vx = 3
vy = 0
frame_index = 0
state = "sleep"


def load_sequence(filename, frame_count):
    path = os.path.join(ASSET_DIR, filename)
    frames = []
    if not os.path.exists(path):
        return frames

    for i in range(frame_count):
        try:
            frames.append(tk.PhotoImage(file=path, format=f"gif -index {i}"))
        except tk.TclError:
            break
    return frames


idle = load_sequence(SCRAPPY_IDLE, 5)
idle_to_sleep = load_sequence(SCRAPPY_ISLEEP, 8)
sleep = load_sequence(SCRAPPY_SLEEP, 3)
sleep_to_idle = load_sequence(SCRAPPY_SLEEPI, 8)
roll_left = load_sequence(SCRAPPY_LEFTROLL, 8)
roll_right = load_sequence(SCRAPPY_RIGHTROLL, 8)

for seq in (idle, idle_to_sleep, sleep, sleep_to_idle, roll_left, roll_right):
    if not seq:
        break

if not idle:
    idle = [tk.PhotoImage()]  # fallback so the app still starts if assets are missing

label = tk.Label(root, bd=0, bg="black")
label.pack()
label.image = idle[0]
label.configure(image=idle[0])
label.bind("<Button-1>", lambda event: on_click(event))
label.bind("<Enter>", lambda event: on_hover(event))
label.bind("<Leave>", lambda event: on_leave(event))
label.configure(cursor="hand2")


def show_bubble(message):
    bubble = tk.Toplevel(root)
    bubble.overrideredirect(True)
    bubble.wm_attributes("-topmost", True)
    bubble.configure(bg="black")
    bubble_label = tk.Label(bubble, text=message, bg="black", fg="white", padx=12, pady=8)
    bubble_label.pack()
    bubble.geometry(f"+{x + 30}+{y - 20}")
    bubble.after(1500, bubble.destroy)


def go_to_sleep():
    global state, frame_index
    if state != "idle":
        return
    show_bubble("Yawn...")
    state = "idle_to_sleep"
    frame_index = 0


def on_click(event):
    global state, frame_index
    if state == "sleep":
        state = "sleep_to_idle"
        frame_index = 0
        show_bubble(random.choice([
           
            "Ready to help!"
            
        ]))
    else:
        ask_question()


def ask_question():
    global state, frame_index, return_x

    return_x = x
    state = "move_left"
    frame_index = 0
    root.after(4000, show_prompt)


def show_prompt():
    prompt = tk.Toplevel(root)
    prompt.title("Scrappy")
    prompt.geometry("500x150+520+500")
    prompt.overrideredirect(True)
    prompt.wm_attributes("-topmost", True)
    #prompt.configure(bg="darkblue")

    answer = tk.Label(prompt, text="", fg="black")
    answer.place(relx=0.5, rely=0.5, anchor="center")

    success_label = tk.Label(prompt, text="", fg="green")
    success_label.place(relx=0.5, rely=0.22, anchor="center")

    error_label = tk.Label(prompt, text="", fg="red")
    error_label.place(relx=0.5, rely=0.22, anchor="center")

    question = tk.Label(prompt, text="Scrappy: Would you like to scan a website?", fg="black")
    question.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    yes_button = tk.Button(prompt, text="Yes", command=lambda: clicked_yes(prompt, question, yes_button, no_button, answer, success_label, error_label))
    yes_button.place(relx=0.43, rely=0.72, anchor=tk.CENTER)
    no_button = tk.Button(prompt, text="No", command=lambda: clicked_no(prompt, question, yes_button, no_button, answer))
    no_button.place(relx=0.57, rely=0.72, anchor=tk.CENTER)


#####################################################################################################

def input_validation(prompt, answer, success_label, error_label, link_box):
    answer.place_forget()

    text = link_box.get().strip()
    periods = [char for char in text if char == "."]

    if text == "":
        error_label.config(text="Scrappy: Please enter a link !!")
        return
    elif " " in text:
        error_label.config(text="Scrappy: Links can't have spaces in them")
        return
    elif not text.startswith(("http://", "https://")):
        error_label.config(text="Scrappy: Links start with http:// or https://")
        return
    elif len(periods) < 2:
        error_label.config(text="There has to be minimum 2 periods (www. and .com")
        return
    else:
        success_label.config(text="Thank you for the valid link! Now I can look for red flags.")
        
        
        if __name__ == "__main__":
            scan_url(link_box)
        
#####################################################################################



def clicked_yes(prompt, question, yes_button, no_button, answer, success_label, error_label):


    yes_button.place_forget()
    no_button.place_forget()
    question.place_forget()

    answer.config(text="Okay paste link here")
    
    link_box = tk.Entry(prompt, width=70)

    link_box.place(relx=0.5, rely=0.5, anchor="center")
    check_button = tk.Button(prompt, text="Check Link", command=lambda: input_validation(prompt, answer, success_label, error_label, link_box))
    check_button.place(relx=0.5, rely=0.75, anchor="center")
    nvm_button = tk.Button(prompt, text="X", command=lambda: clicked_nvm(prompt, link_box, check_button, nvm_button, answer),bg="red", fg= "white", font=("Areil", 12, "bold"))
    nvm_button.place(relx=1.00, rely=0.00, anchor="ne")


def clicked_no(prompt, question, yes_button, no_button, answer):
    yes_button.place_forget()
    no_button.place_forget()
    question.place_forget()

    answer.place(relx=0.5, rely=0.5, anchor="center")
    answer.config(text="Scrappy: Okay have a good day")
    root.after(1000, end_question)
    prompt.after(2000, prompt.destroy)
    
def clicked_nvm(prompt, link_box, check_button, nvm_button, answer):
     
    link_box.place_forget()
    check_button.place_forget()
    nvm_button.place_forget()
    
    answer.config(text="Scrappy: Okay have a good day")
    
    answer.place(relx=0.5, rely=0.5, anchor="center")
    root.after(1000,end_question)
    prompt.after(2000, prompt.destroy)
####################################################################################################################

    
def end_questions():
    global state, frame_index
    if clicked_no():
        "move_right"
        frame_index = 0
        


#this function is to make yes no buttons after pressing image
#def next_steps():



    #this it to position buttons


    
    # so we moved beyond the picture, into question and yes or no

    
    
    

###################









def end_question():
    global state, frame_index
    state = "return_to_start"
    frame_index = 0

def handle_answer(prompt, answer):
    prompt.destroy()
    print(f"User answered: {answer}")


def on_hover(event):
    root.configure(cursor="hand2")


def on_leave(event):
    root.configure(cursor="")


#def pick_next_state():
 #   global state
  #  if state == "idle":
   #     chance = random.random()
    #    if chance < 0.12:
     #       state = "idle_to_sleep"
      #  elif chance < 0.25:
       #     state = "move_left" if random.random() < 0.5 else "move_right"
    #elif state == "sleep":
     #   if random.random() < 0.15:
      #      state = "sleep_to_idle"
    #elif state in {"move_left", "move_right"}:
     #   state = "idle"


def move_window():
    global x, y, vx, vy
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()

    x += vx
    y += vy
    if x < 0:
        x = 0
        vx = abs(vx)
    elif x + width > screen_w:
        x = screen_w - width
        vx = -abs(vx)

    if y < 0:
        y = 0
        vy = abs(vy)
    elif y + height > screen_h:
        y = screen_h - height
        vy = -abs(vy)

    root.geometry(f"{width}x{height}+{x}+{y}")


def animate():
    global frame_index, state, x, vx

    sequences = {
        "idle": idle,
        "idle_to_sleep": idle_to_sleep,
        "sleep": sleep,
        "sleep_to_idle": sleep_to_idle,
        "move_left": roll_left,
        "move_right": roll_right,
    }

    if state == "return_to_start":
        if x == return_x:
            state = "idle_to_sleep"
        current = roll_left if x > return_x else roll_right if x < return_x else idle
    else:
        current = sequences.get(state, idle)
    if not current:
        current = sleep

    if frame_index >= len(current):
        frame_index = 0

    frame = current[frame_index]
    label.image = frame
    label.configure(image=frame)

    if state == "move_left":
        x -= 80
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}+{x}+{y}")
    elif state == "move_right":
        x += 80
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}+{x}+{y}")
    elif state == "return_to_start":
        distance = min(80, abs(return_x - x))
        x += distance if x < return_x else -distance
        root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()}+{x}+{y}")

    if state == "return_to_start" and x == return_x:
        state = "idle"
        frame_index = 0
        root.after(SLEEP_DELAY_MS, go_to_sleep)
    else:
        frame_index += 1
        if frame_index >= len(current):
            frame_index = 0
            if state == "idle_to_sleep":
                state = "sleep"
            elif state == "sleep_to_idle":
                state = "idle"
            elif state in {"move_left", "move_right"}:
                state = "idle"

    root.after(500, animate)


def on_press(event):
    root._drag_x = event.x_root - root.winfo_x()
    root._drag_y = event.y_root - root.winfo_y()
    root.bind("<B1-Motion>", on_drag)


def on_drag(event):
    root.geometry(f"+{event.x_root - root._drag_x}+{event.y_root - root._drag_y}")


root.bind("<Button-1>", on_press)
root.bind("<ButtonRelease-1>", lambda event: root.unbind("<B1-Motion>"))
root.geometry(f"100x100+{x}+{y}")
root.after(120, animate)



# 1. Paste your actual key here
API_KEY = "936fc7949586d85f5987af4896a73dda7a47e6bf9862bfdc90e8da41141dfc43"
HEADERS = {"x-apikey": API_KEY, "accept": "application/json"}

def get_url_id(url: str) -> str:
    """Generates a perfect VirusTotal API v3 URL identifier."""
    clean_url = url.strip()
    encoded = base64.urlsafe_b64encode(clean_url.encode("utf-8"))
    return encoded.decode("utf-8").rstrip("=")

def scan_url(target_url: str):
    if hasattr(target_url, "get"):
        target_url = target_url.get().strip()
    url_id = get_url_id(target_url)
    
    # 100% EXPLICIT AND HARDCODED PATH
    report_endpoint = "https://www.virustotal.com/api/v3/urls/" + url_id
    
    print(f"Checking: {target_url}")
    
    try:
        request = urllib.request.Request(report_endpoint, headers=HEADERS)
        try:
            with urllib.request.urlopen(request) as response:
                status_code = response.status
                response_text = response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            status_code = error.code
            response_text = error.read().decode("utf-8")
        
        # Scenario A: The URL exists in the database
        if status_code == 200:
            stats = json.loads(response_text)["data"]["attributes"]["last_analysis_stats"]
            #print(f"\nResults for {target_url}:")
            #print(f"➡ Malicious: {stats['malicious']}")
            #print(f"➡ Suspicious: {stats['suspicious']}")
            #print(f"➡ Harmless: {stats['harmless']}\n")

            window = tk.Toplevel(root)
            report = tk.Label(window, text = f"\nResults for {target_url}: \n\t Malicious: {stats['malicious']} \n\t Suspicious: {stats['suspicious']} \n\t Harmless: {stats['harmless']}\n", font=("Areil", 12, "bold"))
            # This conditional is to see give the user a final verdict of the site if its malicious, suspicious, or harmless based on the report.
            if int(stats["malicious"]) >= 1:
                    final_verdict = tk.Label(window, text = "This site is malicious. It is dangerous. Do not enter !!", font= ("Ariel", 12, "bold"))
                    final_verdict.place(relx = 0.5, rely = 0.85, anchor = "center")
            elif int(stats["suspicious"]) >= 1:
                    final_verdict = tk.Label(window, text = "Heads up! This site is suspicious.", font= ("Ariel", 12, "bold"))
                    final_verdict.place(relx = 0.5, rely = 0.85, anchor = "center")
            else:
                    final_verdict = tk.Label(window, text = "This site is harmless." , font= ("Ariel", 12, "bold"))
                    final_verdict.place(relx = 0.5, rely = 0.85, anchor = "center")
            report.place(relx = 0.5, rely = 0.5, anchor = "center")
            window.geometry("500x340+520+150")
            #500x150+520+500"
            window.overrideredirect(True)
            window.wm_attributes("-topmost", True)
            close_report = tk.Button(window, text="X",command = lambda: when_click(window), bg="red", fg= "white", font=("Areil", 12, "bold"))
            close_report.place(relx=1.00, rely=0.00, anchor="ne")
            def when_click(window):
                window.after(500, window.destroy)
                    




            
        # Scenario B: 404 - Not Found. Trigger automatic submission!
        elif status_code == 404:
            print("⚠ URL not found in database. Automatically submitting it now...")
            
            # 100% EXPLICIT AND HARDCODED SUBMISSION PATH
            submit_endpoint = "https://www.virustotal.com/api/v3/urls/"
            
            post_data = urllib.parse.urlencode({"url": target_url}).encode("utf-8")
            submit_request = urllib.request.Request(
                submit_endpoint, data=post_data, headers=HEADERS, method="POST"
            )
            try:
                with urllib.request.urlopen(submit_request) as submit_response:
                    submit_status = submit_response.status
                    submit_text = submit_response.read().decode("utf-8")
            except urllib.error.HTTPError as error:
                submit_status = error.code
                submit_text = error.read().decode("utf-8")
            
            if submit_status in (200, 201):
                print("🚀 Successfully submitted! Waiting 15 seconds for analysis...")
                time.sleep(15)
                print("🔄 Retrying report fetch...\n")
                return scan_url(target_url)
            else:
                print(f"❌ Failed to submit URL: {submit_status} - {submit_text}")
                
        # Scenario C: Something else went wrong (e.g., Wrong API key)
        else:
                print(f"❌ Error {status_code}: {response_text}")
            
    except urllib.error.URLError as e:
        print(f"❌ Network Error: Make sure your internet is working. Code: {e}")





root.mainloop()










