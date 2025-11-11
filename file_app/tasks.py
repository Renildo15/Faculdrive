from celery import shared_task
from .models import Archive
import time

@shared_task
def process_archive_task(archive_id):
    from .models import Archive

    try:
        archive = Archive.objects.get(id=archive_id)
    except Archive.DoesNotExist:
        return f"Archive {archive_id} não encontrado."

    time.sleep(5)

    archive.processed = True
    archive.save()

    print(f"Processamento concluído para o arquivo {archive.file.name}")

    return f"Arquivo {archive_id} processado com sucesso!"
