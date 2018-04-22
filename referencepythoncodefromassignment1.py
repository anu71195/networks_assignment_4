import matplotlib.pyplot as plt
import numpy as np;

def partition(x,y,low,high):
	pivot=x[high];
	i=low;
	for j in range(low,high+1):
		if x[j]<pivot:
			x[i],x[j]=x[j],x[i]
			y[i],y[j]=y[j],y[i]
			i+=1;
	x[i],x[j]=x[j],x[i]
	y[i],y[j]=y[j],y[i]	
	return i;


def quick_sort(x,y,low,high):
	if(low<high):
		index=partition(x,y,low,high);
		quick_sort(x,y,low,index-1);
		quick_sort(x,y,index+1,high);







def plot_graph(time):
	dicti={};
	x=[];
	y=[];
	for i in time:
		dicti[i]=0;
	for i in time:
		dicti[i]+=1;
	for i in dicti:
		x.append(i);
		y.append(dicti[i]);
	# print(x)
	quick_sort(x,y,0,len(x)-1)
	# print(x)
	axes=[0,6,0,50];
	plt.plot(x,y);	
	plt.plot(x,y,'ro');
	plt.xlabel("round trip time (rtt) (in ms)");
	plt.ylabel("frequency of rtt");
	plt.title("1) ping -n 202.141.80.14")
	plt.axis(axes);
	plt.show();

def find_median(time):
	time.sort();
	length=len(time)/2;
	if(length*10%10):
		return ((time[int(length)]+time[int(length)+1])/2)
	return time[int(length)]


def file_operations(fp):
	text=(fp.read()).split('\n');
	time=[]
	for i in range(len(text)):
		text[i]=(text[i].split(" "))
		if (len(text[i])<2):
			continue;
		if(text[i][1]=='bytes'):
			time.append(float(( (text[i][6]).split('='))[1]))
		if(text[i][1]=='packets'):
			packets_sent=int(text[i][0]);
			packets_received=int(text[i][3])
			packets_loss=int((text[i][5].split('%'))[0])
			time_taken=int((text[i][9].split('ms'))[0])
	minimum=min(time);
	maximum=max(time);
	average=sum(time)/len(time);
	median=find_median(time)
	print("minimum\t=",minimum,"\nmaximum\t=",maximum,"\naverage\t=",average,"\nmedian\t=",median);
	plot_graph(time);
	print(median,average,minimum,maximum)



fp1=open("q3.1_2.txt","r");
fp2=open("q3.2_2.txt","r");

file_operations(fp1);

