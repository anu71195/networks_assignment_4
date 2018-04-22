import matplotlib.pyplot as plt
x=[]
x_row=[45.2497,45.1393,45.1304]
x.append(x_row)
x_row=[40.1029,40.1629,40.1624]
x.append(x_row)

x_row=[39.0251,39.1562,39.0258]
x.append(x_row)

x_row=[41.8596,41.2564,41.2368]
x.append(x_row)


y=[0,256,512,1000]
print(x,y)
plt.plot([0,0,0],x[0],'ro')
plt.plot([256,256,256],x[1],'ro')
plt.plot([512,512,512],x[2],'ro')
plt.plot([1000,1000,1000],x[3],'ro')
plt.xlabel("threshold(MB)")
plt.ylabel("Bandwidth lost due to collisions)")
plt.title("Bandwidth lost due to collisions vs threshold")
x_row=[]
x_row.append(sum(x[0])/3)
x_row.append(sum(x[1])/3)
x_row.append(sum(x[2])/3)
x_row.append(sum(x[3])/3)
plt.plot(y,x_row)
# plt.axes([0,0,1000,1])

plt.show();


