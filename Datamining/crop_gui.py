import tkinter as tk
from tkinter.ttk import *
import tkinter.filedialog as fd
from crop_advisor import *
import string
from tkinter.messagebox import askyesno,showinfo
from decision_tree_crop import *
from threading import Thread
widgets=[]
res_widget=[]
global known_district_listbox
global season
global inpt_lf
#dt
dt_dn=''; dt_sn=''
dt_inpt_lf=''
dt_district_input=''
district_label_inpt=''
season_label_inpt=''
area_label_inpt=''
dt_season_input=''
dt_arae_input=''
dt_widgets=[]
dt_filename=''
dt_label=''
def call_getbestcrop():
    global res_widget
    global inpt_lf
    if res_widget:
        for e in res_widget:
            e.destroy()
        res_widget=[]
    try:
        dn=known_district_listbox.get(known_district_listbox.curselection())
        sn=season.get()
    except  Exception:
        status_label.config(text='select both district and season')
    else:
        if dn and sn:
            status_label.config(text='Findng crop for district :'+dn+' season:'+sn+'...')
            res=get_bestcrop(dn,sn)
            #-->res_lf <root->child5> labelframe
            res_lf=tk.LabelFrame(inpt_lf,text='[Result]',font=('Courier 15 bold'))
            res_lf.pack(fill='y')
            #append it
            res_widget.append(res_lf)
            #->res_label
            res_str='District->'+dn+' Season->'+sn+'\n'+'-'*30+'\nSEASON | CROP | PROD/AREA\n'+'-'*30+'\n'
            season_predict=''
            wholeyear_predict=''
            for es in res:
                for r in es:
                    if r==sn:
                        season_predict=es[r][0],es[r][1]
                    if r.lower().strip()=='whole year':
                        wholeyear_predict=es[r][0],es[r][1]
                    res_str+=r+' | '+es[r][0]+' | '+str(es[r][1])+'\n'
            res_label=tk.Label(res_lf,font=('Courier 12 '),text=res_str,justify='left',fg='goldenrod1',bg='black')
            res_label.pack(fill='x')
            predict_str=''
            #check for season and whole year
            if season_predict[1]>=wholeyear_predict[1]:
                predict_str='For District:'+dn+' in season:'+sn+'\ncrop should be:'+season_predict[0]
            else:
                predict_str='[whole year]For District:'+dn+' in season:'+sn+'\ncrop should be:'+season_predict[0]+'\nBut according to high p/a crop is:'+wholeyear_predict[0]
            #-->predict_lf 
            predict_lf=tk.LabelFrame(frame_naive,text='[Prediction]',font=('Courier 15 bold'),bg='black',fg='lawngreen')
            predict_lf.pack(fill='x')
            #->predict_label
            predict_label=tk.Label(predict_lf,font=('Courier 12'),bg='black',fg='darkorange1')
            predict_label.pack(fill='x',side='left')
            predict_label.config(text=predict_str)
            #append predict_res
            res_widget.append(predict_lf)
            status_label.config(text='Done finding crops.')
        else:
            status_label.config(text='select both district and season')

def get_dt_result(event):
    global dt_filename
    global dt_inpt_lf
    global inpt_lf
    global dt_widgets
    global dt_label
    global prediction
    if isinstance(dt_widgets[-1],(tk.LabelFrame)):
        dt_widgets[-1].destroy()
        dt_widgets=dt_widgets.pop(-1)
    fn=dt_filename
    dn=dt_district_input.get().upper().strip()
    sn=dt_season_input.get().title()+' '*5
    ar=dt_area_input.get()
    start=time.time()
    try:
        crop=iter_find_best_crop(fn,[(dn,sn,int(ar))],dt_status_label)
        dt_status_label.config(text='[Decision Tree]Crop prediction Started...')
        stop=time.time()
        crop_str='='*30+'\nCrop    | Class \n'+'='*30
        for ind,crop in enumerate(crop[0]):
            crop_str+='\n'+crop[0]+'    |'+str(crop[1])+'\n'+'-'*30
        #dt_res_lf
        dt_res_lf=tk.LabelFrame(dt_label,text='[Prediction]',font=('Courier 15 bold'))
        dt_res_lf.pack(fill='x')
        #label for result
        dt_label_res=tk.Label(dt_res_lf,text=crop_str+'\nTime required : '+str(stop-start)+' sec',justify='left',bg='black',fg='darkorange1',font=('Courier 12 bold'))
        dt_label_res.pack(fill='x')
        #append it in dt_widgets
        dt_widgets.append(dt_res_lf)
        dt_status_label.config(text='[Decision Tree]Done finding crops.')
    except ValueError:
        dt_status_label.config(text='Number is required!!!')
def append_area(event):
    global dt_widgets
    global dt_sn
    global sesaon_label_inpt
    global dt_season_input
    global dt_inpt_lf
    global area_label_inpt
    global dt_area_input
    global dt_label
    #print(dt_sn)
    if dt_season_input.get().title()  in [e.strip() for e in dt_sn] and len(dt_season_input.get())>0:
         #districti_label_inpt_lf
        area_label_inpt=tk.Label(dt_label)
        area_label_inpt.pack(fill='x')
        #distritc_label_lf
        area_label=tk.Label(area_label_inpt,text='Enter Area:',font=('Courier 12 bold'))
        area_label.pack(side='left')
        #district_label_lf
        dt_area_input=tk.Entry(area_label_inpt,font=('Courier 12 bold'))
        dt_area_input.pack(side='right')
        dt_area_input.focus()
        dt_area_input.bind('<Return>',get_dt_result)
        dt_widgets.append(area_label_inpt)
        dt_status_label.config(text='[Decision Tree]Season Found.')

    else:
        #print(dt_widgets)
        for wid in dt_widgets[2:]:
            wid.destroy()
        dt_widgets[2:]=[]
        dt_status_label.config(text='[Decision Tree]season Not Found!!!.')
def append_season(event):
    global dt_dn;global dt_sn;global dt_inpt_lf
    global season_label_inpt;global dt_season_input
    global district_label_inpt
    global dt_label
    if dt_district_input.get().upper().strip()in dt_dn and len(dt_district_input.get())>0:
        #districti_label_inpt_lf
        season_label_inpt=tk.Label(dt_label)
        season_label_inpt.pack(fill='x')
        #distritc_label_lf
        season_label=tk.Label(season_label_inpt,text='Enter Season:',font=('Courier 12 bold'))
        season_label.pack(side='left')
        #district_label_lf
        dt_season_input=tk.Entry(season_label_inpt,font=('Courier 12 bold'))
        dt_season_input.pack(side='right')
        dt_season_input.focus()
        dt_season_input.bind('<Return>',append_area)
        dt_season_input.bind('<KeyRelease>',append_area)
        dt_widgets.append(season_label_inpt)
        dt_status_label.config(text='[Decision Tree]District Found.')

    else:
        #print(dt_widgets)
        for wid in dt_widgets[1:]:
            wid.destroy()
        dt_widgets[1:]=[]
        dt_status_label.config(text='[Decision Tree]District Not Found!!!.')
        
def askfile_dt(event):
    global dt_dn;global dt_sn
    global dt_inpt_lf
    global dt_district_input
    global dt_widgets
    global district_label_inpt
    global dt_filename
    global dt_label
    dt_status_label.config(text='[Decision Tree]selecting file...')
    dt_filename=fd.askopenfilename(
            initialdir='.',
            filetypes=(('CSV file','*.csv'),),
            title='select a file')
    if dt_filename:
        if dt_widgets:
            for wid in dt_widgets:
                wid.destroy()
            dt_widgets=[]
        if isinstance(dt_inpt_lf,(tk.LabelFrame)) :
            dt_inpt_lf.destroy()
        dt_status_label.config(text='[Decision Tree]file selected.')
        dt_dn,dt_sn=get_knowns(open('../crop.csv','r'))
        #form_labrl_frame
        dt_inpt_lf=tk.LabelFrame(frame_dt,text='I/O',font=('Courier 17 bold'))
        dt_inpt_lf.pack(fill='x')
        #dt_label
        dt_label=tk.Label(dt_inpt_lf)
        dt_label.pack(fill='x')
        #districti_label_inpt_lf
        district_label_inpt=tk.Label(dt_label)
        district_label_inpt.pack(fill='x')
        #distritc_label_lf
        district_label=tk.Label(district_label_inpt,text='Enter district:',font=('Courier 12 bold'))
        district_label.pack(side='left')
        #district_label_lf
        dt_district_input=tk.Entry(district_label_inpt,font=('Courier 12 bold'))
        dt_district_input.pack(side='right')
        dt_district_input.focus()
        dt_district_input.bind('<Return>',append_season)
        dt_district_input.bind('<KeyRelease>',append_season)
        dt_widgets.append(district_label_inpt)
        
        

def dup_call_getbestcrop(event):
    call_getbestcrop()
def askfile(event):
    global district_entry
    global widgets
    global known_district_listbox
    global season
    global res_widget
    global inpt_lf
    #status change
    status_label.config(text='[Naive Approach]selecting file...')
    root.filename=fd.askopenfile(
            filetypes=(('CSV  file','*.csv'),),
            title='select a file')
    if root.filename:
        status_label.config(text='[Naive Approach]file selected.')
        dn,sn=get_knowns(root.filename)
        if widgets:
            for widget in widgets:
                widget.destroy()
            widgets=[]
        if res_widget:
            for e in res_widget:
                e.destroy()
            res_widget=[]
        #--->inpt_lf <root->child4> labelframe
        inpt_lf=tk.LabelFrame(frame_naive,text='[I/O]',font=('Courier 17 bold'))
        inpt_lf.pack(fill='x')
        #-->known_season_lf <inpt_lf->child1> labelframe
        known_season_lf=tk.LabelFrame(inpt_lf,text='[Known Seasons]',font=('Courier 15 bold'))
        known_season_lf.pack(side='top',fill='x')
        #->known_season_radiobutton
        season=tk.StringVar()
        for s in sorted(list(sn)):
            s=tk.Radiobutton(known_season_lf,variable=season,value=s.lower().strip(),text=s.lower().strip(),font=('Courier 12 bold'),command=call_getbestcrop,fg='lawngreen',bg='black')
            s.pack(fill='x',side='left')
        #-->known_district_lf <inpt_lf>child2> labelframe
        known_district_lf=tk.LabelFrame(inpt_lf,text='[Known Disricts]',font=('Courier 15 bold'))
        known_district_lf.pack(side='left')
        #->district_sb <known_district_lf->child1> scrollbar
        district_sb=tk.Scrollbar(known_district_lf)
        district_sb.pack(side='right',fill='y')
        #->known_district_listbox <known_district_lf->child2> listbox
        known_district_listbox=tk.Listbox(known_district_lf,yscrollcommand=district_sb.set,font=('Courier 12 bold'),fg='lawngreen',bg='black')
        known_district_listbox.pack(side='left',fill='y')
        district_sb.config(command=known_district_listbox.yview)
        for d in sorted(list(dn)):
            known_district_listbox.insert('end',d)
        #bind event to listbox
        known_district_listbox.bind('<<ListboxSelect>>',dup_call_getbestcrop)
        #append it in widgets
        #append it in widgets
        widgets.append(inpt_lf)
def askquit():
    if askyesno('crop advisor','Really want to Quit???'):
        root.destroy()
def show_about():
    try:
        showinfo('About crop advisor','Crop Advisor suggests crops for given input district\nDeveloped by Omkar Gavhane ')
    except Exception:
        pass
def show_algo():
    try:
        showinfo('Algorithm',algorithm)
    except Exception:
        pass
#root window
root=tk.Tk()
root.resizable(0,0)
#Notebook
nb=Notebook(root)
frame_naive=Frame(nb)
frame_dt=Frame(nb)
#top_menu
top_menu=tk.Menu(root)
root.config(menu=top_menu)
#algorithm 
#algo_menu=tk.Menu(top_menu)
top_menu.add_command(label='Algorithm',command=show_algo,underline=0)
#about menu
help_menu=tk.Menu(top_menu)
top_menu.add_cascade(label='Info',menu=help_menu,underline=0)
#option in about menu 
help_menu.add_command(label='About',command=show_about,underline=0)
help_menu.add_command(label='Exit',command=askquit,underline=0)
#set title
root.title('crop advisor')
#bind window delete protocol
root.protocol('WM_DELETE_WINDOW',askquit)
#image read
img=tk.PhotoImage(file='ca_1.png')
root.tk.call('wm','iconphoto',root._w,img)
#label for iamge 
label_img=tk.Label(frame_naive,image=img,text='CROP ADVISOR',compound='bottom',font=('Courier 25 bold'),fg='lawngreen',bg='black')
label_img.pack(side='top',fill='x')
#button for file slection
but=tk.Button(frame_naive,text='Select File',font=('Courier 15 bold'))
but.pack(fill='x')
but.bind('<ButtonRelease>',askfile)
#status 
status_lf=tk.LabelFrame(frame_naive,text='[Status]',fg='lawngreen',font=('Courier 15 bold'),bg='black')
status_lf.pack(side='bottom',fill='x')
#
label_img=tk.Label(frame_dt,image=img,text='CROP ADVISOR',compound='bottom',font=('Courier 25 bold'),fg='lawngreen',bg='black')
label_img.pack(side='top',fill='x')
#status_label <status->child1> label
status_label=tk.Label(status_lf,text='[Naive approach]Crop advisor started...',font=('Courier 12'),fg='goldenrod1',bg='black')
status_label.pack(side='left')
#add items to notebook
nb.add(frame_naive,text='Naive Approach')
nb.add(frame_dt,text='DecisionTree')
#pack nb to root
nb.pack()
#button for filw selection
dt_but=tk.Button(frame_dt,text='Select File',font=('Courier 15 bold'))
dt_but.pack(fill='x')
dt_but.bind('<ButtonRelease>',askfile_dt)
#dt_status
dt_status_lf=tk.LabelFrame(frame_dt,text='[Status]',fg='lawngreen',font=('Courier 15 bold'),bg='black')
dt_status_lf.pack(side='bottom',fill='x')
#label for status
dt_status_label=tk.Label(dt_status_lf,text='[Decision tree]Crop advisor started...',font=('Courier 12'),fg='goldenrod1',bg='black')
dt_status_label.pack(side='left')
root.mainloop()

