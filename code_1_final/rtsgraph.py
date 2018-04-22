import matplotlib.pyplot as plt
x=[]
x_row=[0.867795410156	,0.866641693115,0.86773651123]
x.append(x_row)
x_row=[0.697254638672	,0.694607696533,0.695234985352]
x.append(x_row)

x_row=[0.698653106689		,0.695790405273,0.695767364502]
x.append(x_row)

x_row=[0.655659179687,0.653371276855,0.653222198486]
x.append(x_row)


y=[0,256,512,1000]
print(x,y)
plt.plot([0,0,0],x[0],'ro')
plt.plot([256,256,256],x[1],'ro')
plt.plot([512,512,512],x[2],'ro')
plt.plot([1000,1000,1000],x[3],'ro')
plt.xlabel("threshold(MB)")
plt.ylabel("rts bandwidth (MBps)")
plt.title("Average bandwidth spent in transmitting RTS VS RTS threshold")
x_row=[]
x_row.append(sum(x[0])/3)
x_row.append(sum(x[1])/3)
x_row.append(sum(x[2])/3)
x_row.append(sum(x[3])/3)
plt.plot(y,x_row)
# plt.axes([0,0,1000,1])

plt.show();


