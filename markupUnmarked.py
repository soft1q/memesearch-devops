import os
import django
import torch
import sys

from config import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from memes.models import Memes
from memes.ocr_pipeline.craft import CRAFT
from memes.ocr_pipeline.recognition import netInference, copyStateDict


def markUp(n=500):

    # ImageDescriptions.objects.all().delete()
    # TextDescriptions.objects.all().delete()

    net = CRAFT()
    net.load_state_dict(copyStateDict(torch.load("memes/ocr_pipeline/craft_mlt_25k.pth", map_location='cpu')))
    net.eval()

    for _ in range(n):
        try:
            meme = Memes.objects.filter(textDescription="").order_by('?')[0]
        except Exception:
            break
        print("memeID: " + str(meme.id))
        y = settings.Y
        path = 'media/toMarkup'   # по идее по этому адрсу и будет лежать картинка, можешь поменять адрес как тебе надо
        y.download(meme.fileName, path)
        textDescription = " ".join(netInference(net, path))
        if os.path.isfile(path):
            os.remove(path)
        # Построение нового индекса по добавленному мему
        meme.textDescription = textDescription

        meme.is_mark_up_added = False
        meme.save()  # при сохранении индекс сам обновляется для этого мема
        break


if __name__ == '__main__':
    if len(sys.argv) > 1:
        markUp(sys.argv[1])
    else:
        markUp()
