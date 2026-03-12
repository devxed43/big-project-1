from PIL import ImageDraw, ImageFont
import matplotlib.pyplot as plt
from text_to_speech import save
from pydub import AudioSegment
from config import BLS_API_KEY
import imageio.v3 as iio
from pydub import effects
from io import BytesIO
from fpdf import FPDF
from PIL import Image
import requests
import qrcode
import json
import csv


def vid_to_gif():
    from moviepy import VideoFileClip
    import os
    import yt_dlp

    url = input("Enter video url (YouTube, etc.): ").strip()
    start = float(input("Enter start time in seconds: "))
    end = float(input("Enter end time in seconds: "))
    output_name = input("Enter output filename: ").strip()

    temp_video = "temp_video.mp4"

    print("Downloading video for processing...please wait...")

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "outtmpl": "temp_video.%(ext)s",
        "merge_output_format": "mp4",
        "quiet": True
    }

    temp_video = None

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            temp_video = ydl.prepare_filename(info)

        if not os.path.exists(temp_video):
            raise FileNotFoundError(f"Downloaded file not found: {temp_video}")

        print(f"Cutting clip from {start}s to {end}s...")
        clip = VideoFileClip(temp_video).subclipped(start, end).resized(width=480)

        print("⚡️ Generating GIF...")
        clip.write_gif(output_name, fps=10)
        clip.close()

        print(f"✅ Gif saved!")

        if os.path.exists(temp_video):
            os.remove(temp_video)

        print(f"✅ GIF SUCCESSFULLY CREATED! Saved as {output_name}")

    except Exception as e:
        print(f"❌ Something went wrong: {e}")

    finally:
        if temp_video and os.path.exists(temp_video):
            os.remove(temp_video)

def voice_record():
    import sounddevice as sd
    import soundfile as sf
    import numpy as np

    SAMPLE_RATE = 44100
    CHANNELS = 1
    FILENAME = 'recording.wav'
    DURATION = 3

    print("Recording...")

    audio_data = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='float32'
    )

    sd.wait()
    print("Done!")

    sf.write(FILENAME, audio_data, SAMPLE_RATE)
    print(f"Saved to {FILENAME}")

    # data, sr = sf.read(FILENAME)
    # sd.play(data, sr)
    # sd.wait()

def alarm_clock():
    import time
    import os
    from datetime import datetime

    alarm_time = input(
        "enter alarm time (e.g. 7:30am or 2:30pm): ").strip().upper()

    try:
        time_part, period = alarm_time.split(" ")
        alarm_hour, alarm_minute = time_part.split(":")
        alarm_hour = int(alarm_hour)
        alarm_minute = int(alarm_minute)

        if period == "PM" and alarm_hour != 12:
            alarm_hour += 12
        if period == "AM" and alarm_hour == 12:
            alarm_hour = 0

    except:
        print("❌ invalid format, use e.g. 7:30 AM or 2:30 PM")
        return

    alarm_file = input(
        "enter audio filename for alarm (e.g. alarm.mp3): ").strip()

    print(f"⏰ Alarm set for {alarm_time}!")

    while True:
        now = datetime.now()

        if now.hour == alarm_hour and now.minute == alarm_minute:
            print("🔔 WAKE UP! ALARM GOING OFF!")
            os.system(f"afplay {alarm_file}")
            break

        time.sleep(30)

def read_todos():
    with open('todos.txt', 'r') as file:
        print(file.read())

def add_todo():
    add = input("enter item: ")
    with open('todos.txt', 'a') as file:
        file.writelines(f'{add}\n')

def newsletter_signup():
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    age = input("Age: ")
    city = input("City: ")
    email = input("Email: ")

    entry = f"{first_name}, {last_name}, {age}, {city}, {email}"

    with open("contacts.txt", "a") as file:
        file.writelines(f'{entry}\n')

    print("Thank You for signing up for the bands touring list!")

def add_todos():
    print("Note: type 'done' to exit and get your new list")
    while True:
        tsk = input("add item: ")
        if tsk == "done":
            return
        else:
            with open('todos.txt', 'a') as file:
                file.writelines(f'{tsk}\n')

def edit_todo():
    with open('todos.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) == 0:
            print('nothing to edit! list is empty!')
            return False
        print("".join(lines))
        old = input("enter item to edit: ")
        new = input("enter new value: ")
        updated = []
        for line in lines:
            updated.append(line.replace(old, new))
        with open("todos.txt", 'w') as file:
            file.writelines(updated)
        return True

def edit_todos():
    with open('todos.txt', 'r') as file:
        lines = file.readlines()
        print("".join(lines))
        old = input("enter word to replace: ")
        new = input("enter new word: ")
        updated = []

        for line in lines:
            updated.append(line.replace(old, new))

        with open('todos.txt', 'w') as file:
            file.writelines(updated)

def delete_todo():
    with open("todos.txt", "r") as file:
        lines = file.readlines()
        if len(lines) == 0:
            print('nothing to delete! list is empty!')
            return False
        print("".join(lines))
        delete = input("select value to delete: ")
        updated = []
        for line in lines:
            if line.strip() != delete:
                updated.append(line)
        with open('todos.txt', 'w+') as file:
            file.writelines(updated)
        return True

def delete_todos():
    with open("todos.txt", "w") as file:
        file.write("")
    print("items deleted")

def speechify():
    with open("todos.txt", "r") as file:
        todo_content = file.read().strip()

        if not todo_content:
            print("empty list")
            return

        print("Generating audio for your todos...beep boop...beep boop...")
        language = "en"
        output_file = "todos.mp3"

        save(todo_content, language, file=output_file)
        print(f'VOICE ANALYSIS COMPLETE! {output_file}')

def pdfify():
    with open("todos.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    print("Generating PDF...⏱️...✅")

    pdf = FPDF()

    pdf.add_page()
    pdf.set_margin(10)
    pdf.set_font("helvetica", "B", size=16)
    pdf.cell(0, 10, text="Your Tasks for Today",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("helvetica", size=12)

    for index, line in enumerate(lines, 1):
        content = f"{index}. {line.strip()}"
        pdf.multi_cell(w=0, h=10, text=content, align="L",
                       new_x="LMARGIN", new_y="NEXT")

    output_file = "tasks.pdf"

    pdf.output(output_file)
    print(f"PDF SUCCESSFULLY CREATED! Check {output_file}")

def csvify():
    with open("contacts.txt", "r") as txt_file, open("contacts.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # This creates a header
        writer.writerow(['First Name', 'Last Name', 'Age', 'City', 'Email'])

        # loop thru each line
        for line in txt_file:
            task = line.strip()
            if task:
                # splits into separate columns
                writer.writerow(task.split(','))

    print("CSV conversion complete!")

def gifify():
    # https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmXvgBhvPpWFWiAkAGHWsqX1Ci96z-kdX32w&s

    # https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_WQQH3B6GXjpIQBez_fKqhJzc8yBzANE-GA&s

    resized_images = []
    choices = [input("enter first url: ").strip(),
               input("enter second url: ").strip()]
    for url in choices:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((500, 500))
        resized_images.append(img)

    print("🚀 Creating GIF now...let the roasts begin! 🔥")
    iio.imwrite('result.gif', resized_images, duration=200, loop=0)

def pixel_art():
    url = input("enter image url: ").strip()
    block_size = int(input("enter pixel size (try 10 or 20): "))

    # downloads the img
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    print("🎮 Converting to Pixel Art...🖼️")

    # calc for small size
    small_size = (img.size[0] // block_size, img.size[1] // block_size)
    # downsize
    img_small = img.resize(small_size, resample=Image.BILINEAR)
    # Upsample back to OG size with hard edges
    result = img_small.resize(img.size, Image.NEAREST)

    output_name = "pixel_art.png"
    result.save(output_name)
    print(f"👾 PIXEL ART COMPLETE! saved as {output_name}")

def alter_img1():
    img = Image.open("color-1.jpg")
    img = img.convert("RGB")

    d = img.get_flattened_data()

    new_image = []

    for item in d:
        if item[0] in list(range(200, 256)):
            new_image.append((50, 244, 200))
        else:
            new_image.append(item)

    # update img with new_image details if applicable
    img.putdata(new_image)

    img.save("new-color-1.jpg")

def export_audio():
    filename = input(
        "Enter audio filename (e.g. guitar.wav or drumbeat.mp3): ").strip()
    audio = AudioSegment.from_file(filename)

    # print info
    print(f"Duration:    {len(audio)} ms")          # length in milliseconds
    print(f"Channels:    {audio.channels}")          # 1=mono, 2=stereo
    print(f"Sample rate: {audio.frame_rate} Hz")     # e.g. 44100
    print(f"Bit depth:   {audio.sample_width * 8}")  # bits per sample

    # Slicing
    first_10s = audio[:10000]  # first 10,000 miliseconds aka 10 seconds
    last_5s = audio[-5000:]  # last 5 seconds
    middle = audio[5000:15000]  # 5s to 15s

    # Adjust Volume
    louder = audio + 6  # +6dB (2x louder)
    quieter = audio - 10  # -10db (much quieter)

    normalized = effects.normalize(audio)

    # ask user what to export
    print("\nWhat would you like to export?")
    print("options: full, first10, last5, middle, louder, quieter, normalized")
    choice = input("choice: ").strip().lower()

    export_map = {
        "full": audio,
        "first10": first_10s,
        "last5": last_5s,
        "middle": middle,
        "louder": louder,
        "quieter": quieter,
        "normalized": normalized,
    }

    if choice not in export_map:
        print("Invalid choice!")
        return

    out_format = input("export format? (wav / mp3): ").strip().lower()
    out_name = f"output-{choice}.{out_format}"
    export_map[choice].export(out_name, format=out_format)
    print(f"Exported as {out_name}")

def make_qrcode():
    data_to_encode = input("enter a url to create a QR code: ").strip().lower()
    img = qrcode.make(data_to_encode)
    img.save("QR-code.png")
    print("✅ QR code generated! 🔥")

def chartify():
    months = [
        "Jan 24", "Feb 24", "Mar 24", "Apr 24", "May 24", "Jun 24",
        "Jul 24", "Aug 24", "Sep 24", "Oct 24", "Nov 24", "Dec 24",
        "Jan 25", "Feb 25", "Mar 25", "Apr 25", "May 25", "Jun 25"
    ]

    postings = [
        41000, 43500, 47000, 45000, 48500, 46000,
        44000, 42000, 49000, 100, 000, 98, 500, 39000,
        52000, 6000,  53, 000,
    ]

    plt.figure(figsize=(12, 6))
    plt.plot(months, postings, marker='o',
             color='#3776AB', linewidth=2, markersize=6)
    plt.title("Python Job Postings 2024-2025", fontsize=16, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Job Postings")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True, linestyle="--", alpha=0.5)

    output_name = "2024-2025_jobs_chart.png"
    plt.savefig(output_name)
    plt.show()
    print(f"Chart saved as {output_name}")

def meme_generator():
    url = input("enter image url: ").strip()

    if url.startswith('http'):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        img = Image.open(url).convert("RGB")

    text = input("enter text to add: ").strip()

    draw = ImageDraw.Draw(img)

    # position options
    print("position options: top, center, bottom")
    position = input("position: ").strip().lower()

    w, h = img.size
    font = ImageFont.load_default(size=40)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    positions = {
        "top": ((w - text_w) // 2, 20),
        "center": ((w - text_w) // 2, (h - text_h) // 20),
        "bottom": ((w - text_w) // 2, h - text_h - 20)
    }

    xy = positions.get(position, positions["bottom"])
    draw.text(xy, text, fill="black", font=font)

    output = "new_meme.png"
    img.save(output)
    print(f"check✅ saved as {output}")

def extract_audio():
    import yt_dlp
    import os

    url = input("Enter video url (youtube or direct mp4): ").strip()
    print("🎸 Extracting audio... 🎷")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'extracted_audio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("✅ Audio extracted and saved as extracted_audio.mp3")

def unemployment_by_state():
    state_codes = {
        "alabama": "01", "alaska": "02", "arizona": "04", "arkansas": "05",
        "california": "06", "colorado": "08", "connecticut": "09", "delaware": "10",
        "florida": "12", "georgia": "13", "hawaii": "15", "idaho": "16",
        "illinois": "17", "indiana": "18", "iowa": "19", "kansas": "20",
        "kentucky": "21", "louisiana": "22", "maine": "23", "maryland": "24",
        "massachusetts": "25", "michigan": "26", "minnesota": "27", "mississippi": "28",
        "missouri": "29", "montana": "30", "nebraska": "31", "nevada": "32",
        "new hampshire": "33", "new jersey": "34", "new mexico": "35", "new york": "36",
        "north carolina": "37", "north dakota": "38", "ohio": "39", "oklahoma": "40",
        "oregon": "41", "pennsylvania": "42", "rhode island": "44", "south carolina": "45",
        "south dakota": "46", "tennessee": "47", "texas": "48", "utah": "49",
        "vermont": "50", "virginia": "51", "washington": "53", "west virginia": "54",
        "wisconsin": "55", "wyoming": "56"
    }

    state = input("enter state name (e.g. california): ").strip().lower()

    if state not in state_codes:
        print("state not found. check spelling")
        return

    # if what they type in is findable within state_codes object
    code = state_codes[state]
    series_id = f"LASST{code}0000000000003"

    payload = {
        "seriesid": [series_id],
        "startyear": "2022",
        "endyear": "2025",
        "registrationkey": BLS_API_KEY
    }

    print(f"Fetching unemployment data for {state.title()}...")

    response = requests.post(
        "https://api.bls.gov/publicAPI/v2/timeseries/data/",
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    data = response.json()

    if data["status"] != "REQUEST_SUCCEEDED":
        print(f"API error: {data['message']}")
        return

    series_data = data["Results"]["series"][0]["data"]
    series_data.reverse()

    labels = []
    values = []

    for d in series_data:
        if d['value'] == '-':    # ← skip missing data points
            continue
        month = d['periodName'][:3]
        year = d['year']
        label = f"{month} {year}"
        labels.append(label)

        value = float(d['value'])
        values.append(value)

    plt.figure(figsize=(14, 6))
    plt.plot(labels, values, marker='o',
             color='#e74c3c', linewidth=2, markersize=4)
    plt.fill_between(range(len(values)), values, min(
        values), alpha=0.1, color='#e74c3c')
    plt.title(
        f"Unemployment Rate — {state.title()} {payload["startyear"]}-{payload["endyear"]} (BLS)", fontsize=16, fontweight='bold')
    plt.xlabel("Month")
    plt.ylabel("Unemployment Rate (%)")
    plt.xticks(range(len(labels)), labels, rotation=45, ha='right', fontsize=7)
    plt.tight_layout()
    plt.grid(True, linestyle='--', alpha=0.5)

    output = f"unemployment_{state.replace(' ', '_')}.png"
    plt.savefig(output)
    plt.show()
    print(f"✅ Chart saved as {output}")

def yt_vid_download():
    import yt_dlp
    import os

    url = input("Enter YouTube URL: ").strip()
    print("🎬 Downloading...Downloading... 📥")

    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    print(f"✅ Video downloads complete! {info['title']}.mp4")


def main():
    print("**************************** SELECT MODE: **********************************")
    print(""
          "read, \n"
          "add, \n"
          "add multiple, \n"
          "alarm clock, \n"
          "unemployment by state, \n"
          "vid to mp3, \n"
          "video downloader, \n"
          "voice record, \n"
          "create meme, \n"
          "QR code, \n"
          "create chart, \n"
          "speech, \n"
          "pdf, \n"
          "csv, \n"
          "email signup, \n"
          "gif, \n"
          "pixel art, \n"
          "alter 1, \n"
          "export audio, \n"
          "edit, \n"
          "replace, \n"
          "delete, \n"
          "delete all \n")

    while True:
        mode = input("mode: ").strip().lower()
        print("")
        match mode:
            case "read":
                read_todos()
                break
            case "add":
                add_todo()
                break
            case "add multiple":
                add_todos()
                break
            case "edit":
                edit_todo()
                break
            case "replace":
                edit_todos()
                break
            case "delete":
                delete_todo()
                break
            case "delete all":
                delete_todos()
                break
            case "speech":
                speechify()
                break
            case "voice record":
                voice_record()
                break
            case "pdf":
                pdfify()
                break
            case "csv":
                csvify()
                break
            case "email signup":
                newsletter_signup()
                break
            case "gif":
                gifify()
                break
            case "pixel art":
                pixel_art()
                break
            case "alter 1":
                alter_img1()
                break
            case "export audio":
                export_audio()
                break
            case "QR code":
                make_qrcode()
                break
            case "create chart":
                chartify()
                break
            case "create meme":
                meme_generator()
                break
            case "vid to mp3":
                extract_audio()
                break
            case "vid to gif":
                vid_to_gif()
                break
            case "unemployment by state":
                unemployment_by_state()
                break
            case "alarm clock":
                alarm_clock()
                break
            case "video downloader":
                yt_vid_download()
                break
            case _:
                print("please select a mode")


if __name__ == "__main__":
    main()
