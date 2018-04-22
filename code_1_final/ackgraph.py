import matplotlib.pyplot as plt
x=[]
x_row=[0.642498168945	,0.663664245605,0.664056091309]
x.append(x_row)
x_row=[0.714746856689	,0.739566650391,0.739766082764]
x.append(x_row)

x_row=[0.714945068359		,0.739964599609,0.739937744141]
x.append(x_row)

x_row=[0.671350708008,0.694751586914,0.69486328125]
x.append(x_row)


y=[0,256,512,1000]
print(x,y)
plt.plot([0,0,0],x[0],'ro')
plt.plot([256,256,256],x[1],'ro')
plt.plot([512,512,512],x[2],'ro')
plt.plot([1000,1000,1000],x[3],'ro')
plt.xlabel("threshold(MB)")
plt.ylabel("ack bandwidth (MBps)")
plt.title("Average bandwidth spent in transmitting ack VS RTS threshold")
x_row=[]
x_row.append(sum(x[0])/3)
x_row.append(sum(x[1])/3)
x_row.append(sum(x[2])/3)
x_row.append(sum(x[3])/3)
plt.plot(y,x_row)
# plt.axes([0,0,1000,1])

plt.show();


