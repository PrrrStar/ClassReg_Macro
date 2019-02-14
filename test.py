from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

#Line Token 연동
API_HOST = 'https://notify-api.line.me'
url = 'https://notify-api.line.me/api/notify'
token = {'Authorization': 'Bearer 4S1Dx1IsEISN6YapumXjQw2feFRGvSZqULXulnWYpFk'}
data = {}

# Chrome을 안 띄우고 수행하고 싶으면 아래 주석을 해제하자. (리눅스 서버에서 작업시 headless)

# options.add_argument("headless")
# setup Driver|Chrome : 크롬드라이버를 사용하는 driver 생성
driver = webdriver.Chrome('D:\\Project\\chromedriver_win32\\chromedriver')
driver.get("https://for-s.seoultech.ac.kr/index.jsp")           # 수강신청 메인페이지



driver.implicitly_wait(2) 

print("학번 : ")
stNum = input("")

print("비밀번호 : ")
pw = input("")

print(stNum)
print("*"*len(pw))


driver.find_element_by_name('USER_NUMB').send_keys(stNum)  # 학번 입력
driver.find_element_by_name('PWD').send_keys(pw)      # 비밀번호 입력c
driver.find_element_by_id('btn_Login').click()

#1.장바구니 조회   2. 소속분반과목조회   3. 요일별 조회   4. 특정과정과목조회   5.과목직접입력
print("1.장바구니 조회    2. 소속분반과목조회    3. 요일별 조회    4. 특정과정과목조회    5.과목직접입력")
tabNo = input("")

if (tabNo=="1"):
    print("1. 장바구니 조회")
    driver.get("https://for-s.seoultech.ac.kr/view/sugang.jsp#tab-basket")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.select('tbody')[3]
    remainNum = table.select('tr > td:nth-child(17)')
    subjectName = table.select('tr > td:nth-child(3)')

    print("1. 전체선택")
    print("2. 일부선택")
    select = input("")
   

    while True:
        if select == "1":
            driver.find_element_by_id('cb_grd_basket').click()
            driver.find_element_by_id('btn_basketSave').click()
        
        elif select == "2":
            basketNo = []
            field = []
            for saveIdNum in range(1,len(remainNum)):
                print("{}. 과목명 : {}  잔여인원 : {}\n\n".format(saveIdNum, subjectName[saveIdNum].text, remainNum[saveIdNum].text))

                print("해당 과목 번호 입력 :  (입력을 마치려면 x 키를 눌러주세요)")
                basketNo[saveIdNum] = input("")
                field[saveIdNum] = driver.find_element_by_xpath('//*[@id="jqg_grd_basket_%s"]'%basketNo[saveIdNum])

            selectedCheckBox = table.select('tr:nth-child(%s)'%basketNo[saveIdNum])
            
            escape=False
            for count in range(1,len(field)):
                if remainNum[count].text != "0":
                    print("click")
                    field[count].click()
                    message = "%s수강신청이 완료되었습니다." %subjectName[count].text
                    print(message)
                driver.switch_to_alert().accept()
                escape = True
                break
        if escape == True:
            break

        driver.refresh()
        driver.switch_to_alert().accept()


elif (tabNo=="2"):
    print("2. 소속분반과목조회")
    driver.get("https://for-s.seoultech.ac.kr/view/sugang.jsp#tab-clas")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    cbo_clasClas = soup.select('#cbo_clasClas > option')

    table = soup.select('tbody')[3]
    remainNum = table.select('tr > td:nth-child(17)')
    subjectName = table.select('tr > td:nth-child(3)')

    for i, a in enumerate(cbo_clasClas):
        print("{}. {}".format(i+1,a.text))
    print("소속분반 번호 입력")
    cbo_clasClas_No = input("")

    for i, a in enumerate(subjectName):
        print("{}. {}".format(i+1,a.text))
    print("과목 번호 입력 : ")
    cbo_clasClas_No = input("")
    
    for i in range(5,-1,-1):
        print(i)
        sleep(1)
    print("매크로를 시작합니다.")

    while(True):
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        cbo_clasClas_field = driver.find_element_by_xpath('//*[@id="cbo_clasClas"]/option[%s]'%cbo_clasClas_No)
        cbo_clasClas_field.click()
        

        print("소속분반 : %s"%cbo_clasClas_field.text)

        sleep(0.1)
        driver.find_element_by_id('btn_clasSearch').click()

        escape=False
        for saveIdNum in range(1,len(remainNum)):
            print(subjectName[saveIdNum].text,remainNum[saveIdNum].text)
            field = driver.find_element_by_xpath('//table[@id=""]//tr[@id="%s"]/td[1]/input'%saveIdNum)
            if remainNum[saveIdNum].text != "0":
                print("click")
                field.click()
                print("%s수강신청이 완료되었습니다." %subjectName[saveIdNum].text)
                message = "%s수강신청이 완료되었습니다." %subjectName[saveIdNum].text
                driver.switch_to_alert().accept()
                escape = True
                break
        if escape == True:
            break

        driver.refresh()
        driver.switch_to_alert().accept()

elif (tabNo=="3"):
    print("3. 요일별 조회")
    driver.get("https://for-s.seoultech.ac.kr/view/sugang.jsp#tab-dayLess")
    
    driver.switch_to_alert().accept()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    majorList = soup.select('#cbo_dayLessLess > option')
    dnList = soup.select('#cbo_dayLessDnDiv > option')
    dayList = soup.select('#cbo_dayLessDays > option')

    table = soup.select('tbody')[3]
    remainNum = table.select('tr > td:nth-child(17)')
    subjectName = table.select('tr > td:nth-child(3)')

    for i,a in enumerate(majorList):
        print("{}. {}".format(i+1,a.text))    
    print("전공번호 입력 (미선택시 자동으로 본인 전공 선택)")
    majorNo = input("")

    for i,a in enumerate(dnList):
        print("{}. {}".format(i+1,a.text))
    print("주야 선택")
    dn =input("")

    for i,a in enumerate(dayList):
        print("{}. {}".format(i+1,a.text))
    print("요일 (미선택시 전체)")
    day =input("")


    print("과목명 (두글자 이상 입력)")
    subjKnm =input("")
    
    #카운트다운
    for i in range(5,-1,-1):
        print(i)
        sleep(1)
    print("매크로를 시작합니다.")    

    while(True):
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        majorField = driver.find_element_by_xpath('//*[@id="cbo_dayLessLess"]/option[%s]'%majorNo)
        dnField = driver.find_element_by_xpath('//*[@id="cbo_dayLessDnDiv"]/option[%s]'%dn)
        dayField = driver.find_element_by_xpath('//*[@id="cbo_dayLessDays"]/option[%s]'%day)

        majorField.click()
        dnField.click()
        dayField.click()
        driver.find_element_by_id('edt_dayLessSubjKnm').send_keys(subjKnm)
        
        print(majorField.text, dnField.text," ", dayField.text, " ", "입력값 : ",subjKnm)
        sleep(0.1)

        driver.find_element_by_id('btn_dayLessSearch').click()

        escape=False
        for saveIdNum in range(1,len(remainNum)):
            print(subjectName[saveIdNum].text,remainNum[saveIdNum].text)
            field = driver.find_element_by_xpath('//table[@id="grd_dayLess"]//tr[@id="%s"]/td[1]/input'%saveIdNum)
            if remainNum[saveIdNum].text != "0":
                print("click")
                field.click()
                print("%s수강신청이 완료되었습니다." %subjectName[saveIdNum].text)
                message = "%s수강신청이 완료되었습니다." %subjectName[saveIdNum].text
                driver.switch_to_alert().accept()
                escape = True
                break
        if escape == True:
            break

        driver.refresh()
        driver.switch_to_alert().accept()

elif (tabNo=="4"):
    print("4. 특정과정과목조회")
    driver.get("https://for-s.seoultech.ac.kr/view/sugang.jsp#tab-specCors")

    
elif (tabNo=="5"):
    print("5. 과목직접입력")
    driver.get("https://for-s.seoultech.ac.kr/view/sugang.jsp#tab-direct")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    print("교과목 코드 : ")
    directSubjCd = input("")

    print("강좌번호 : ")
    directLectNumb = input("")
    
    #카운트다운
    for i in range(5,-1,-1):
        print(i)
        sleep(1)
    print("매크로를 시작합니다.")  
    
    while(True):
        driver.find_element_by_id('edt_directSubjCd').send_keys(directSubjCd)
        driver.find_element_by_id('edt_directLectNumb').send_keys(directLectNumb)
        driver.find_element_by_id('btn_directSave').click()

        if "개설된 강좌가 없거나" in driver.switch_to_alert().text:
            driver.switch_to_alert().accept()
            message = driver.switch_to_alert().text

        elif "중복" in driver.switch_to_alert().text:
            driver.switch_to_alert().accept()
            message = driver.switch_to_alert().text

        elif "수강신청" in driver.switch_to_alert().text:
            driver.switch_to_alert().accept()
            message = driver.switch_to_alert().text
            break

parameter = {"message": message}
# Response
response = requests.post(url, headers =token, data = parameter)
print(response.text)