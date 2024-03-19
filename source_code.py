import tkinter
import datetime
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import filedialog
from functools import partial
import os
from os import startfile
import mysql.connector
import pickle

connection = mysql.connector.connect(host='localhost',
                                     database='stegNtrans',
                                     user='root',
                                     password='password')
cursor = connection.cursor()

#decoding program
def decode_image_text_window():
    decode_image_text_window = tkinter.Toplevel()
    decode_image_text_window.title("decoding image")
    decode_image_text_window.geometry("700x400")
    decode_image_text_window.configure(background="azure2")
    logo4 = tkinter.Canvas(decode_image_text_window, width=100,
                           height=100, bg="azure2", bd=0)
    img4 = Image.open("logo_new.gif")
    img4 = img4.resize((100, 100))
    img_4 = ImageTk.PhotoImage(img4)
    logo4.create_image(100, 100, image=img_4, anchor="se")
    logo4.grid(column=0, row=0, sticky="w", padx=20, pady=10)
    appname = tkinter.Label(decode_image_text_window,
                            text="STEG N TRANS", bg="azure2", fg="dark orange",
                            font=("Comic Sans MS", 25))
    appname.place(x=150, y=30)

    changing_user = decode_tkinter.import_e_org.get(1.0, "end-1c")
    file_changed = decode_tkinter.import_e.get(1.0, "end-1c")
    f = open("ImageInfo.txt", "rb")
    try:
        while True:
            i = pickle.load(f)
            if i:
                if i["user"] == changing_user and i["filename_changed"] == file_changed:
                    ori = i["filename_original"]
                else:
                    messagebox.showerror("ERROR", "INCORRECT USER OR FILENAME!!")
    except EOFError:
        f.close()
    img = Image.open(ori)
    pixels = img.load()
    oimg = Image.open(file_changed)
    opixels = oimg.load()
    lst = []
    for i in range(oimg.size[0]):
        char = ""
        for j in range(0, 3):
            if pixels[i, j] != opixels[i, j]:
                for k in range(0, 3):
                    if opixels[i, j][k] % 2 == 0:
                        char = char + "0"
                    else:
                        char = char + "1"
            else:
                c = 0
                if j == 0:
                    if pixels[i, j+1] != opixels[i, j+1]:
                        c = c + 1
                    if pixels[i, j+2] != opixels[i, j+2]:
                        c = c + 1
                elif j == 1:
                    if pixels[i, j+2] != opixels[i, j+2]:
                        c = c + 1
                for a in range(i+1, oimg.size[0]):
                    for b in range(0, 3):
                        if pixels[a, b] != opixels[a, b]:
                            c = c + 1
                if c == 0:
                    break
                    break
                else:
                    for k in range(0, 3):
                        if opixels[i, j][k] % 2 == 0:
                            char = char + "0"
                        else:
                            char = char + "1"
        lst = lst + [char]
    new_lst = []
    for g in lst:
        f = ""
        f = f + g[0:8]
        new_lst = new_lst + [f]
    decimal = []
    for m in new_lst:
        sumb = 0
        p = 7
        for n in range(0, len(m)):
            sumb = sumb + (int(m[n]) * (2**(p)))
            p = p - 1
        decimal = decimal + [sumb]
    message = ""
    for o in decimal:
        message = message + chr(o)
    coded_img_msg = tkinter.Label(decode_image_text_window, text=message, bg="azure2", fg="black",
                                   font=("Consolas", 30))
    coded_img_msg.grid(column=2, row=2, padx=15, pady=15, columnspan=2)

#coded image
def file_explorer_code():
    global filename_de

    filename_de = filedialog.askopenfilename(title="Select an Image", initialdir="/", filetypes=(("png Files", "*.PNG*"),))

    decode_tkinter.import_e.insert(1.0, filename_de)


def open_file_decode():
    open_file_decode.has_been_called = True
    open_file_decode.filename = decode_tkinter.import_e.get(1.0, "end-1c")
    if len(open_file_decode.filename) == 0:
        messagebox.showerror("Input Error", "FILE NOT FOUND! Please enter a valid file name/path.")
    else:
        try:
            img = Image.open(open_file.filename)

        except FileNotFoundError:
            messagebox.showerror("Input Error", "FILE NOT FOUND! Please enter a valid file name/path.")
            open_file_decode.has_been_called = False
#decode tkinter
def decode_tkinter(x):
    if x == 1:
        decode_img = tkinter.Tk()
    if x == 2:
        decode_img = tkinter.Toplevel()
    decode_img.title("Image Selection")
    decode_img.geometry("1050x500")
    decode_img.configure(background="azure2")
    #logo
    logo = tkinter.Canvas(decode_img, width=100, height=100, bg="azure2", bd=0)
    img = Image.open("logo_new.gif")
    img = img.resize((100, 100))
    img_1 = ImageTk.PhotoImage(img)
    logo.create_image(100, 100, image=img_1, anchor="se")
    logo.grid(column=0, row=0, sticky="w", padx=20, pady=10)
    #label
    appname = tkinter.Label(decode_img, text="STEG N TRANS", bg="azure2", fg="dark orange", font=("Comic Sans MS", 25))
    appname.place(x=150, y=30)
    #selecting coded image
    for_import = tkinter.Label(decode_img, text="IMPORT CODED IMAGE FROM THE COMPUTER", bg="azure2", fg="black", font=("Consolas", 15))
    for_import.grid(column=0, row=1, padx=15, pady=15, columnspan=2)
    decode_tkinter.import_e = tkinter.Text(decode_img, width=55, height=1, font=("Consolas", 10))
    decode_tkinter.import_e.grid(column=2, row=1, padx=0, pady=15, sticky="w", columnspan=2)

    import_b = tkinter.Button(decode_img, text="Click to import", bg="white", fg="black", font=("Consolas", 10), command=file_explorer_code)
    import_b.grid(column=2, row=2, padx=40, pady=5, sticky="e")
    #username
    for_import_org = tkinter.Label(decode_img, text="WRITE USERNAME OF IMPORTED IMAGE:", bg="azure2", fg="black", font=("Consolas", 15))
    for_import_org.grid(column=0, row=3, padx=15, pady=15, columnspan=2)
    decode_tkinter.import_e_org = tkinter.Text(decode_img, width=55, height=1, font=("Consolas", 10))
    decode_tkinter.import_e_org.grid(column=2, row=3, padx=0, pady=15, sticky="w", columnspan=2)
    #decode button
    decode_button = tkinter.Button(decode_img, text="DECODE", width=15, bg="navy", fg="azure2", font=("Consolas", 20,'bold'),
                                   activeforeground='azure2', activebackground='black', command=decode_image_text_window)
    decode_button.grid(column=1, row=10, sticky="e", padx=10, pady=2)
#saving image tkinter
def final_window_image(newimage, file):
    input_text_window.text_win.withdraw()
    final_window_image.final = tkinter.Toplevel()
    final_window_image.final.title("Message Hidden")
    final_window_image.final.geometry("900x750")
    final_window_image.final.configure(background="azure2")

    logo3 = tkinter.Canvas(final_window_image.final, width=100, height=100, bg="azure2", bd=0)
    img3 = Image.open("logo_new.gif")
    img3 = img3.resize((100, 100))
    img_3 = ImageTk.PhotoImage(img3)
    logo3.create_image(100, 100, image=img_3, anchor="se")
    logo3.grid(column=0, row=0, sticky="w", padx=20, pady=10)
    appname3 = tkinter.Label(final_window_image.final, text="STEG N TRANS", bg="azure2", fg="dark orange", font=("Comic Sans MS", 25))
    appname3.place(x=120, y=30)

    final_display = tkinter.Canvas(final_window_image.final, width=500, height=300, bg="azure2", bd=0)
    finalimg = Image.open("temp_StegNTrans_" + hide.fin + ".png")
    finalimg = finalimg.resize((500, 300))
    final_img = ImageTk.PhotoImage(finalimg)
    final_display.create_image(500, 300, image=final_img, anchor="se")
    final_display.grid(column=0, row=1, padx=10, pady=30, sticky="w", rowspan=4)

    def sendto():
        print(8787)

    def savefile(newimage):
        def saveas():
            filename = filedialog.asksaveasfilename(title="Save Image as", initialdir="/", filetypes=(("PNG Files", "*.PNG*"),))
            savefile.path.insert(1.0, filename)
def savepng(newimage):
    filename_1 = savefile.path.get(1.0, "end-1c")
    if len(filename_1) == 0:
        messagebox.showerror("Input Error", "Please enter a valid file location.")
    else:
        try:
            newimage.save(filename_1 + ".png")
            messagebox.showinfo("Saved", "Image saved.")
        except FileNotFoundError:
            messagebox.showerror("Input Error", "FILE NOT FOUND! Please enter a valid file name/path.")
    f = open("ImageInfo.txt", "ab")
    if open_file.has_been_called == True:
        ofile = open_file.filename
    else:
        ofile = open_file_2.filename
    time1 = datetime.datetime.now()
    d = {"filename_changed": filename_1 + ".png", "user": str(l[0]), "filename_original": ofile, "timestamp": time1}
    pickle.dump(d, f)
    f.close()

    save = tkinter.Toplevel()
    save.title("Save as")
    save.geometry("400x150")
    name = tkinter.Label(save, text="Write the path of the location you want to save at or select the path:", font=("Consolas", 7), fg="black")
    name.grid(column=0, row=0, pady=10)
    savefile.path = tkinter.Text(save, width=55, height=1, font=("Consolas", 10))
    savefile.path.grid(column=0, row=1)
    choose = tkinter.Button(save, text="Choose Path", command=saveas)
    choose.grid(column=0, row=2)

    saveaspng = tkinter.Button(save, text="Save as PNG", command=partial(savepng, newimage))
    saveaspng.grid(column=0, row=4)

    save.mainloop()

    saveas = tkinter.Button(final_window_image.final, text="Save File", width=15, font=("Consolas", 20), command=partial(savefile, newimage))
    saveas.grid(column=1, row=1, padx=10, pady=10, sticky="n")

    backto = tkinter.Button(final_window_image.final, text="Try again", width=15, font=("Consolas", 20), command=partial(selection_window, 2))
    backto.grid(column=1, row=3, padx=10, pady=10, sticky="n")

    final_window_image.final.mainloop()
def hide(file, message):
    def inputcheck(file, message):
        im = Image.open(file, 'r')
        if 0.4 * im.size[0] >= len(message):
            binary = binarydata(message)
            return binary
        else:
            messagebox.showerror("Input Error", "CHARACTER LIMIT CROSSED! You can only input", 0.4 * im.size[0], "characters")

    def binarydata(x):
        binary = []
        for i in x:
            y = format(ord(i), "08b")
            binary = binary + [y]
        return binary

    binary = inputcheck(file, message)

    def changepixels(file, binary):
        allpixels = []
        im = Image.open(file, 'r')

        for i in range(0, len(binary)):
            pix_val_list = []
            for j in range(0, 3):
                pix_val = im.getpixel((i, j))
                pix_val_list.append(pix_val)

            r = 0
            pix_val_list_2 = []
            for k in range(0, 3):
                for m in range(0, 3):
                    if r < 8:
                        pixelx = int(pix_val_list[k][m])
                        digit = int(binary[i][r])
                        if digit == 0:
                            if pixelx % 2 == 0:
                                pix_val_list_2.append(pixelx)
                            else:
                                pix_val_list_2.append(pixelx + 1)
                        if digit == 1:
                            if pixelx % 2 == 0:
                                pix_val_list_2.append(pixelx + 1)
                            else:
                                pix_val_list_2.append(pixelx)
                        else:
                            break
                        r = r + 1
            pix_val_list_2.append(pix_val_list[2][2])

            def listtotuple(d):
                x = 0
                new_pixels = []
                for i in range(3):
                    t = (d[x + 0], d[x + 1], d[x + 2])
                    new_pixels = new_pixels + [t]
                    x = x + 3
                return new_pixels

            ab = listtotuple(pix_val_list_2)
            allpixels.append(ab)
        return allpixels

    newpixels = changepixels(file, binary)

    def putpixels(file, newpixels, binary):
        im = Image.open(file, 'r')
        originalpixel = im.load()
        new_img = Image.new(im.mode, im.size)
        draftpixels = new_img.load()
        w = 0
        for a in range(new_img.size[0]):
            for b in range(new_img.size[1]):
                if a <= len(binary) - 1 and b in [0, 1, 2] and w < len(binary):
                    draftpixels[a, b] = newpixels[w][b]
                else:
                    draftpixels[a, b] = originalpixel[a, b]
                w = w + 1
        im.close()
        hide.ext = ""
        for i in str(file):
            if i != "/" and i != ":":
                hide.ext = hide.ext + i
            else:
                hide.ext = hide.ext + "_"
        hide.fin = ""
        hide.fin = hide.fin + hide.ext[0:-4]
        new_img.save("temp_StegNTrans_" + hide.fin + ".png")
        return new_img

    new_img.close()
    newimage = putpixels(file, newpixels, binary)
    final_window_image(newimage, file)
# text tkinter window
def input_text_window(img):
    selection_window.select.withdraw()
    input_text_window.text_win = tkinter.Toplevel()
    input_text_window.text_win.title("Input Text")
    input_text_window.text_win.geometry("900x750")
    input_text_window.text_win.configure(background="azure2")

    logo2 = tkinter.Canvas(input_text_window.text_win, width=100, height=100, bg="azure2", bd=0)
    img2 = Image.open("logo_new.gif")
    img2 = img2.resize((100, 100))
    img_2 = ImageTk.PhotoImage(img2)
    logo2.create_image(100, 100, image=img_2, anchor="se")
    logo2.grid(column=0, row=0, sticky="w", padx=20, pady=10)
    appname2 = tkinter.Label(input_text_window.text_win, text="STEG N TRANS", bg="azure2", fg="dark orange", font=("Comic Sans MS", 25))
    appname2.place(x=120, y=30)
    input_text = tkinter.Label(input_text_window.text_win, text="Enter the message you want to hide:", bg="azure2", fg="black", font=("Consolas", 15))
    input_text.grid(column=0, row=1, sticky="nw", pady=30, padx=5)

    img_1 = Image.open(img)
    x = img_1.size[0]

    char_lim = tkinter.Label(input_text_window.text_win, text="Character Limit:" + str(int(0.4 * x)))
    char_lim.grid(column=0, row=1, pady=40)

    text_box = tkinter.Text(input_text_window.text_win, height=10, width=35, font=("Georgia", 15))
    text_box.grid(column=1, row=1, padx=5, pady=30)

    def get():
        get.message = text_box.get(1.0, "end-1c")
        if get.message == "":
            messagebox.showerror("Input Error", "NO TEXT FOUND!!")
        else:
            hide(img, get.message)

    hide_message = tkinter.Button(input_text_window.text_win, text="HIDE MESSAGE", command=get, width=20, font=("Georgia", 25))
    hide_message.grid(column=1, row=2, padx=10, pady=10)
    input_text_window.text_win.mainloop()
# steganography of image
def open_file_2(a):
    open_file_2.filename = "selectimage" + str(a) + ".jpg"
    input_text_window(open_file_2.filename)

def file_explorer():
    filename_1 = filedialog.askopenfilename(title="Select an Image", initialdir="/", filetypes=(("JPEG Files", "*.jpg*"), ("PNG Files", "*.png*")))

    selection_window.import_e.insert(1.0, filename_1)

def open_file():
    open_file.has_been_called = True
    open_file.filename = selection_window.import_e.get(1.0, "end-1c")
    if len(open_file.filename) == 0:
        messagebox.showerror("Input Error", "FILE NOT FOUND! Please enter a valid file name/path.")
    else:
        try:
            img = Image.open(open_file.filename)
            input_text_window(open_file.filename)
        except FileNotFoundError:
            messagebox.showerror("Input Error", "FILE NOT FOUND! Please enter a valid file name/path.")
    open_file.has_been_called = False
# selecting image for steganography
def selection_window(x):
    if x == 1:
        selection_window.select = tkinter.Toplevel()
    if x == 2:
        selection_window.select = tkinter.Toplevel()
        final_window_image.final.withdraw()
        os.remove("temp_StegNTrans_" + hide.fin + ".png")

    selection_window.select.title("Image Selection")
    selection_window.select.geometry("900x850")
    selection_window.select.configure(background="azure2")

    logo = tkinter.Canvas(selection_window.select, width=100, height=100, bg="azure2", bd=0)
    img = Image.open("logo_new.gif")
    img = img.resize((100, 100))
    img_1 = ImageTk.PhotoImage(img)
    logo.create_image(100, 100, image=img_1, anchor="se")
    logo.grid(column=0, row=0, sticky="w", padx=20, pady=10)
    appname = tkinter.Label(selection_window.select, text="STEG N TRANS", bg="azure2", fg="dark orange",
                            font=("Comic Sans MS", 25))
    appname.place(x=150, y=30)

    for_import = tkinter.Label(selection_window.select, text="IMPORT IMAGE FROM THE COMPUTER:", bg="azure2",
                               fg="black", font=("Consolas", 15))
    for_import.grid(column=0, row=1, padx=15, pady=15, columnspan=2)
    selection_window.import_e = tkinter.Text(selection_window.select, width=55, height=1, font=("Consolas", 10))
    selection_window.import_e.grid(column=2, row=1, padx=0, pady=15, sticky="w", columnspan=2)

    import_b = tkinter.Button(selection_window.select, text="Click to import", bg="white", fg="black",
                              font=("Consolas", 10), command=file_explorer)
    import_b.grid(column=2, row=2, padx=40, pady=5, sticky="e")
    convert_b = tkinter.Button(selection_window.select, text="Use Image", bg="white", fg="black",
                                font=("Consolas", 10), command=open_file)
    convert_b.grid(column=2, row=3, padx=60, pady=5, sticky="e")

    for_selection = tkinter.Label(selection_window.select, text="OR SELECT AN IMAGE:", justify="left",
                                   bg="azure2", fg="black", font=("Consolas", 15))
    for_selection.grid(column=0, row=4, pady=15, padx=20, sticky="w")

    image_1 = tkinter.Canvas(selection_window.select, width=180, height=100, bg="azure2", bd=0)
    img_11 = Image.open("selectimage1_new.gif")
    img_11 = img_11.resize((180, 100))
    img_12 = ImageTk.PhotoImage(img_11)
    image_1.create_image(180, 100, image=img_12, anchor="se")
    image_1.grid(column=0, row=5, sticky="w", padx=10, pady=10)
    button_1 = tkinter.Button(selection_window.select, text="Use This Image", width=25, command=partial(open_file_2, 1))
    button_1.grid(column=0, row=6, sticky="w", padx=10, pady=2)

    image_2 = tkinter.Canvas(selection_window.select, width=180, height=100, bg="azure2", bd=0)
    img_22 = Image.open("selectimage2_new.gif")
    img_22 = img_22.resize((180, 100))
    img_23 = ImageTk.PhotoImage(img_22)
    image_2.create_image(180, 100, image=img_23, anchor="se")
    image_2.grid(column=1, row=5, padx=15, pady=10, sticky="e")
    button_2 = tkinter.Button(selection_window.select, text="Use This Image", width=25, command=partial(open_file_2, 2))
    button_2.grid(column=1, row=6, padx=15, pady=2, sticky="e")

    image_3 = tkinter.Canvas(selection_window.select, width=180, height=100, bg="azure2", bd=0)
    img_33 = Image.open("selectimage3_new.gif")
    img_33 = img_33.resize((180, 100))
    img_34 = ImageTk.PhotoImage(img_33)
    image_3.create_image(180, 100, image=img_34, anchor="se")
    image_3.grid(column=2, row=5, sticky="e", padx=0, pady=10)
    button_3 = tkinter.Button(selection_window.select, text="Use This Image", width=25, command=partial(open_file_2, 3))
    button_3.grid(column=2, row=6, sticky="e", padx=0, pady=2)

    image_4 = tkinter.Canvas(selection_window.select, width=180, height=100, bg="azure2", bd=0)
    img_44 = Image.open("selectimage4_new.gif")
    img_44 = img_44.resize((180, 100))
    img_45 = ImageTk.PhotoImage(img_44)
    image_4.create_image(180, 100, image=img_45, anchor="se")
    image_4.grid(column=0, row=7, sticky="w", padx=10, pady=15)
    button_4 = tkinter.Button(selection_window.select, text="Use This Image", width=25, command=partial(open_file_2, 4))
    button_4.grid(column=0, row=8, sticky="w", padx=10, pady=2)

    image_5 = tkinter.Canvas(selection_window.select, width=180, height=100, bg="azure2", bd=0)
    img_55 = Image.open("selectimage5_new.gif")
    img_55 = img_55.resize((180, 100))
    img_56 = ImageTk.PhotoImage(img_55)
    image_5.create_image(180, 100, image=img_56, anchor="se")
    image_5.grid(column=1, row=7, padx=15, pady=15, sticky="e")
    button_5 = tkinter.Button(selection_window.select, text="Use This Image", width=25, command=partial(open_file_2, 5))
    button_5.grid(column=1, row=8, padx=15, pady=2, sticky="e")

    image_6 = tkinter.Canvas(selection_window.select, width=180, height=100, bg="azure2", bd=0)
    img_66 = Image.open("selectimage6_new.gif")
    img_66 = img_66.resize((180, 100))
    img_67 = ImageTk.PhotoImage(img_66)
    image_6.create_image(180, 100, image=img_67, anchor="se")
    image_6.grid(column=2, row=7, sticky="e", padx=0, pady=15)
    button_6 = tkinter.Button(selection_window.select, text="Use This Image", width=25, command=partial(open_file_2, 6))
    button_6.grid(column=2, row=8, sticky="e", padx=0, pady=2)

    image_7 = tkinter.Canvas(selection_window.select, width=180, height=100, bg="azure2", bd=0)
    img_77 = Image.open("selectimage7_new.gif")
    img_77 = img_77.resize((180, 100))
    img_78 = ImageTk.PhotoImage(img_77)
    image_7.create_image(180, 100, image=img_78, anchor="se")
    image_7.grid(column=0, row=9, sticky="w", padx=10, pady=15)
    button_7 = tkinter.Button(selection_window.select, text="Use This Image", width=25, command=partial(open_file_2, 7))
    button_7.grid(column=0, row=10, sticky="w", padx=10, pady=2)

    image_8 = tkinter.Canvas(selection_window.select, width=180, height=100, bg="azure2", bd=0)
    img_88 = Image.open("selectimage8_new.gif")
    img_88 = img_88.resize((180, 100))
    img_89 = ImageTk.PhotoImage(img_88)
    image_8.create_image(180, 100, image=img_89, anchor="se")
    image_8.grid(column=1, row=9, padx=15, pady=15, sticky="e")
    button_8 = tkinter.Button(selection_window.select, text="Use This Image", width=25, command=partial(open_file_2, 8))
    button_8.grid(column=1, row=10, padx=15, pady=2, sticky="e")

    image_9 = tkinter.Canvas(selection_window.select, width=180, height=100, bg="azure2", bd=0)
    img_99 = Image.open("selectimage9_new.gif")
    img_99 = img_99.resize((180, 100))
    img_910 = ImageTk.PhotoImage(img_99)
    image_9.create_image(180, 100, image=img_910, anchor="se")
    image_9.grid(column=2, row=9, sticky="e", padx=0, pady=15)
    button_9 = tkinter.Button(selection_window.select, text="Use This Image", width=25, command=partial(open_file_2, 9))
    button_9.grid(column=2, row=10, sticky="e", padx=0, pady=2)

    selection_window.select.mainloop()
# sign out tkinter window
def signout_page():
    out = tkinter.Tk()
    out.title('Steg-N-Trans')
    out.geometry('700x400')
    out.configure(background="azure2")
    close_button = tkinter.Button(out, text="Tap the button to close the application", bg="navy",
                                  fg="azure2", font=("Consolas", 25, 'italic'),
                                  activeforeground='azure2', activebackground='black',
                                  command=out.withdraw)
    close_button.pack()

def up_password():
    createpass = tkinter.StringVar()
    confirmpass = tkinter.StringVar()

    def checkpassword():
        a = createpassmessage.get()
        b = confirmpassmessage.get()
        if a == "" or b == "":
            messagebox.showwarning("showwarning", "Entries are incomplete")
        else:
            if a == b:
                # updating password in database
                update_data = "UPDATE user_info SET pass_word=%s WHERE user_name =%s"
                infoup = (str(a), str(l[0]),)
                cursor.execute(update_data, infoup)
                connection.commit()
                messagebox.showinfo("showinfo", "Successfully Updated")

    up_pass = tkinter.Tk()
    up_pass.title("Update Password")
    up_pass.geometry('700x400')
    up_pass.configure(background="azure2")
    head_1 = tkinter.Label(up_pass, text="Update password", bg="azure2",
                           fg="black", font=("Consolas", 30, 'bold')).grid(column=1, row=1)
    # create password
    user_createpass = tkinter.Label(up_pass, text="Create password", bg="azure2",
                                    fg="black", font=("Consolas", 20)).grid(column=0, row=3, pady=10, padx=10)
    createpassmessage = tkinter.Entry(up_pass, textvariable=createpass, font=("Consolas", 20), show='*')
    createpassmessage.grid(column=1, row=3, pady=10, padx=10)
    # confirm password
    user_confirmpass = tkinter.Label(up_pass, text="Confirm password", bg="azure2",
                                     fg="black", font=("Consolas", 20)).grid(column=0, row=4, pady=10, padx=10)
    confirmpassmessage = tkinter.Entry(up_pass, textvariable=confirmpass, font=("Consolas", 20), show='*')
    confirmpassmessage.grid(column=1, row=4, pady=10, padx=10)
    confirm_button = tkinter.Button(up_pass, text="update", bg="navy", fg="azure2",
                                    font=("Consolas", 25, "italic"), activeforeground="azure2",
                                    activebackground="black",
                                    command=lambda: [checkpassword(), up_pass.withdraw(), control.withdraw(), log_in()])
    confirm_button.grid(column=1, row=5, padx=10, pady=10)
def user_infopage():
    # basic window formation
    user_page = tkinter.Tk()
    user_page.title("User Info")
    user_page.geometry('700x400')
    user_page.configure(background="azure2")
    head_1 = tkinter.Label(user_page, text="User Information", bg="azure2",
                           fg="black", font=("Consolas", 30, 'bold')).grid(column=1, row=1)
    ID_lab = tkinter.Label(user_page, text="USER ID:", bg="azure2",
                           fg="black", font=("Consolas", 15, 'italic')).grid(row=2, padx=10, pady=10)
    name_lab = tkinter.Label(user_page, text="Name:", bg="azure2",
                             fg="black", font=("Consolas", 15, 'italic')).grid(row=3, padx=10, pady=10)
    mail_lab = tkinter.Label(user_page, text="Mail ID:", bg="azure2",
                             fg="black", font=("Consolas", 15, 'italic')).grid(row=4, padx=10, pady=10)
    pass_lab = tkinter.Label(user_page, text="Password:", bg="azure2",
                             fg="black", font=("Consolas", 15, 'italic')).grid(row=5, padx=10, pady=10)
    
    # showing information from MySQL
    sql = "SELECT * FROM user_info WHERE user_name = %s AND pass_word=%s"
    us_info = (l[0], l[1],)
    cursor.execute(sql, us_info)
    myresult = cursor.fetchall()
    for i in myresult:
        ID_ans = tkinter.Label(user_page, text=i[0], bg="azure2",
                               fg="black", font=("Consolas", 15, 'italic')).grid(column=1, row=2, padx=10, pady=10)
        name_ans = tkinter.Label(user_page, text=i[1], bg="azure2",
                                 fg="black", font=("Consolas", 15, 'italic')).grid(column=1, row=3, padx=10, pady=10)
        mail_ans = tkinter.Label(user_page, text=i[2], bg="azure2",
                                 fg="black", font=("Consolas", 15, 'italic')).grid(column=1, row=4, padx=10, pady=10)
        pass_ans = tkinter.Label(user_page, text=i[3], bg="azure2",
                                 fg="black", font=("Consolas", 15, 'italic')).grid(column=1, row=5, padx=10, pady=10)

    # updation buttons
    update_password = tkinter.Button(user_page, text="Update Password", bg="navy",
                                     fg="azure2", font=("Consolas", 15, 'italic'),
                                     activeforeground='azure2', activebackground='black',
                                     command=lambda: [user_page.withdraw(), up_password()]).grid(column=1, row=6, padx=10, pady=10)
def control_page():
    global control
    control = tkinter.Tk()
    control.title("Steg N Trans")
    control.geometry('700x400')
    control.configure(background="azure2")
    head_1 = tkinter.Label(control, text="Steg-N-Trans \n Welcome " + str(l[0]), bg="azure2",
                            fg="orange", font=("Consolas", 30, 'bold')).pack(padx=10, pady=10)
    # buttons of control page
    coding_button = tkinter.Button(control, text="Code a message", bg="navy", fg="azure2",
                                    font=("Consolas", 15, 'italic'), activeforeground='azure2',
                                    activebackground='black', command=partial(selection_window, 1)).pack(padx=10, pady=10)
    decoding_button = tkinter.Button(control, text="Decode a message", bg="navy",
                                      fg="azure2", font=("Consolas", 15, 'italic'), activeforeground='azure2',
                                      activebackground='black', command=partial(decode_tkinter, 2)).pack(padx=10, pady=10)
    userinfo_button = tkinter.Button(control, text="User Info", bg="navy", fg="azure2",
                                     font=("Consolas", 15, 'italic'), activeforeground='azure2',
                                     activebackground='black', command=user_infopage).pack()
    signout_button = tkinter.Button(control, text="Sign Out", bg="navy", fg="azure2",
                                    font=("Consolas", 25, 'italic'), activeforeground='azure2',
                                    activebackground='black',
                                    command=lambda: [control.withdraw(), signout_page()]).pack(padx=10, pady=10)
def log_in():
    # taking information from user
    log_in.user_info = tkinter.StringVar()
    pass_info = tkinter.StringVar()

    def check_info():
        a = user_message.get()
        b = pass_message.get()
        global l
        l = [a, b]
        check = "SELECT * FROM user_info"
        cursor.execute(check)
        information = cursor.fetchall()
        length = len(information)
        for i in range(length):
            if information[i][1] == a and information[i][3] == b:
                messagebox.showinfo("showinfo", "Welcome " + str(l[0]))
                log.withdraw()
                control_page()
                break
            else:
                messagebox.showwarning("showwarning", "Invalid Password or Invalid Username")

    main.withdraw()
    global log
    log = tkinter.Tk()
    log.title("Steg N Trans")
    log.geometry('650x400')
    log.configure(background="azure2")
    head_1 = tkinter.Label(log, text="#LOG IN#", bg="azure2",
                           fg="black", font=("Consolas", 20, 'bold')).grid(column=1, row=0, pady=10, padx=10)

    # user name
    user_name = tkinter.Label(log, text="User Name", bg="azure2",
                              fg="black", font=("Consolas", 20)).grid(column=0, row=1, pady=10, padx=10)
    user_message = tkinter.Entry(log, textvariable=log_in.user_info,
                                  font=("Consolas", 20))
    user_message.grid(column=1, row=1, pady=10, padx=10)
    # password
    pass_word = tkinter.Label(log, text="Password", bg="azure2",
                              fg="black", font=("Consolas", 20)).grid(column=0, row=2, pady=10, padx=10)
    pass_message = tkinter.Entry(log, textvariable=pass_info,
                                  font=("Consolas", 20), show="*")
    pass_message.grid(column=1, row=2, pady=10, padx=10)
    # log in button
    log_button = tkinter.Button(log, text="Log In",
                                bg="navy", fg="azure2", font=("Consolas", 25, 'italic'), activeforeground='azure2',
                                activebackground='black', command=check_info).grid(column=1, row=4, pady=10, padx=10)


def sign_in():
    user_nameinfo = tkinter.StringVar()
    user_mailinfo = tkinter.StringVar()
    user_createpassinfo = tkinter.StringVar()
    user_confirmpassinfo = tkinter.StringVar()

    def checkpass():
        a = user_namemessage.get()
        b = user_mailmessage.get()
        c = user_createpassmessage.get()
        d = user_confirmpassmessage.get()

        if a == "" or b == "" or c == "" or d == "":
            messagebox.showwarning("showwarning", "Entries are incomplete")
        else:
            if c == d:
                # inserting data in database
                insert_data = ("INSERT INTO user_info(user_name,user_mailID,pass_word) VALUES(%s,%s,%s)")
                e = (a, b, c)
                cursor.execute(insert_data, e)
                connection.commit()
                messagebox.showinfo("showinfo", "successfully signed in")
                log_in()
                sign.withdraw()
            elif c != d:
                messagebox.showwarning("showwarning", "Invalid password")
            if a == "":
                messagebox.showwarning("showwarning", "User Name is not entered")

    main.withdraw()
    sign = tkinter.Tk()
    sign.title("Steg N Trans")
    sign.geometry('650x400')
    sign.configure(background="azure2")
    head_1 = tkinter.Label(sign, text="#SIGN IN#", bg="azure2",
                            fg="black", font=("Consolas", 20, 'bold')).grid(column=1, row=0, pady=10, padx=10)
    # user name
    user_name = tkinter.Label(sign, text="User Name", bg="azure2",
                              fg="black", font=("Consolas", 20)).grid(column=0, row=1, pady=10, padx=10)
    user_namemessage = tkinter.Entry(sign, textvariable=user_nameinfo, font=("Consolas", 20))
    user_namemessage.grid(column=1, row=1, pady=10, padx=10)
    # mail id
    user_mail = tkinter.Label(sign, text="User Mail ID", bg="azure2",
                               fg="black", font=("Consolas", 20)).grid(column=0, row=2, pady=10, padx=10)
    user_mailmessage = tkinter.Entry(sign, textvariable=user_mailinfo, font=("Consolas", 20))
    user_mailmessage.grid(column=1, row=2, pady=10, padx=10)
    # create password
    user_createpass = tkinter.Label(sign, text="Create password", bg="azure2",
                                     fg="black", font=("Consolas", 20)).grid(column=0, row=3, pady=10, padx=10)
    user_createpassmessage = tkinter.Entry(sign, textvariable=user_createpassinfo,
                                            font=("Consolas", 20), show='*')
    user_createpassmessage.grid(column=1, row=3, pady=10, padx=10)
    # confirm password
    user_confirmpass = tkinter.Label(sign, text="Confirm password", bg="azure2",
                                      fg="black", font=("Consolas", 20)).grid(column=0, row=4, pady=10, padx=10)
    user_confirmpassmessage = tkinter.Entry(sign, textvariable=user_confirmpassinfo,
                                             font=("Consolas", 20), show='*')
    user_confirmpassmessage.grid(column=1, row=4, pady=10, padx=10)
    # checking create password and confirm password are same
    sign_button = tkinter.Button(sign, text="Sign In", bg="navy", fg="azure2",
                                  font=("Consolas", 25, "italic"), activeforeground="azure2",
                                  activebackground="black", command=checkpass)
    sign_button.grid(column=1, row=5, padx=10, pady=10)

# introduction page
main = tkinter.Tk()
main.title("Steg N Trans")
main.geometry('800x800')
main.configure(background="azure2")
lbl = tkinter.Label(main, text="Steg N Trans", bg="azure2", fg="black", font=("Consolas", 40)).pack()
logo = tkinter.Canvas(main, width=300, height=300, bg='azure2', bd=0)
img = Image.open("logo_new.gif")
img = img.resize((200, 200))
img = ImageTk.PhotoImage(img)
logo.create_image(150, 150, image=img)
logo.pack(padx=50, pady=50)
lbl = tkinter.Label(main, text="CREATED BY: DISHA AND NIDHI", bg="azure2", fg="black", font=("Consolas", 25, 'italic')).pack(padx=10, pady=10)
lbl = tkinter.Label(main, text="Passionate about programming....", bg="azure2", fg="black", font=("Consolas", 25, 'italic')).pack(padx=10, pady=10)
# main page button
main_button = tkinter.Button(main, text="Log In", bg="navy", fg="azure2", font=("Consolas", 25, 'italic'), activeforeground='azure2', activebackground='black', command=log_in).pack(padx=10, pady=10)
# sign in button
sign_button = tkinter.Button(main, text="Sign In", bg="navy", fg="azure2", font=("Consolas", 25, 'italic'), activeforeground='azure2', activebackground='black', command=sign_in).pack(padx=10, pady=10)
main.mainloop()

