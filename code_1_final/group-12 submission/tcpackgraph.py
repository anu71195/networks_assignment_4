import matplotlib.pyplot as plt
x=[]
x_row=[3.77447250366	,3.77119110107,3.77154373169]
x.append(x_row)
x_row=[4.86895828247	,4.8595324707,4.85975341797]
x.append(x_row)

x_row=[4.88491912842		,4.87717178345,4.87712478638]
x.append(x_row)

x_row=[4.34563613892,4.33887145996,4.33895172119]
x.append(x_row)


y=[0,256,512,1000]
print(x,y)
plt.plot([0,0,0],x[0],'ro')
plt.plot([256,256,256],x[1],'ro')
plt.plot([512,512,512],x[2],'ro')
plt.plot([1000,1000,1000],x[3],'ro')
plt.xlabel("threshold(MB)")
plt.ylabel("tcp-ack bandwidth (MBps)")
plt.title("Average bandwidth spent in transmitting tcp-ack VS RTS threshold")
x_row=[]
x_row.append(sum(x[0])/3)
x_row.append(sum(x[1])/3)
x_row.append(sum(x[2])/3)
x_row.append(sum(x[3])/3)
plt.plot(y,x_row)
# plt.axes([0,0,1000,1])

plt.show();


