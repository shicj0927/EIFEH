########################################
#                EIFEH                 #
#                V 1.0                 #
#    EIFEH Is For English Homework     #
########################################

from cnocr import CnOcr
from turtle import*
import cv2
#goto(0,0)
#ht()
#speed(10)


#############################################################################################################
#                                                 内核部分开始                                              #
#############################################################################################################


def draw(a,b,c,d):
	A=a,B=b,C=c,D=d
	A[1]=-A[1]
	B[1]=-B[1]
	C[1]=-C[1]
	D[1]=-D[1]
	pu()
	goto(A[0]/10-100,A[1]/10+100)
	pd()
	xx=(A[0]+B[0]+C[0]+D[0])/40-100
	yy=(A[1]+B[1]+C[1]+D[1])/40+100
	goto(B[0]/10-100,B[1]/10+100)
	goto(C[0]/10-100,C[1]/10+100)
	goto(D[0]/10-100,D[1]/10+100)
	goto(A[0]/10-100,A[1]/10+100)
	pu()
	goto(xx-5,yy-5)
	pd()
	goto(xx+5,yy+5)
	pu()
	goto(xx-5,yy+5)
	pd()
	goto(xx+5,yy-5)
	pu()
def check_black(img,A,B,C,D):
	_cvimg=cv2.imread(img,cv2.IMREAD_GRAYSCALE)
	ret,cvimg=cv2.threshold(_cvimg,100,255,cv2.THRESH_BINARY)
	showimg=cv2.resize(cvimg,dsize=None,fx=0.2,fy=0.2,interpolation=cv2.INTER_LINEAR)
#	cv2.imshow("img",showimg)
	cv2.waitKey(0)
	mxx=int(min(B[0],C[0]))
	mnx=int(max(A[0],D[0]))
	mxy=int(min(C[1],D[1]))
	mny=int(max(A[1],B[1]))
	tot=0
	ss=0
#	print(mnx,mxx,mny,mxy)
	for i in range(mnx,mxx):
		for j in range(mny,mxy):
			ss+=cvimg[j][i]
			tot+=1
	if tot==0:
		return False
	val=ss/tot
#	print(val)
	if(val<=120):
		return True
	else:
		return False
def is_cycz(txt):
	if txt=="常用词组":return True
	if "常" in txt:return True
	if "用" in txt:return True
	if "组" in txt:return True
	return False
def is_cxbh(txt):
	if txt=="词形变换":return True
	if "形" in txt:return True
	if "变" in txt:return True
	if "换" in txt:return True
	return False
def is_zdjx(txt):
	if txt=="重点句型":return True
	if "重" in txt:return True
	if "点" in txt:return True
	if "句" in txt:return True
	if "型" in txt:return True
	return False
def is_cjsd(txt):
	if txt=="晨间诵读":return True
	if "晨" in txt:return True
#	if "间" in txt:return True
#	间 会与 词 混淆
	if "诵" in txt:return True
	if "读" in txt:return True
	return False

def is_eng(i):
	eng="QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
	if i in eng:
		return True
	return False

def is_opt(i):
	opt="`~!@#$%^&*()_+-=[]{}|\\;:\"\'<>,.?/《》，。？、“”‘’：；【】！ "
	if i in opt:
		return True
	return False

def is_num(i):
	num="1234567890"
	if i in num:
		return True
	return False

def is_chi(i):
	if is_eng(i) or is_opt(i) or is_num(i):
		return False
	return True

def del_opt(txt):
	opt_s="。？！.?!…)）"
	txta=[]
	for i in txt:
		txta.append(i)
	i=len(txta)-1
	while is_opt(txta[i]) or is_num(txta[i]):
		i-=1
	if i+1<len(txta) and txta[i+1] in opt_s:
		i+=1
	ss=""
	for j in range(0,i+1):
		ss+=txta[j]
	return ss

def get_chi(txt):
	ans=[]
	tmp=""
	txta=[]
	for i in txt:
		txta.append(i)
#	print(txta)
	for i in range(len(txta)):
		if is_chi(txta[i]):
			tmp+=txta[i]
#			print(tmp)
		elif is_opt(txta[i]) and is_opt(txta[i-1]):
			if tmp!="":
#				ans+=del_opt(tmp)
#				ans+="\n"
				ans.append(del_opt(tmp))
				tmp=""
		elif i<len(txta)-1 and len(tmp)>0 and is_chi(tmp[len(tmp)-1]) and is_chi(txta[i+1]):
			tmp+=txta[i]
		elif i<len(txta)-2 and len(tmp)>1 and (is_chi(tmp[len(tmp)-1]) or is_chi(tmp[len(tmp)-2])) and (is_chi(txta[i+1]) or is_chi(txta[i+2])):
			tmp+=txta[i]
		elif ((is_num(txta[i]) and (len(tmp)!=0 and not is_opt(tmp[len(tmp)-1]))) or is_opt(txta[i])) and len(tmp)!=0 and tmp[len(tmp)-1]==txta[i-1]:
			tmp+=txta[i]
		elif tmp!="":
#			ans+=del_opt(tmp)
#			ans+="\n"
			ans.append(del_opt(tmp))	
			tmp=""
	if tmp!="":
#		ans+=del_opt(tmp)
#		ans+="\n"
		ans.append(del_opt(tmp))
#	print("GC",ans)
	return ans

all_ans=[]

def add_data(op,txt):
	global all_ans
	chi=get_chi(txt)
	if op=="常用词组":
		for i in chi:
			all_ans[len(all_ans)-1][0].append(i)
	elif op=="重点句型":
		for i in chi:
			all_ans[len(all_ans)-1][1].append(i)

def is_title(pos):
	xx=(pos[0][0]+pos[1][0]+pos[2][0]+pos[3][0])/4
	if xx>=1200 and xx<=1800:
		return True
	return False
def ocr_file(img):
	ocr=CnOcr()
	out=ocr.ocr(img)
	pos=[]
	cen=[]
	for i in out:
		pos.append(i["position"])
#	print(pos)
#	for i in pos:
#		draw(i[0],i[1],i[2],i[3])
	tags=[]
	for i in range(len(pos)):
		if check_black(img,pos[i][0],pos[i][1],pos[i][2],pos[i][3]):
			tags.append(i)
	tags_text=[]
	for i in tags:
		print("black tag:",i,out[i]["text"])
		if is_cycz(out[i]["text"]):
#			print("!常用词组!")
			out[i]["text"]="常用词组"
		if is_cxbh(out[i]["text"]):
#			print("!词形变换!")
			out[i]["text"]="词形变换"
		if is_zdjx(out[i]["text"]):
#			print("!重点句型!")
			out[i]["text"]="重点句型"
		if is_cjsd(out[i]["text"]):
#			print("!晨间诵读!")
			out[i]["text"]="晨间诵读"
	if is_title(pos[1]):
		#第一页
		all_ans.append([[],[],[]])
#		print("第一页")
		if len(tags)==1:
			tags.append(len(pos))
		left=[]
		right=[]
		for j in range(tags[0]+1,tags[1]):
			i=pos[j]
			tmp=[]
			tmp.append((i[0][0]+i[1][0]+i[2][0]+i[3][0])/4)
			tmp.append((i[0][1]+i[1][1]+i[2][1]+i[3][1])/4)
			if(tmp[0]<=1500):
				left.append(out[j])
			else:
				right.append(out[j])
		leftt=[]
		rightt=[]
		for i in left:
			leftt.append(i["text"])
		for i in right:
			rightt.append(i["text"])
#		print("left:",leftt)
#		print("right:",rightt)
		txt=""
		for i in leftt:txt+=i
		for i in rightt:txt+=i
#		print("常用词组",txt)
		add_data("常用词组",txt)
		if tags[1]!=len(pos):
			left=[]
			right=[]
			for j in range(tags[0]+1,tags[1]):
				i=pos[j]
				tmp=[]
				tmp.append((i[0][0]+i[1][0]+i[2][0]+i[3][0])/4)
				tmp.append((i[0][1]+i[1][1]+i[2][1]+i[3][1])/4)
				if(tmp[0]<=1500):
					left.append(out[j])
				else:
					right.append(out[j])
			leftt=[]
			rightt=[]
			for i in left:
				leftt.append(i["text"])
			for i in right:
				rightt.append(i["text"])
#			print("left:",leftt)
#			print("right:",rightt)
			txt=""
			for i in leftt:txt+=i
			for i in rightt:txt+=i
#			print("词形变换",txt)
			add_data("词形变换",txt)
	else:
		#第二/三页
#		print("第二/三页")
		if out[tags[0]]["text"]=="词形变换":
			if tags[0]!=0:
				#这一页开头是半截常用词组
				if len(tags)==1:
					tags.append(len(pos)-1)
				left=[]
				right=[]
				for j in range(tags[0]+1,tags[1]):
					i=pos[j]
					tmp=[]
					tmp.append((i[0][0]+i[1][0]+i[2][0]+i[3][0])/4)
					tmp.append((i[0][1]+i[1][1]+i[2][1]+i[3][1])/4)
					if(tmp[0]<=1500):
						left.append(out[j])
					else:
						right.append(out[j])
				leftt=[]
				rightt=[]
				for i in left:
					leftt.append(i["text"])
				for i in right:
					rightt.append(i["text"])
#				print("left:",leftt)
#				print("right:",rightt)
				txt=""
				for i in leftt:txt+=i
				for i in rightt:txt+=i
#				print("半截常用词组",txt)
				add_data("常用词组",txt)
			#剩下的词形变换
			if len(tags)==1:
				tags.append(len(pos)-1)
			left=[]
			right=[]
			for j in range(tags[0]+1,tags[1]):
				i=pos[j]
				tmp=[]
				tmp.append((i[0][0]+i[1][0]+i[2][0]+i[3][0])/4)
				tmp.append((i[0][1]+i[1][1]+i[2][1]+i[3][1])/4)
				if(tmp[0]<=1500):
					left.append(out[j])
				else:
					right.append(out[j])
			leftt=[]
			rightt=[]
			for i in left:
				leftt.append(i["text"])
			for i in right:
				rightt.append(i["text"])
#			print("left:",leftt)
#			print("right:",rightt)
			txt=""
			for i in leftt:txt+=i
			for i in rightt:txt+=i
#			print("词形变换",txt)
			add_data("词形变换",txt)
		if out[tags[0]]["text"]=="重点句型":
			if tags[0]!=0:
				#这一页开头是半截词形变换
				left=[]
				right=[]
				for j in range(0,tags[0]):
					i=pos[j]
					tmp=[]
					tmp.append((i[0][0]+i[1][0]+i[2][0]+i[3][0])/4)
					tmp.append((i[0][1]+i[1][1]+i[2][1]+i[3][1])/4)
					if(tmp[0]<=1500):
						left.append(out[j])
					else:
						right.append(out[j])
				leftt=[]
				rightt=[]
				for i in left:
					leftt.append(i["text"])
				for i in right:
					rightt.append(i["text"])
#				print("left:",leftt)
#				print("right:",rightt)
				txt=""
				for i in leftt:txt+=i
				for i in rightt:txt+=i
#				print("词形变换",txt)
				add_data("词形变换",txt)
			#剩下的重点句型
			if len(tags)==1:
				tags.append(len(out)-1)
			dat=[]
			for j in range(tags[0]+1,tags[1]):
				dat.append(out[j])
			datt=[]
			for i in dat:
				datt.append(i["text"])
#			print("dat:",datt)
			txt=""
			for i in datt:txt+=i
#			print("重点句型",txt)
			add_data("重点句型",txt)
		if out[tags[0]]["text"]=="晨间诵读":
			#这一页开头是半截重点句型
			dat=[]
			for j in range(0,tags[0]):
				dat.append(out[j])
			datt=[]
			for i in dat:
				datt.append(i["text"])
#			print("dat:",datt)
			txt=""
			for i in datt:txt+=i
#			print("重点句型",txt)
			add_data("重点句型",txt)
		if len(tags)>=2 and out[tags[1]]["text"]=="重点句型":
			#第二块是重点句型
			if len(tags)==2:
				tags.append(len(out)-1)
			dat=[]
			for j in range(tags[1]+1,tags[2]):
				dat.append(out[j])
			datt=[]
			for i in dat:
				datt.append(i["text"])
#			print("dat:",datt)
			txt=""
			for i in datt:txt+=i
#			print("重点句型",txt)
			add_data("重点句型",txt)

#ocr_file("01.jpg")
#ocr_file("02.jpg")

#print()
#print()
#print("----------最终结果----------")
#print("常用词组")
#print(all_ans[0])
#print("重点句型")
#print(all_ans[1])

#文件导出

def mk_html_cycz(x):
	head="""<!DOCTYPE html>
	<html>
	<head> 
	<meta charset="utf-8"> 
	<title>英语默写</title> 
	</head>
	<body>
	<div id="header" >
	<h2 style="margin-bottom:0;">常用词组</h1></div>
	\n"""
	foot="""
	<div id="footer" style="clear:both;text-align:center;"><hr>
	created by EIFEH V1.0</div>
	</div>
	</body>
	</html>\n"""
	div1="""<div id="1" style="float:left;width:50%;">\n"""
	div2="""<div id="2" style="width:50%; float:right;">\n"""
	line="""<p>______________________________________________</p>\n"""
	div1_c=""
	div2_c=""
	dv=len(all_ans[x][0])
	dv=int(dv)
	for i in range(dv):
		if i%2==0:
			div1_c+="<p>"+str(i+1)+". "+all_ans[x][0][i]+"</p>\n"
			div1_c+=line
		else:
			div2_c+="<p>"+str(i+1)+". "+all_ans[x][0][i]+"</p>\n"
			div2_c+=line
	div1_c+="</div>\n"
	div2_c+="</div>\n"
	html=head+div1+div1_c+div2+div2_c+foot
	return html

def mk_html_zdjx(x):
	head="""<!DOCTYPE html>
	<html>
	<head> 
	<meta charset="utf-8"> 
	<title>英语默写</title> 
	</head>
	<body>
	<div id="header" >
	<h2 style="margin-bottom:0;">重点句型</h1></div>
	\n"""
	foot="""
	<div id="footer" style="clear:both;text-align:center;"><hr>
	created by EIFEH V1.0</div>
	</div>
	</body>
	</html>\n"""
	line="""<p>__________________________________________________________________________________________</p>\n"""
	c=""
	for i in range(len(all_ans[x][1])):
		c+="<p>"+str(i+1)+". "+all_ans[x][1][i]+"<p>\n"
		c+=line
	html=head+c+foot
	return html

def wt_html(x):
	print("[WRITE]",x)
	file=str(x+1)
	cycz=file+"_常用词组.html"
	zdjx=file+"_重点句型.html"
	with open(cycz,'w',encoding="utf-8") as f:
		f.write(mk_html_cycz(x))
	with open(zdjx,'w',encoding="utf-8") as f:
		f.write(mk_html_zdjx(x))

#ocr_file("01.jpg")
#ocr_file("02.jpg")
#print(all_ans)
#wt_html(0)


#############################################################################################################
#                                                 GUI部分开始                                               #
#############################################################################################################


from tkinter import*
from tkinter import ttk
from tkinter.messagebox import *
import webbrowser 
root=Tk()
root.title("EIFEH V1.0")
root.resizable(0,0)
f_title=Frame(root)
f_main=Frame(root)
f_foot=Frame(root)
f_main_input=Frame(f_main)
f_main_check=Frame(f_main)
f_main_check_l=Frame(f_main_check)
f_main_check_r=Frame(f_main_check)
Label(f_title,font=("TkDefaultFont",50),text="EIFEH").pack()
Label(f_title,font=("TkDefaultFont",20),text="  EIFEH IS FOR ENGLISH HOMEWORK  ").pack()
f_title.pack()
Label(f_main_input,text="输入图片：从 1.").pack(side=LEFT)
E_t=Entry(f_main_input,width=4)
E_t.pack(side=LEFT)
Label(f_main_input,text="(jpg/png) 到").pack(side=LEFT)
E_n=Entry(f_main_input,width=4)
E_n.pack(side=LEFT)
Label(f_main_input,text="(无需类型后缀)").pack(side=LEFT)
f_main_input.pack()
typ=""
num=""
def get_input():
	global typ,num
	typ=str(E_t.get())
	num=str(E_n.get())
	if typ!="png" and typ!="jpg":
		print("[ERROR] type error")
		typ=num=""
		return False
	num_all="1234567890"
	if len(num)==0:
		print("[ERROR] empty num")
		typ=num=""
		return False
	for i in num:
		if not(i in num_all):
			print("[ERROR] num error")
			typ=num=""
			return False
	return True
OK=False
now=0
def get_str(x,y):
	s=""
	for i in all_ans[x][y]:
		s+=i+"\n"
	return s
def str_to_list(txt):
	ans=[]
	for i in txt.splitlines():
		if i!="":
			ans.append(i)
	print("[TXT]",ans)
	return ans
P1=ttk.Progressbar(f_main)
T1=Text(f_main_check_l,width=50)
T2=Text(f_main_check_r,width=50)
P2=ttk.Progressbar(f_main)
def load_text(x):
	print("[LOAD]",x)
	T1.delete(1.0,"end")
	T2.delete(1.0,"end")
	T1.insert("end",get_str(x,0))
	T2.insert("end",get_str(x,1))
def submit_text(x):
	all_ans[x][0]=[]
	all_ans[x][1]=[]
	txt0=str(T1.get(1.0,"end"))
	txt1=str(T2.get(1.0,"end"))
	print("[SUBMIT]",x)
	all_ans[x][0]=str_to_list(txt0)
	all_ans[x][1]=str_to_list(txt1)
	wt_html(x)
def nxt_check():
	global OK,now
	if OK==False:
		print("[ERROR]","not OK")
		return
	if now>len(all_ans)-1:
		print("[ERROR]","is finished")
		OK=False
		now=0
		return
	submit_text(now)
	P2['value']=int(100/len(all_ans)*(now+1))
	now=now+1
	T1.delete(1.0,"end")
	T2.delete(1.0,"end")
	if now<=len(all_ans)-1:
		load_text(now)
B_nxt=Button(f_main,text="下一单元",command=nxt_check)
def start_ocr():
	global OK,now,all_ans
	OK=False
	val=get_input()
	global num,typ
	print("[START]",val,num,typ)
	if val==False:
		showerror('错误', '不合法的输入')
		return
	else:
#		print("[INPUT]",typ,num)
		num=int(num)
		P1['value']=0
		P2['value']=0
		root.update()
		all_ans=[]
		for i in range(1,num+1):
			file=str(i)+"."+typ
			print("[OCR]",file)
			ocr_file(file)
			P1['value']=int(100/num*i)
			root.update()
			print("[OK]")
	load_text(0)
	OK=True
	now=0
Button(f_main,text="开始识别",command=start_ocr).pack(fill=X)
P1.pack(fill=X)
Label(f_main_check_l,text="常用词组").pack()
T1.pack()
Label(f_main_check_r,text="重点句型").pack()
T2.pack()
f_main_check_l.pack(side=LEFT,fill=X)
f_main_check_r.pack(side=RIGHT,fill=X)
f_main_check.pack(fill=X)
B_nxt.pack(fill=X)
P2.pack(fill=X)
f_main.pack(fill=X)
def open_project():
	webbrowser.open("https://github.com/shicj0927/EIFEH",new=0)
Label(f_foot,text="EIFEH V1.0 by shicj").pack(side=LEFT)
Button(f_foot,text="P\u0332r\u0332o\u0332j\u0332e\u0332c\u0332t\u0332 \u0332L\u0332i\u0332n\u0332k\u0332",
	command=open_project,fg="blue",relief=FLAT,padx=0,pady=0).pack(side=LEFT)
f_foot.pack()
root.mainloop()
