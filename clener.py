import os
videos = os.listdir('videos')
trash = os.listdir('videos/trash')
for file in trash:
    if file in videos:
        print(str(file))
        os.remove(f'videos/{file}')