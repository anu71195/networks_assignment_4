import matplotlib.pyplot as plt
x=[]
x_row=[0.677150268555	,0.697372436523,0.697825927734]
x.append(x_row)
x_row=[0.534067382812	,0.563737792969,0.563737792969]
x.append(x_row)

x_row=[0.535138549805		,0.564868469238,0.564868469238]
x.append(x_row)

x_row=[0.502201538086,0.530101623535,0.530101623535]
x.append(x_row)


y=[0,256,512,1000]
print(x,y)
plt.plot([0,0,0],x[0],'ro')
plt.plot([256,256,256],x[1],'ro')
plt.plot([512,512,512],x[2],'ro')
plt.plot([1000,1000,1000],x[3],'ro')
plt.xlabel("threshold (MB)")
plt.ylabel("cts bandwidth (MBps)" )
plt.title("Average bandwidth spent in transmitting CTS VS CTS threshold")
x_row=[]
x_row.append(sum(x[0])/3)
x_row.append(sum(x[1])/3)
x_row.append(sum(x[2])/3)
x_row.append(sum(x[3])/3)
plt.plot(y,x_row)
# plt.axes([0,0,1000,1])

plt.show();


