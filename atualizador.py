from apscheduler.schedulers.blocking import BlockingScheduler
from scraping import extrair_dados  # importa a função corretamente

def job_scraping():
    print("Iniciando scraping e salvando dados...")
    extrair_dados()  # ← chame a função diretamente
    print("Scraping concluído!")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(job_scraping, 'interval', minutes=15)  # Para teste: a cada 30s

    print("Scheduler iniciado. Scraping rodando a cada 15 minutos.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler parado.")
