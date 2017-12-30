import time
import re
import numpy as np
import pandas as pd



# this function handles the forecast of each number based on the direction
# the method is not important, no forecast methoed will perform good
def GenerateForecastedNumbers(ResultTable):

    # clear 0 directions

    ForecastedDirections=GetForecastedDirections(ResultTable)
    directions=[1,-1]

    for i in ForecastedDirections.keys():
        if ForecastedDirections[i]==0:
            ForecastedDirections[i]=directions[np.random.randint(0,2)]

    ForecastedNumbers={}

    i=1

    while(i!=7):

        tag="number"+str(i)

        if ForecastedDirections[tag]==-1:
            if i==1:
                ForecastedNumbers[tag]=np.random.randint(1,ResultTable.ix[0,tag]) if ResultTable.ix[0,tag]!=1 else 1
            else:
                tagpre="number"+str(i-1)
                ForecastedNumbers[tag]=np.random.randint(ForecastedNumbers[tagpre]+1,ResultTable.ix[0,tag]+1)
            i=i+1


        if ForecastedDirections[tag]==1:
            if i==6:
                ForecastedNumbers[tag]=np.random.randint(ResultTable.ix[0,tag],50)
                i=i+1

            else:
                j=-1
                for j in range(i+1,7):
                    if ForecastedDirections[("number"+str(j))]==-1:
                        break

                if j!=7:
                    for k in range(i,j+1):
                        if k!=j:
                            if k==i:
                                pre=0
                            else:
                                pre=ForecastedNumbers[("number"+str(k-1))]+1
                            ForecastedNumbers[("number"+str(k))]=np.random.randint(max(pre,ResultTable.ix[0,("number"+str(k))]),ResultTable.ix[0,("number"+str(j))]-(j-k-1))
                        
                        else:
                            pre=ForecastedNumbers[("number"+str(k-1))]+1
                            ForecastedNumbers[("number"+str(k))]=np.random.randint(pre,ResultTable.ix[0,("number"+str(j))]-(j-k-1))
                    i=j+1

                else:
                    for k in range(i,j):
                        if k==i:
                            pre=0
                        else:
                            pre=ForecastedNumbers[("number"+str(k-1))]+1
                        ForecastedNumbers[("number"+str(k))]=np.random.randint(max(pre,ResultTable.ix[0,("number"+str(k))]),49-(6-k-1))
                    i=7    

    return ForecastedNumbers





# this function will trace the historical data to check for each number
# the forecasted number is bigger or smaller
def GetForecastedDirections(ResultTable, length=5):

    ForecastedDirections={}
    
    for i in range(1,7):
        colname='number' + str(i)

        ToCompare=ResultTable.loc[:length,colname]
        CorrelationList=ResultTable.loc[:,colname].rolling(center=False, 
                                         window = len(ToCompare)).apply(lambda x: np.corrcoef(ToCompare,x)[0,1])

        pos=np.where(CorrelationList==max(CorrelationList[len(ToCompare):]))[0]
        pickedPos=pos[pos!=len(ToCompare)-1][0]

        if ResultTable.loc[pickedPos-len(ToCompare),colname]>ResultTable.ix[pickedPos-len(ToCompare)+1,colname]:
            ForecastedDirection=1
        elif ResultTable.loc[pickedPos-len(ToCompare),colname]<ResultTable.ix[pickedPos-len(ToCompare)+1,colname]:
            ForecastedDirection=-1
        else:
            ForecastedDirection=0

        ForecastedDirections[colname]=ForecastedDirection

    return ForecastedDirections









