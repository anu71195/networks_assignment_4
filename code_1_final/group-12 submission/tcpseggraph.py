import matplotlib.pyplot as plt
x=[]
x_row=[7.56315887451	,7.55657485962,7.55742294312]
x.append(x_row)
x_row=[9.75382919312	,9.73553604126,9.73612030029]
x.append(x_row)

x_row=[9.78686141968		,9.77068756104,9.77059692383]
x.append(x_row)

x_row=[8.70769073486,8.69438690186,8.69461914063]
x.append(x_row)


y=[0,256,512,1000]
print(x,y)
plt.plot([0,0,0],x[0],'ro')
plt.plot([256,256,256],x[1],'ro')
plt.plot([512,512,512],x[2],'ro')
plt.plot([1000,1000,1000],x[3],'ro')
plt.xlabel("threshold(MB)")
plt.ylabel("tcp-seg bandwidth (MBps)")
plt.title("Average bandwidth spent in transmitting tcp-seg VS RTS threshold")
x_row=[]
x_row.append(sum(x[0])/3)
x_row.append(sum(x[1])/3)
x_row.append(sum(x[2])/3)
x_row.append(sum(x[3])/3)
plt.plot(y,x_row)
# plt.axes([0,0,1000,1])

plt.show();


