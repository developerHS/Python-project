import turtle as t
import math
import sympy as sym
hidden_x1 = 0 #전처리 
hidden_y1= 0
hidden_x2 = 0
hidden_y2 = 0
hidden_x3 = 0
hidden_y3 = 0
data = []
t.speed(10)
t.hideturtle()
##########선분 그리는 함수##########
def line(x1, y1, x2, y2):
    t.up()
    t.goto(x1, y1)
    t.down()
    t.goto(x2, y2)
    #print("선분 (x:", x1, ", y:", y1, ") --> (x:", x2, ",y:", y2, ") 생성")
    return
##########좌표 적는 함수##########
def write(x, y, text):
    t.up()
    t.goto(x, y)
    t.down()
    t.write(text)

    return

##########점찍는 함수##########
def dot(x, y, size):
    t.up()
    t.goto(x, y)
    t.down()
    t.dot(size)
    #print("점 (x:", x, ", y:", y, ") 생성")
    return

##########두점사이의 거리 구하는 함수##########
def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)** 2+(y2-y1)**2)

##########정삼각형에서 두점이 주어졌을때 나머지 한점을 구하는 함수##########
def tri_o_xy(x1, y1, x2, y2, pin):
    y = sym.Symbol('y') #y 변수 선언 

    if pin==0: 
        equation = sym.Eq(y, (x1+x2)/2 + sym.sqrt(3)/2*(y2-y1))  #정규식 
        xx1 =  sym.solve(equation, y)[0].evalf() #.evalf() - 무리수값을 근사값으로 바꿔서 대입
        
        equation = sym.Eq(y, (y1+y2)/2 - sym.sqrt(3)/2*(x2-x1))
        yy1 = sym.solve(equation, y)[0].evalf() #.evalf() - 무리수값을 근사값으로 바꿔서 대입
        
        dot(xx1, yy1, 10)
        return (xx1, yy1) #튜플형태로 반환 
    elif pin==1:
        equation = sym.Eq(y, (x1+x2)/2 - sym.sqrt(3)/2*(y2-y1)) #정규식 
        xx1 = sym.solve(equation, y)[0].evalf() #.evalf() - 무리수값을 근사값으로 바꿔서 대입
        
        equation = sym.Eq(y, (y1+y2)/2 + sym.sqrt(3)/2*(x2-x1))
        yy1 = sym.solve(equation, y)[0].evalf() #.evalf() - 무리수값을 근사값으로 바꿔서 대입
        
        dot(xx1, yy1, 10)
        return (xx1, yy1) #튜플형태로 반환 
    else:
        print("tri_o_xy error")

##########세점이 주어졌을때 외심 - 무개중심 구하기##########
#설명: 외심-무개중심으로부터 각각의 점까지의 거리가 같다는 성질을 이용해 값을 도출 
def tri_o_m(x1,y1, x2,y2, x3,y3):
    x = sym.Symbol('x') #x변수 선언
    y = sym.Symbol('y') #y변수 선언
    
    ab = (x1-x)** 2+(y1-y)**2   #AP^2 값
    bc = (x2-x)** 2+(y2-y)**2  #BP^2 값 
    ac =  (x3-x)** 2+(y3-y)**2   #CP^2 값

    equation1 = sym.Eq(ab, bc)
    equation2 = sym.Eq(bc, ac)

    dummy = sym.solve(  (equation1, equation2) )
    if type(dummy) == dict:
        xx1 = dummy[x]
        yy1 = dummy[y]
        return (xx1, yy1)
    for i in range(0, len(dummy)): #노이즈 제거
        if dummy[i][x] < 1000 and dummy[i][y] < 1000:
          
            xx1 = dummy[i][x]
            yy1 = dummy[i][y]
    dot(xx1, yy1, 10)
    return (xx1, yy1) #튜플 형태로 반환


##########원 그리기##########
def draw_circle(x, y, r):
    t.up()
    t.goto(x, y-r)
    t.down()
    t.circle(r)

##########원 교점 구하기+페르마 포인트 구하기##########
#설명: 두원의 교점을 지나는 직선의방정식을 구한후, y=~~~꼴로 나타낸후 원의방정식에 대입
def i_dot(x1, y1, r1, x2, y2, r2):
    x1 = round(x1) #소수점 버림 
    y1 = round(y1)
    r1 = round(r1)
    x2= round(x2)
    y2 = round(y2)
    r2 = round(r2)
    x = sym.Symbol('x') #임시변수 x
    y = sym.Symbol('y') #임시변수 y
    main_m = tri_o_m(hidden_x1,hidden_y1,hidden_x2,hidden_y2,hidden_x3,hidden_y3) #메인 삼각형 무개중심
    dot(main_m[0], main_m[1], 10)
    equation1 = (x-x1)**2 + (y-y1)**2 - r1**2  -    (x-x2)**2 - (y-y2)**2 + r2**2  #직선의 방정식
    equation2 =  (x-x1)**2 + (y-y1)**2 - r1**2 #원의방정식1

    equation1 = sym.expand(equation1) #직선의 방정식 전개

    #equation2.subs(y, equation1[0])는 원의 방정식에 직선의 방정식을 대입한 '식'임
    result = sym.solve(equation2.subs(y, sym.solve(equation1, y)[0])) #result리스트에 결과 2개를 대입. 여기서 두원의 교점은 2개이므로 원소는 2개
    r_x1 = round(result[0].evalf())
    r_x2 = round(result[1].evalf())
    r_y1 = sym.solve(equation1.subs(x, r_x1))[0].evalf()
    r_y2 = sym.solve(equation1.subs(x, r_x2))[0].evalf()

    ##----------------------------------
    d1 = distance(main_m[0], main_m[1], r_x1, r_y1) #ABC의 외심과 원의 교점과의 거리 
    d2 = distance(main_m[0], main_m[1], r_x2, r_y2) #ABC의 외심과 원의 교점과의 거리

    if d1 > d2:
        #r_x2, r_y2가 페르마 포인트
        t.color('red')
        dot(r_x2, r_y2, 10)
        t.color('black')
        return(round(r_x2), round(r_y2)) #튜플형태로 소숫점 버리고 반환
    else:
        #r_x1, r_y1가 페르마 포인트
        t.color('red')
        dot(r_x1, r_y1, 10)
        t.color('black')
        return(round(r_x1), round(r_y1)) #튜플형태로 소숫점 버리고 반환
        
    ##------------------------------
    


##########MAIN##########
#좌표평면 그리기
line(-800, 0, 800 , 0) #X축 
line(0, 500, 0, -500) #Y축

#눈금 그리기
for i in range(-800, 800, 50): #X축 눈금 
    line(i, 5, i, -5)
for i in range(500, -500, -50): #Y축 눈금
    line(-5, i, 5, i)
    
#좌표 적기
for i in range(-800, 800, 50): #X축 좌표 적기
    write(i-5, -20, i)
for i in range(500, -500, -50): #Y축 좌표 적기
    if i==0: #0중복 제거 
        continue
    write(10, i, i)

#세점 좌표 입력
x1 = int(t.textinput("Fermat_Point", "x1좌표를 입력해주세요"))
hidden_x1 = x1 #히든 
y1 = int(t.textinput("Fermat_Point", "y1좌표를 입력해주세요"))
hidden_y1 = y1  #히든 
dot(x1, y1, 10)

x2 = int(t.textinput("Fermat_Point", "x2좌표를 입력해주세요"))
hidden_x2 - x2  #히든 
y2 = int(t.textinput("Fermat_Point", "y2좌표를 입력해주세요"))
hidden_y2 = y2  #히든 
dot(x2, y2, 10)

x3 = int(t.textinput("Fermat_Point", "x3좌표를 입력해주세요"))
hidden_x3 = x3  #히든 
y3 = int(t.textinput("Fermat_Point", "y3좌표를 입력해주세요"))
hidden_y3 = y3  #히든 
dot(x3, y3, 10)

#세 선분 이어서 삼각형 그리기
line(x1, y1, x2,  y2)
line(x2, y2, x3, y3)
line(x1, y1, x3, y3)

#정삼각형의 나머지 점들 좌표 대입 
o_x1, o_y1 = tri_o_xy(x1, y1, x2, y2, 0)[0], tri_o_xy(x1, y1, x2, y2, 0)[1]
o_x2, o_y2 = tri_o_xy(x2, y2, x3, y3, 0)[0], tri_o_xy(x2, y2, x3, y3, 0)[1]
o_x3, o_y3 = tri_o_xy(x1, y1, x3, y3, 1)[0], tri_o_xy(x1, y1, x3, y3, 1)[1]

#정삼각형 변 그리기
line(o_x1, o_y1, x1, y1)
line(o_x1, o_y1, x2, y2)
line(o_x2, o_y2, x3, y3)
line(o_x2, o_y2, x2, y2)
line(o_x3, o_y3, x1, y1)
line(o_x3, o_y3, x3, y3)

#외심(무개중심)의 좌표 대입 
o_m_x1, o_m_y1 = tri_o_m(x1, y1, x2, y2, o_x1, o_y1 )[0], tri_o_m(x1, y1, x2, y2, o_x1, o_y1 )[1]
o_m_x2, o_m_y2 = tri_o_m(x2, y2, x3, y3, o_x2, o_y2 )[0], tri_o_m(x2, y2, x3, y3, o_x2, o_y2 )[1]
o_m_x3, o_m_y3 = tri_o_m(x1, y1, x3, y3, o_x3, o_y3 )[0], tri_o_m(x1, y1, x3, y3, o_x3, o_y3 )[1]

#원 그리기
d1 = distance(o_m_x1, o_m_y1, x1, y1) #반지름 
draw_circle(o_m_x1, o_m_y1, d1)
d2 = distance(o_m_x2, o_m_y2, x2, y2) #반지름 
draw_circle(o_m_x2, o_m_y2, d2)
d3 = distance(o_m_x3, o_m_y3, x3, y3) #반지름 
draw_circle(o_m_x3, o_m_y3, d3)

#원 교점 구하기-->Fermat_Point
fermat_point = i_dot(o_m_x1, o_m_y1, d1, o_m_x2, o_m_y2, d2)

#Fermat_Point 출력
print("\n\n\n [결과]: 페르마 포인트의 좌표는 x:",fermat_point[0],", y:",fermat_point[1],"입니다.")
t.done()










###############################################읽어주세요!! 
#i_dot함수에서 식을 풀면서 교점 2개가 나오는데 그중에서 원래 삼  
#각형 ABC의 외심과 가장 가까운 점을 페르마 포인트라고 가정 하고
#페르마포인트를 구하는 프로그램임. 그리고 계산의 용이성을 위해 
#소수점을 버림하고 계산하기에 +-1.5정도 오차가 있을수 있음.         
########################################################
