import yt_dlp

ydl_opts = {
    "continuedl": True,
    "retries": 10  # Повторяем попытку загрузки до 10 раз
}

link = input("ссылку: ")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])