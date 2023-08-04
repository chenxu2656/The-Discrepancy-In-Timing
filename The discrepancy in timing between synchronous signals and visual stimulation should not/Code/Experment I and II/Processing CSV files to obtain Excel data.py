import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal,stats
%matplotlib

###################获取数据###############################
Analog = pd.read_csv(r'C:\Users\user\Desktop\1-1.csv') .astype("float32")#获取波形数据
Digital = pd.read_csv(r'C:\Users\user\Desktop\1-2.csv') .astype("float32")#获取波形数据

Analog_Time = Analog.iloc[:,0]#读出模拟数据时间列
Analog_Data = Analog.iloc[:,1]#读出模拟数据列

Digital_Time = Digital.iloc[:,0]#读出数字数据时间列
Digital_Data = Digital.iloc[:,1]#读出数字数据列

###################需要改变的参数###############################
fs = 781250    #设定模拟信号采样率，fs>5fh；和saleae logic模拟通道的采样频率一致
plus = 0.008  #设定数字信号阈值，等于数字信号半周期

###################数字处理###############################
threshold = 0
dig_time_stemp = []#最终选出的数字信号第一个下降沿时间戳
while 1:
    #筛选下降沿
    Digital_Down = Digital[(Digital_Data == 0.0) & (Digital_Time>= threshold)]['Time[s]']
    if(len(Digital_Down) == 0):
        break
    dig_time_stemp.append(Digital_Down.iloc[0])#保存符合要求的下降沿时间戳
    threshold = Digital_Down.iloc[0]+plus#选取下一个时间片

####################模拟处理################################
#使用6阶巴特沃斯低通滤波器对波形进行滤波
fh = 3500     #低通滤波器的截止频率
b,a = signal.butter(6, fh, 'lowpass',fs=fs)
Analog_Data_flt = signal.filtfilt(b,a,Analog_Data)

#依据图形选取阈值
threshold_Analog = Analog_Data_flt.max()/2.0

#计算上升沿，过阈值的点。
crosses_up = np.where(np.diff(np.sign(Analog_Data_flt - threshold_Analog)) > 1)[0]
#计算下降沿，过阈值的点。
crosses_down = np.where(np.diff(np.sign(Analog_Data_flt - threshold_Analog)) < -1)[0]

time_up = crosses_up/fs#计算时间戳
time_down = crosses_down/fs#计算时间戳

####################输出时间戳###############################
if(0):
    time_up=pd.DataFrame(time_up)#转换成DataFrame格式
    time_down=pd.DataFrame(time_down)#转换成DataFrame格式
    dig_time_stemp=pd.DataFrame(dig_time_stemp)#转换成DataFrame格式
    path = pd.ExcelWriter(r'D:\data2\3.xlsx',engine = 'xlsxwriter')#设置输出文件路径

    time_up.to_excel(path,sheet_name="模拟上升沿")
    time_down.to_excel(path,sheet_name="模拟下降沿")
    dig_time_stemp.to_excel(path,sheet_name="数字下降沿")
    path.save()#保存
else:
    #print(threshold_Analog)
    #plt.plot(Analog_Time,Analog_Data,'ro',Digital_Time,Digital_Data,'bs')
    #plt.plot(crosses_up,np.ones(crosses_up.shape[0])*threshold_Analog,'*')
    #plt.plot(crosses_down,np.ones(crosses_down.shape[0])*threshold_Analog,'*')
    #plt.show()
    
    plt.plot(time_up,np.ones(time_up.shape[0])*threshold_Analog,'*')#绘制波形，星号位置为过阈值位置
    plt.plot(time_down,np.ones(time_down.shape[0])*threshold_Analog,'*')
    plt.plot(dig_time_stemp,np.ones(len(dig_time_stemp))*threshold_Analog,marker='h')
    plt.show()
