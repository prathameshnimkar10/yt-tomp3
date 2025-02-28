import os
import yt_dlp
import requests
import threading
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# https://youtu.be/yiJ5k2vBtlw?si=bIQL31WQz5x4TRfp
ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "bin")

output_dir = "downloads"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def download_audio():
    """Starts a separate thread to download audio to prevent UI freezing."""
    threading.Thread(target=process_download, daemon=True).start()

def process_download():
    url = url_entry.get().strip()
    if not url:
        status_label.config(text = "Enter a valid YouTube URL!", fg = "red")
        return
    
    save_path = output_dir if not dir_var.get() else dir_var.get()

    progress_bar["value"] = 0
    progress_label.config(text = "In progres...", fg="blue")
    open_folder_button.pack_forget()

    yt_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_path, "%(title)s.%(ext)s"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'writethumbnails': True,
        'embedthumbnails': True,
        'postprocessor_args': [
            '-metadata', 'title=%(title)s',
            '-metadata', 'artist=%(title)s',
        ],
        'quiet': False,
        'ffmpeg_location': ffmpeg_path,
        'progress_hooks': [update_progress],
    }

    try:
        with yt_dlp.YoutubeDL(yt_opts) as yt:
            info_dict = yt.extract_info(url, download=True)
            song_title = info_dict.get('title')
            thumbnail_url = info_dict.get('thumbnail')

        if thumbnail_url:
            download_thumbnail(thumbnail_url, song_title, save_path)

        status_label.config(text = f"Downloaded: {song_title}.mp3", fg='green')
        messagebox.showinfo("Success!", f"Downloaded complete:\n{song_title}.mp3")

        open_folder_button.pack(pady=10)
    
    except Exception as e:
        status_label.config(text = "Aww hell naw!", fg = "red")
        messagebox.showinfo(f"Download Failed,{e}, womp womp.")

def update_progress(d):
    if d['status'] == 'downloading':
        try:
            percent = d['percent_str'].strip().replace('%', '')
            progress_bar["value"] = float(percent)
            root.update_idletasks()
        except:
            pass

def download_thumbnail(thumbnail_url, song_title, save_path):
    try:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image_path = os.path.join(save_path, f"{song_title}.jpg")
            image.save(image_path, "JPEG")

    except Exception:
        pass

def browse_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        dir_var.set(folder_selected)

def open_folder():
    save_path = output_dir if not dir_var.get() else dir_var.get()
    webbrowser.open(save_path)

root = tk.Tk()
root.title("YT to MP3 Downloader!")
root.geometry("800x600")
root.configure(bg="#F4F4F4")

logo_path = "logo.png"
try:
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((250, 250), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(root, image=logo_photo, bg="#F4F4F4")
    logo_label.pack(pady=10)
except Exception as e:
    print(f"Logo Error: {e}")

frame = tk.Frame(root, bg="#F4F4F4")
frame.pack(expand=True, pady=10)

tk.Label(frame, text="Enter YouTube URL:", font=("Arial", 12, "bold"), bg="#F4F4F4").pack(pady=5)
url_entry = tk.Entry(frame, width=55, relief='solid', bd=2)  # Made entry a bit bigger
url_entry.pack(pady=5)

dir_var = tk.StringVar()
dir_frame = tk.Frame(frame, bg="#F4F4F4")
dir_frame.pack(pady=10, fill="x")

tk.Label(dir_frame, text="Save to: \n(Music folder, obv??)", font=("Arial", 11), bg="#F4F4F4").grid(row=0, column=0, sticky="w", padx=5)
dir_entry = tk.Entry(dir_frame, textvariable=dir_var, width=45, relief="solid", bd=2)  # Made it wider
dir_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(dir_frame, text="Browse", command=browse_directory, font=("Arial", 10, "bold"), bg="#007BFF", fg="white", relief="flat").grid(row=0, column=2, padx=5)

progress_label = tk.Label(frame, text="", font=("Arial", 12), bg="#F4F4F4")
progress_label.pack(pady=5)
progress_bar = ttk.Progressbar(frame, length=400, mode="determinate")
progress_bar.pack(pady=5)

download_button = tk.Button(frame, text="Let's Go!", command=download_audio, font=("Arial", 12, "bold"), bg="blue", fg="white", relief="flat", padx=10, pady=5)
download_button.pack(pady=15)

status_label = tk.Label(frame, text="", font=("Arial", 12), fg="black", bg="#F4F4F4")
status_label.pack(pady=5)

open_folder_button = tk.Button(frame, text="Open Folder to view new song?", command=open_folder, font=("Arial", 11, "bold"), bg="#007BFF", fg="white", relief="flat", padx=10, pady=5)

root.mainloop()