import FinanceDataReader as fdr
from datetime import datetime
from numpy import NaN

def getPeriod(crawlingYears=3):         # 주가데이터를 가져올 기간 설정 / 변수입력이 없으면 기본값 3년
    tDay = datetime.today().strftime('%Y-%m-%d')
    lDay = str(int(tDay.split('-', 1)[0])-crawlingYears)
    lDay = lDay + '-' + tDay.split('-', 1)[1]         # 작년 올해의 문자열을 구하는 계산식
    return lDay, tDay

def mAverageCalc(theDay, period):       # 이동평균선 계산
    if theDay+1 - period < 0:
#        print('theDay :', theDay, '- period :', period, ' =', theDay-period, 'Returning NaN')
#        print('')
        return NaN
    
#    print('df.iloc... is ', theDay-(period-1), ' : ', df.iloc[theDay-(period-1),3], 3)
    aggregate = df.iloc[theDay-(period-1):theDay+1, 3].sum()
#    print('aggregate is ', theDay, period, aggregate)
#    print('')
    average = aggregate / period

    return average

def algo0000():
    ret = 5
    for n in range(l+ret, sizeOfIndex):
        if df.iloc[n,8] < 0:
            if abs(df.iloc[n,8]) / abs(maxMinusDiff) < 0.1:
                p = 0
                for i in range(ret):
                    if df.iloc[n-i,8] > df.iloc[n-1-i,8]:
                        p += 1
                if p >= 3:
                    df.iloc[n, 10] = True
#                    print('The signal of golden cross has occured in', df.index.array[n])
                else:
                    pass
#                    print('3. There is no signal in', df.index.array[n])
#                    print(abs(df.iloc[n,8]), abs(maxMinusDiff), abs(df.iloc[n,8]/abs(maxMinusDiff)))
            else:
                pass
#                print('2. There is no signal in', df.index.array[n])            
        else:
            pass
#            print('1. There is no signal in', df.index.array[n])

def backTest(backTestPeriod=20):
    fitIndexNo = 0                        # 알고리즘의 유용성, 적합도
    pedometorNo = 0                       # 시그널이 잡힌 횟수를 기록하는 계측기 변수
    for i in range(sizeOfIndex):
        if df.iloc[i,10] == True:
            pedometorNo += 1
            high = 0
            low = df.iloc[i,3]
            for j in range(i,i+backTestPeriod):
                if j == sizeOfIndex-1:
                    pass
                elif high < df.iloc[j,1]:
                    high = df.iloc[j,1]
                
                if j == sizeOfIndex-1:
                    pass
                elif low > df.iloc[j,2]:
                    low = df.iloc[j,2]
            up = round((high/df.iloc[i,3]-1)*100, 2)
            down = round((1-low/df.iloc[i,3])*100, 2)
            print(df.index.array[i].strftime('%Y-%m-%d'), '에 Golden Cross 신호가 감지되었으며, 신호발생 이후', min(backTestPeriod, sizeOfIndex-i-1),'일간 최대 상승폭은', up,'% 이고, 최대 하락폭은', down, '% 입니다.')
            if up > down:
                fitIndexNo += 1
                if up/down > 1.3:
                    fitIndexNo += 0.5
            elif up < down:
                fitIndexNo -= 1
                if up/down < 0.7:
                    fitIndexNo -= 0.5

    fitIndex = round(fitIndexNo / pedometorNo * 150, 2)
    print('')
    print('해당 주식, 최근', years, '년간의 0000 알고리즘 적합도는', fitIndex, 'points 입니다.')
    print('')
    print('=== 적합도 해석 ===')
    print('  -100 points이면 알고리즘 적용시, 하락 가능성 무척 높음.')
    print('     0 point이면 알고리즘 적용시, 오를 수도 있고 하락할 수도 있음.')
    print('   100 points이면 알고리즘 적용시, 상승 가능성 무척 높음.')

s = 60      # 이동평균선 수 설정
l = 120     # 테스트용으로는 s=3, l=6 사용
years = 3   # 알고리즘 적용 기간
ld, td = getPeriod(years)
df = fdr.DataReader('000660', ld, td)
sizeOfIndex = len(df.index)     # 알고리즘 적용 기간동안의 주가 자료 갯수

tempShort = []
tempLong = []
tempDiff = []
tempDiffSlope = []
tempSignal = []
maxMinusDiff = 0

for d in range(sizeOfIndex):
    tempShort.append(mAverageCalc(d, s))
    tempLong.append(mAverageCalc(d, l))
    tempDiff.append(tempShort[d]-tempLong[d])
    if tempShort[d]-tempLong[d] < maxMinusDiff:
        maxMinusDiff = tempShort[d]-tempLong[d]
    if tempLong[d] == NaN:
        tempDiffSlope.append(NaN)
    elif tempLong[d-1] == NaN:
        tempDiffSlope.append(NaN)
    else:
        tempDiffSlope.append((tempDiff[d]-tempDiff[d-1])/1)
    tempSignal.append(False)

df['mAve60'] = tempShort        # 범용성을 위해선 mAveShort
df['mAve120'] = tempLong        # mAveLong으로 만들 수도 있다.
df['Diff'] = tempDiff
df['Slope'] = tempDiffSlope
df['Signal'] = tempSignal

algo0000()
backTest()

#stocks = fdr.StockListing('KOSPI')
#print(stocks)

# backTest의 finIndex는 0~100에서 -100~100으로 바꾸는 것이 좋을 듯 함.
# 상승 횟수, 하락 횟수, ddm(최대손실), 일정 퍼센트(ex: 30%)를 넘어가는 횟수, 일정 손실을 넘어가는 횟수도 detail항목에서 표시해주면 좋을 듯.

# backTest와, 주식자료 읽어오는 함수, 혹은 알고리즘 함수는 모듈화시키고 불러오는 것이 좋을 듯 함.
# 알고리즘에 부합할 시, True, False가 아니고, 0, 1로 구분하는 것이 좋을 듯 함.
# 이유는 알고리즘을 몇 개 복합적으로 쓸 때, (ex 3개를 쓰면), 0, 1, 2, 3으로 구분될 때, 3만 골라내기 위함.

# 두번째 알고리즘은 4월 구매 10월 판매 (할투)
# 세번째 알고리즘은 52주 최대-최저가 구간에서 하위 10% 이하에서 3일 연속 상승시, 거래량 증가시 구매

# Quant로 할 수 있는 것은, 종목 스크리닝 뿐 아니라, 시간에 따른 판단에도 적용될 수 있음.
# 따라서, backTest를 통해, 매수시점을 판단한다면(매수 후 가격 상승하는 확률이 높은지 확인)
# 같은 논리로 backTest를 통해, 매도시점도 판단할 수 있다.(매도 후 가격 하락하는 확률이 높은지 확인)

# 자체적인 db구축을 하는 게 좋겠다. 유통주식수, PER, PBR 등의 자료를 db안에서 쓰면 좋을 것 같아서.
