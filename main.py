import tkinter as tk
import tkinter.filedialog as tk_file
from pytube import YouTube as YT

def browseFiles():
    global folder_to_download
    folder_to_download = tk_file.askdirectory()
    updateInfoLabel("Download path has been updated")

def updateInfoLabel(text):
    info_label['text'] = text

def download():
    if chosen_format == '':
        updateInfoLabel("No selected format to download! Fetch and select desired format!")
        return
    if folder_to_download == '':
        updateInfoLabel("Select a path to download")
        browseFiles()
        if folder_to_download == '':
            return
    itag = ''
    for letter in chosen_format[6:]:
        if letter != ',':
            itag += letter
        else: break
    itag = int(itag)
    updateInfoLabel("Downloading...")
    stream_to_download = yt_obj.streams.get_by_itag(itag)
    stream_to_download.download(folder_to_download)
    updateInfoLabel(f"Download has been finished! Saved in {folder_to_download}")

def fetchVideo():
    def handle_fps(i):
        if scrap[i].type == 'audio':
            return 'Codec: ' + str(scrap[i].audio_codec)
        else:
            return ' Fps: ' + str(scrap[i].fps) + ' Codec: ' + str(scrap[i].video_codec)
    def handle_res(i):
        if scrap[i].resolution == None:
            return "Bitrate: " + str(scrap[i].abr)
        else:
            return "Res: " + str(scrap[i].resolution)
    
    updateInfoLabel("Fetching...")
    #fetch yt_vid info
    global yt_link
    yt_link = link.get()
    if yt_link == '':
        print("Enter a link to yt")
        return
    global yt_obj
    yt_obj = YT(yt_link)
    scrap = yt_obj.streams
    scrap_2 = list()

    #format for a listbox
    for i in range(len(scrap)):
        scrap_2.append( 'itag: {}, type: {}, {}, {}'.format(scrap[i].itag , scrap[i].type ,handle_res(i), handle_fps(i)) )
    #update the listbox
    for format in scrap_2:
        dwn_options.insert(scrap_2.index(format), format)
    updateInfoLabel("Done fetching! Now select desired format and path and start downloading!")

def on_listbox_format(event):
    global chosen_format
    chosen_format = dwn_options.get(dwn_options.curselection())

window = tk.Tk()
window.title("YT downloader")
window.minsize(width=500, height=500)

folder_to_download = ''
yt_link = ''

dwn_path = tk.Button(text="Select download path", command=browseFiles)
dwn_path.pack()

tk.Label(text="What you want to download: ").pack()
link = tk.Entry(width=50)
link.pack()

dwn_fetch = tk.Button(text='Get available formats', command=fetchVideo).pack()
tk.Label(text="Fetched formats:").pack()

chosen_format = ''
dwn_options = tk.Listbox(width=100)
dwn_options.bind("<<ListboxSelect>>", on_listbox_format)
dwn_options.pack()
dwn_start = tk.Button(text="Start downloading!", command=download).pack()

info_label = tk.Label(window, text="  ")
info_label.pack()

window.mainloop()