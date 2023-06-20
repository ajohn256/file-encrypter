from tkinter.messagebox import showinfo,showwarning,showerror
from tkinter import *
from tkinter.ttk import Progressbar
import time
import threading
from cryptography.fernet import Fernet
import os


root = Tk()
root.geometry("400x500")
active = True
decrypted = False

head_label = Label(root,text="MULTIPLE FILE ENCRYPTION TOOL.",relief='sunken',font="Monserrat")
head_label.pack(anchor="center",ipady=4,ipadx=8)

frame1 = LabelFrame(root)
frame1.pack(fill=X,padx=8,pady=8,ipadx=5)

frame2 = LabelFrame(root)
frame2.pack(fill=X,padx=8,pady=8,ipadx=5)

frame3 = LabelFrame(root)
frame3.pack(fill=X,padx=8,pady=8,ipadx=5)

menubar = Menu(root)
root.config(menu=menubar)

filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=filemenu)
menubar.add_cascade(label="Logs")
menubar.add_cascade(label="About")
menubar.add_cascade(label="Help")

filemenu.add_command(label="New")
filemenu.add_command(label="Save")
filemenu.add_command(label="Save as")

#encrypting data
label_encrypt = Label(frame1,text="Encrypt and lock files")
label_encrypt.pack(anchor="center",ipady=4,ipadx=8)

paths_encrypt = Entry(frame1)
paths_encrypt.pack(side="left",fill=X,padx=10,pady=10,expand=True,ipady=10)

#decryption algorithm
#decrypting frame
label_decrypt = Label(frame2,text="Decrypt locked files")
label_decrypt.pack(anchor="center",ipady=4,ipadx=8)

paths_decrypt = Entry(frame2)
paths_decrypt.pack(side="left",fill=X,padx=10,pady=10,expand=True,ipady=10)

label_decrypt = Label(frame3,text="Enter decryption key in space below")
label_decrypt.pack(anchor="center",ipady=4,ipadx=8)

unlock_key = Entry(frame3)
unlock_key.pack(side="left",fill=X,padx=10,pady=10,expand=True,ipady=5)

def clear_all():
    paths_decrypt.delete(0,END)
    paths_encrypt.delete(0,END)
    unlock_key.delete(0,END)

def show(task):
    showinfo(f"{task}",f"{task} is complete locate the {task} key in key.key file")
    print(paths_encrypt.get())

def encrypt_data(path):
    global decrypted
    decrypted = False
    if path != "":
        key = Fernet.generate_key()
        with open(f"{path}\key.key","wb") as key_file:
            key_file.write(key)
            key_file.close()
        
        try:
            files = os.listdir(path)
            


            for file in files:
                if os.path.isdir(file) or file == "lock.py" or file == "key.key":
                    pass
                
                else:
                
                    dirs = f"{path}\{file}"
                    with open(dirs,"rb") as org_file:
                        data = org_file.read()
                        encrypted_data = Fernet(key).encrypt(data)

                    with open(dirs,"wb") as enc_file:
                        enc_file.write(encrypted_data)
                        enc_file.close()
            
            show("Encrypted!")
            
        
        except Exception as e:
            showerror("Error",f"{e}")

    else:
        showerror("Empty","Empty fields detected, please fill them!")

def decrypt_data(path):
    global decrypted
    key = unlock_key.get()

    if path != '':
        files = os.listdir(path)

       
        try:
            for file in files:
                if os.path.isdir(file) or file == "lock.py" or file == "key.key" or decrypted is True:
                    pass
                
                else:
                    dirs = f"{path}\{file}"
                    with open(dirs,"rb") as enc_file:
                        data = enc_file.read()
                        decrypted_data = Fernet(key).decrypt(data)

                        with open(dirs,"wb") as dec_file:
                            dec_file.write(decrypted_data)
                            dec_file.close()

            showinfo("Success","Decryption completed successfully!")
            decrypted = True
           
                        
        except Exception as e:
            print(e) 
            showerror("Invalid",f"Invalid decryption key,  {e}")   
        
    else:
        showerror("No file","Empty fields present please fill them to decrypt files!")            
            

def load():
    start_time = time.time()
    global active
    val = 10
    while val <= 100 and active is True:
        val += 10
        if val == 100 and active is True:
            bar = Progressbar(root,maximum=100,value=val)
            bar.pack(fill=X)
            progress = Label(root,text=f"Completed, files locked {val}%")
            progress.pack(anchor="center",ipady=1,ipadx=8)
            active = False
            show("decryption")
            break
        
        elif val < 100 and active is True:
            bar = Progressbar(root,maximum=100,value=val)
            bar.pack(fill=X)
            progress = Label(root,text=f"Locking files {val}%")
            progress.pack(anchor="center",ipady=1,ipadx=8)
            time.sleep(0.1)
            bar.destroy()
            progress.destroy()
        
        else:
            pass
    

def start():
    thread = threading.Thread(target=load,)
    thread.start()


#encrypt cta
encrypt_cta = Button(frame1,text="Encrypt data!",padx=10,pady=7,command=lambda:encrypt_data(paths_encrypt.get()))
encrypt_cta.pack(anchor="center",ipadx=6,ipady=4,side="left")

#encrypt cta
decrypt_cta = Button(frame3,text="Decrypt files!",padx=10,pady=7,command=lambda:decrypt_data(paths_decrypt.get()))
decrypt_cta.pack(anchor="center",ipadx=6,ipady=4,side="left")

#clear inputs
clear_cta = Button(root,text="Clear all",state='active',padx=10,pady=7,command=lambda:clear_all())
clear_cta.pack(anchor="center",fill=X,padx=10,pady=5)


label_maker = Label(root,text="@ariko",padx='10',pady='12').pack()

while True:
    root.mainloop()