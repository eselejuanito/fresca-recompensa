import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException


def process_code(code, day, month, year, hour, minute, meridian):
    # Especificar que se quiere usar HtmlUnit como navegador
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 2)

    driver.get("https://nu.globaldqfeedback.com/mex")

    next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
    next_button.click()

    code_input = wait.until(EC.presence_of_element_located((By.ID, "CN1")))
    code_input.send_keys(code)

    day_input = Select(wait.until(EC.presence_of_element_located((By.ID, "InputDay"))))
    day_input.select_by_value(day)
    month_input = Select(wait.until(EC.presence_of_element_located((By.ID, "InputMonth"))))
    month_input.select_by_value(month)
    year_input = Select(wait.until(EC.presence_of_element_located((By.ID, "InputYear"))))
    year_input.select_by_value(year[-2:])

    hour_input = wait.until(EC.presence_of_element_located((By.ID, "InputHour")))
    hour_input.send_keys(hour)
    minute_input = wait.until(EC.presence_of_element_located((By.ID, "InputMinute")))
    minute_input.send_keys(minute)
    meridian_input = wait.until(EC.presence_of_element_located((By.ID, "InputMeridian")))
    meridian_input.send_keys(meridian)

    next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
    next_button.click()

    # Se detectaron X errores en la página.
    try:
        # Verificar que se hayan enviado los datos correctos, de no ser asi, parar selenium y enviar error.
        error = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@name='ErrorMessageOnTopOfThePage']")))
        print(error.text)
        return {'answer': error.text}
    except TimeoutException:
        print("Sin error en los parametros enviados, hay que continuar...")

    # Se detectaron X errores en la página.
    try:
        error = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="hardblock"]/p')))
        print(error.text)
        return {'answer': error.text + '*Ya se reclamo este codigo, favor de usar otros datos por favor :D.'}
    except TimeoutException:
        print("Parametros no usados previamente, hay que continuar...")

    # Resolviendo el cuestionario, aún es posible recibir error al resolverlo.
    try:
        # Por favor, califique su satisfacción general respecto a su experiencia en Dairy Queen. 1 al 5.
        first_question = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="FNSR000007"]/td[1]')))
        first_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # ¿Qué tipo de visita realizó?. 1. Comió en el establecimiento, 2. Ordenó para llevar, 3. Entrega a domicilio
        second_question = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="FNSR000010"]/div/div/div[2]/label')))
        second_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # ¿Qué ordenó? Marque todos los que correspondan. 1.Bebidas, 2.Pastel helado, 3.Helados, 4.Otro
        third_question = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="FNSR000012"]/label')))
        third_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # Califique su grado de satisfacción con:
        for i in range(2, 9):
            fourth_question = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div/table/tbody/tr[' + str(i) + ']/td[1]')))
            fourth_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # Califique su grado de satisfacción con:
        for i in range(2, 5):
            fifth_question = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div/table/tbody/tr[' + str(i) + ']/td[1]')))
            fifth_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # ¿Tuvo un problema durante su experiencia en Dairy Queen?
        sixth_question = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="FNSR000032"]/td[2]/span')))
        sixth_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # Con base en esta experiencia, ¿cuáles son las probabilidades de que usted…?
        for i in range(2, 4):
            seventh_question = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div/table/tbody/tr[' + str(i) + ']/td[1]')))
            seventh_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # Comentarios de satisfaccion
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # Le dieron las gracias?
        for i in range(2, 6):
            x_question = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div/table/tbody/tr[' + str(i) + ']/td[1]')))
            x_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # ¿Te lo entregaron al revez?
        eighth_question = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div/table/tbody/tr[2]/td[1]/span')))
        eighth_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # Califique su grado de satisfacción con respecto a lo siguiente:
        for i in range(2, 7):
            nineth_question = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div/table/tbody/tr[' + str(i) + ']/td[1]')))
            nineth_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # Incluyendo esta ocasión, ¿cuántas veces ha visitado este Dairy Queen en los ultimos 30 días?.
        tenth_question = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div/fieldset/div/div/div[4]/span')))
        tenth_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # ¿Le gustaría hacer un reconocimiento a algún miembro del equipo por haber hecho un esfuerzo adicional para darle un servicio excepcional?
        eleventh_question = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[3]/div[2]/form/div/fieldset/div/div/div[2]/span')))
        eleventh_question.click()
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        # Por favor, indique su edad:
        select = wait.until(EC.element_to_be_clickable((By.ID, "R000120")))
        select = Select(select)
        select.select_by_visible_text("Prefiero no responder")
        next_button = wait.until(EC.element_to_be_clickable((By.ID, "NextButton")))
        next_button.click()

        validation_code = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="finishIncentiveHolder"]/p[3]')))
        result = re.findall(r'\d+', validation_code.text)
        print(result[0])

        driver.quit()
        return {'answer': 'El codigo para tu nieve es ' + result[0]}
    except TimeoutException:
        error = 'Hubo un error al llenar el cuestionario, hay que volver a intentarlo.'
        print(error)
        return {'answer': error}
