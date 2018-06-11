import os, time, shutil
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter import *


root = Tk()
root.title("Sorting parameters")
root.geometry("300x150")
gdeep = IntVar()
goverwrite = IntVar()
gdate = IntVar()
gdeep_checkbutton = Checkbutton(text="Also extract files from subfolders?", variable=gdeep)
goverwrite_checkbutton = Checkbutton(text="Overwrite duplicate files with later version?", variable=goverwrite)
gdate_checkbutton = Checkbutton(text="Split file by the year of last modification?", variable=gdate)

def close_window():
    root.destroy()

gdeep_checkbutton.pack()
gdeep_checkbutton.place(relx=.5, rely=.6, anchor="c")

goverwrite_checkbutton.pack()
goverwrite_checkbutton.place(relx=.5, rely=.4, anchor="c")

gdate_checkbutton.pack()
gdate_checkbutton.place(relx=.5, rely=.2, anchor="c")

button = Button(root, text="Ok", width=10, height=2, command=close_window)
button.pack()
button.place(relx=.5, rely=.8, anchor="c")
gcurrent_directory = tk.filedialog.askdirectory()
root.mainloop()
gdeep = (IntVar.get(gdeep))
goverwrite = (IntVar.get(goverwrite))
gdate = (IntVar.get(gdate))


def pretty(d, indent=0, _filelist=""):
    for key, value in d.items():
        _filelist = _filelist + '\n' + '\t' * indent + str(key)
        if isinstance(value, dict):
            _filelist = pretty(value, indent + 1, _filelist)
        else:
            for i in value:
                _filelist = _filelist + '\n' + '\t' * (indent + 1) + '\t' + str(i)
    return _filelist

if gcurrent_directory:
    def listsort(current_directory, answer, deep, readonly, overwrite, date):
        if answer:
            pathdir = current_directory
            dirlist = []
            filelist = []
            filedic = {}
            if deep:
                for dirname, dirnames, filenames in os.walk(pathdir):
                    if 'NefSort.pyc' in filenames:
                        filenames.remove('NefSort.pyc')
                    for subdirname in dirnames:
                        dirlist.append(os.path.join(dirname, subdirname))

                    for filename in filenames:
                        filelist.append(
                            os.path.join(dirname, filename))  # вставить обработку файла не отдельно а прямо сюда


            else:
                filelist = [pathdir + '\\' + f for f in os.listdir(pathdir) if os.path.isfile(pathdir + '\\' + f)]

            for fileobj in filelist:
                filedate = time.ctime(os.path.getmtime(fileobj))
                filename, file_extension = os.path.splitext(fileobj)
                dir_name = file_extension[1:].upper()
                extdir = pathdir + '\\NefSort\\!' + file_extension[1:].upper()
                filedate_dir = extdir + '\\' + filedate[-5:]
                if date:
                    filedic.setdefault(dir_name, {})
                    filedic[dir_name].setdefault(str(filedate[-5:]), [])
                    filedic[dir_name][filedate[-5:]].append(os.path.basename(filename))
                else:
                    filedic.setdefault(file_extension[1:].upper(), [])
                    filedic[file_extension[1:].upper()].append(os.path.basename(filename))

                if not readonly and not date:
                    if not os.path.exists(extdir):
                        os.makedirs(extdir)
                    if overwrite and os.path.exists(extdir + '\\' + os.path.basename(filename) + file_extension):
                        if os.path.getmtime(fileobj) > os.path.getmtime(
                                                        extdir + '\\' + os.path.basename(filename) + file_extension):
                            os.remove(extdir + '\\' + os.path.basename(filename) + file_extension)
                            shutil.copy2(fileobj, extdir)
                    else:
                        if not os.path.exists(extdir + '\\' + os.path.basename(filename) + file_extension):
                            shutil.copy2(fileobj, extdir)
                if not readonly and date:
                    if not os.path.exists(filedate_dir):
                        os.makedirs(filedate_dir)
                    if overwrite and os.path.exists(filedate_dir + os.path.basename(filename) + file_extension):
                        if os.path.getmtime(fileobj) > os.path.getmtime(filedate_dir + '\\' + os.path.basename(filename) + file_extension):
                            os.remove(filedate_dir + '\\' + os.path.basename(filename) + file_extension)
                            shutil.copy2(fileobj, filedate_dir)
                    else:
                        if not os.path.exists(filedate_dir + '\\' + os.path.basename(filename) + file_extension):
                            shutil.copy2(fileobj, filedate_dir)

            return pretty(filedic)


    filesprint = listsort(gcurrent_directory, True, gdeep, True, False, gdate)
    root2 = Tk()
    root2.title("Before sorting, check the file list")
    root2.geometry("700x350")
    scroll = Scrollbar(root2)
    scroll.pack(side=RIGHT, fill=Y)
    text = Text(root2, width=680)
    text.insert(END, filesprint)
    text.pack(side=LEFT, fill=Y)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    root2.mainloop()

    root3 = Tk()
    root3.withdraw()
    ganswer = mb.askyesno(message="Are you sure you want to sort the data?")
    listsort(gcurrent_directory, ganswer, gdeep, False, goverwrite, gdate)

    root4 = Tk()
    root4.title("Success")
    root4.geometry("250x50")


    def close_window4():
        root4.destroy()
        raise SystemExit(0)


    button4 = Button(root4, text="Done!", width=10, height=2, command=close_window4)
    button4.pack()
    button4.place(relx=.5, rely=.5, anchor="c")
    root4.mainloop()


