import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime, timedelta

# --- CONFIGURAÇÕES DO AMBIENTE ---
# Preencha com as credenciais do seu SUPERUSUÁRIO
ADMIN_USERNAME = 'PH' 
ADMIN_PASSWORD = 'Pede10571057'
BASE_URL = 'http://127.0.0.1:8000/' 


class BarberFlowTests(unittest.TestCase):
    
    def setUp(self):
        # Inicializa o driver do Selenium (certifique-se de que o chromedriver está configurado)
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10) # Tempo de espera implícito
        self.driver.get(BASE_URL)
        print("--- Teste Iniciado ---")


    def tearDown(self):
        # Fecha o navegador após cada teste
        self.driver.quit()
        print("--- Teste Finalizado ---")


    def login_admin(self):
        """Função auxiliar para login no painel de administração."""
        self.driver.get(BASE_URL + 'admin/')
        
        # Espera o campo de login aparecer
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = self.driver.find_element(By.NAME, "password")
        
        username_field.send_keys(ADMIN_USERNAME)
        password_field.send_keys(ADMIN_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        
        # Verifica se o login foi bem-sucedido
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('admin/')
        )
        print(f"Login de Admin em {datetime.now().strftime('%H:%M:%S')}: OK")


    def test_01_cadastro_e_login(self):
        """CT-06: Validar Autenticação e Cadastro (RF01/RF02 adaptados)."""
        print("\n[CT-06] Iniciando Teste de Autenticação e Cadastro.")
        driver = self.driver
        
        # 1. Acessar tela de cadastro
        driver.get(BASE_URL + 'cadastro/')
        self.assertIn('Cadastro', driver.title)
        
        # Dados de um novo cliente
        timestamp = datetime.now().strftime("%H%M%S")
        username = f"novo_cliente_{timestamp}"
        email = f"cliente.{timestamp}@teste.com"
        
        # 2. Preencher e submeter formulário de cadastro (RF01)
        driver.find_element(By.ID, "id_username").send_keys(username)
        driver.find_element(By.ID, "id_email").send_keys(email)
        driver.find_element(By.ID, "id_password1").send_keys("senha1234")
        driver.find_element(By.ID, "id_password2").send_keys("senha1234")
        driver.find_element(By.ID, "id_telefone").send_keys("34999998888")
        
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Resultado Esperado: Redirecionamento para a página de agendamento e mensagem de sucesso.
        WebDriverWait(driver, 10).until(EC.url_to_be(BASE_URL))
        self.assertIn('Agendamento', driver.title)
        self.assertTrue("sucesso" in driver.page_source, "Falha no CT-06: Mensagem de sucesso não apareceu após cadastro.")
        print("[CT-06] Cadastro de Cliente e Login Automático: OK.")


    # No arquivo selenium_barberflow_tests.py

    def test_02_cadastro_servico_e_barbeiro_admin(self):
        """CT-03 Adaptado: Validar cadastro de Serviço e Barbeiro (via Admin)."""
        print("\n[CT-03] Iniciando Teste de Cadastro de Serviço e Barbeiro.")
        self.login_admin()
        driver = self.driver
        
        # --- Cadastrar Serviço ---
        driver.get(BASE_URL + 'admin/agendamentos/servico/add/')
        
        # --- CORREÇÃO AQUI ---
        # Espera a página carregar e o campo "id_nome" aparecer (até 10 seg)
        try:
            nome_servico_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "id_nome"))
            )
        except TimeoutException:
            self.fail("Página de adicionar serviço demorou muito para carregar ou 'id_nome' não encontrado.")

        # Dados do Serviço
        service_name = f"Selenium Teste - {datetime.now().strftime('%M%S')}"
        nome_servico_field.send_keys(service_name)
        driver.find_element(By.ID, "id_preco").send_keys("50.00")
        driver.find_element(By.ID, "id_duracao_minutos").send_keys("60")
        
        driver.find_element(By.NAME, "_save").click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains('admin/agendamentos/servico/')
        )
        
        self.assertTrue(service_name in driver.page_source, "Falha no CT-03: Serviço não foi salvo no Admin.")
        print("[CT-03] Cadastro de Serviço: OK.")
        
        # --- Cadastrar Barbeiro ---
        driver.get(BASE_URL + 'admin/agendamentos/barbeiro/add/')
        
        # --- CORREÇÃO AQUI ---
        # Espera a página carregar e o campo "id_nome" aparecer
        try:
            nome_barbeiro_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "id_nome"))
            )
        except TimeoutException:
            self.fail("Página de adicionar barbeiro demorou muito para carregar ou 'id_nome' não encontrado.")

        barber_name = f"Barbeiro Teste {datetime.now().strftime('%M%S')}"
        nome_barbeiro_field.send_keys(barber_name)
        driver.find_element(By.ID, "id_especialidade").send_keys("Cortes Clássicos")
        driver.find_element(By.NAME, "_save").click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains('admin/agendamentos/barbeiro/')
        )
        
        self.assertTrue(barber_name in driver.page_source, "Falha no CT-03: Barbeiro não foi salvo no Admin.")
        print("[CT-03] Cadastro de Barbeiro: OK.")


    # No arquivo selenium_barberflow_tests.py

    def test_03_agendamento_completo_e_regra_negocio(self):
        """CT-02 + Validações: Agendamento, Ocupação e Domingo."""
        print("\n[CT-02] Iniciando Teste de Agendamento e Regras de Negócio.")
        
        # Pré-requisito: Login. (Usamos o admin 'PH' que agora tem um perfil Cliente)
        self.login_admin() 
        driver = self.driver
        
        driver.get(BASE_URL) # Vai para a página de agendamento
        
        # --- 1. Agendamento Básico (Ocupa o horário) ---
        
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        if tomorrow.weekday() == 6: 
            tomorrow += timedelta(days=1)
        
        # Formato correto (sem segundos)
        valid_date_time = tomorrow.strftime('%Y-%m-%dT%H:%M')
        
        # Seleciona o primeiro barbeiro e serviço (index [1] pois [0] é "---------")
        driver.find_element(By.NAME, "barbeiro").find_elements(By.TAG_NAME, "option")[1].click()
        driver.find_element(By.NAME, "servico").find_elements(By.TAG_NAME, "option")[1].click()
        
        # --- CORREÇÃO AQUI: Usando JavaScript para definir a data ---
        # O send_keys é instável para inputs datetime-local.
        date_element = driver.find_element(By.NAME, "data_e_hora")
        driver.execute_script(f"arguments[0].value = '{valid_date_time}';", date_element)
        
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Resultado Esperado: Agendamento bem-sucedido
        WebDriverWait(driver, 10).until(EC.url_to_be(BASE_URL))
        
        time.sleep(0.5) 
        
        self.assertTrue("sucesso" in driver.page_source, "Falha no CT-02: Agendamento básico falhou.")
        print("[CT-02] Agendamento Básico: OK.")

        # --- 2. Tentar Agendar Horário Ocupado (Regra de Negócio) ---
        
        # Tenta agendar o mesmo horário
        driver.find_element(By.NAME, "barbeiro").find_elements(By.TAG_NAME, "option")[1].click()
        driver.find_element(By.NAME, "servico").find_elements(By.TAG_NAME, "option")[1].click()
        
        # --- CORREÇÃO AQUI: Usando JavaScript ---
        date_element_occupied = driver.find_element(By.NAME, "data_e_hora")
        driver.execute_script(f"arguments[0].value = '{valid_date_time}';", date_element_occupied)
        
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Resultado Esperado: Erro de validação.
        time.sleep(0.5) # Garante que o erro apareça
        self.assertTrue("Este horário já está agendado" in driver.page_source, "Falha na Regra de Negócio: Não bloqueou horário ocupado.")
        print("[CT-02] Bloqueio de Horário Ocupado: OK.")

        # --- 3. Tentar Agendar em Domingo (Regra de Negócio) ---
        
        next_sunday = datetime.now()
        while next_sunday.weekday() != 6: # 6 é Domingo
            next_sunday += timedelta(days=1)
        
        sunday_date_time = next_sunday.strftime('%Y-%m-%dT11:00')
        
        # --- CORREÇÃO AQUI: Usando JavaScript ---
        date_element_sunday = driver.find_element(By.NAME, "data_e_hora")
        driver.execute_script(f"arguments[0].value = '{sunday_date_time}';", date_element_sunday)
        
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Resultado Esperado: Erro de validação.
        time.sleep(0.5) # Garante que o erro apareça
        self.assertTrue("A barbearia não funciona aos domingos" in driver.page_source, "Falha na Regra de Negócio: Não bloqueou agendamento em domingo.")
        print("[CT-02] Bloqueio de Domingo: OK.")


if __name__ == '__main__':
    # Este é o ponto de entrada para rodar os testes
    unittest.main(argv=['first-arg-is-ignored'], exit=False)