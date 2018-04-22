import matplotlib.pyplot as plt
x=[]
x_row=[22.4635958672	,22.4641032219,22.4635400772]
x.append(x_row)
x_row=[28.8285822868	,28.8098802567,28.8098750114]
x.append(x_row)

x_row=[28.9274249077		,28.9117083549,28.9116473198]
x.append(x_row)

x_row=[25.7887988091,25.7775788307,25.7778429985]
x.append(x_row)


y=[0,256,512,1000]
print(x,y)
plt.plot([0,0,0],x[0],'ro')
plt.plot([256,256,256],x[1],'ro')
plt.plot([512,512,512],x[2],'ro')
plt.plot([1000,1000,1000],x[3],'ro')
plt.xlabel("threshold(MB)")
plt.ylabel("tcp-throughput bandwidth (MBps)")
plt.title("Average bandwidth spent in transmitting tcp-throughput VS RTS threshold")
x_row=[]
x_row.append(sum(x[0])/3)
x_row.append(sum(x[1])/3)
x_row.append(sum(x[2])/3)
x_row.append(sum(x[3])/3)
plt.plot(y,x_row)
# plt.axes([0,0,1000,1])

plt.show();


