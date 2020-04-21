import os
import time

import yadisk
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

import searchEngine.models as indexer_models
from memes.compressor import compress_image
from searchEngine.indexer import indexer
from searchEngine.indexer import info
from searchEngine.indexer import misc
from searchEngine.indexer import simplifier
from tags.models import Tags


def update_index_in_db(text, description, new_index_text, new_index_description):
    """
    function add new indexes to database

    :param text: old text description
    :param description: old image description
    :param new_index_text: builded index for words in text description that must be added to DB
    :param new_index_description: builded index for words in image description that must be added to DB
    :return:
    """
    simplified_text = simplifier.simplify_string(text)
    simplified_description = simplifier.simplify_string(description)

    if simplified_text == '' and simplified_description == '':
        return

    text_words = simplified_text.split(' ')
    description_words = simplified_description.split(' ')

    if simplified_text != '':
        text_index = indexer_models.TextDescriptions.objects.filter(Q(word__in=text_words))
        updated_text_words = []
        if text_index is not None:  # otherwise no need to update
            for row in text_index:
                updated_text_words.append(row.word)
                row.index = str(misc.union_text(row.index, new_index_text[row.word]))
                row.save()

        for word in text_words:  # create for new words
            if not (word in updated_text_words):
                indexer_models.TextDescriptions.objects.create(word=word, index=new_index_text[word])

    if simplified_description != '':
        descr_index = indexer_models.ImageDescriptions.objects.filter(Q(word__in=description_words))
        updated_descr_words = []
        if descr_index is not None:  # otherwise no need to update
            for row in descr_index:
                updated_descr_words.append(row.word)
                row.index = str(misc.union_descr(row.index, new_index_description[row.word]))
                row.save()

        for word in description_words:  # create for new words
            if not (word in updated_descr_words):
                indexer_models.ImageDescriptions.objects.create(word=word, index=new_index_description[word])


class Memes(models.Model):
    # ID
    id = models.AutoField(primary_key=True, unique=True)
    # файл картинки
    image = models.ImageField(blank=True, null=True)
    # имя файла при загрузке  облако
    fileName = models.TextField(blank=True, null=True)
    # последняя известная ссылка на файл в облаке
    url = models.URLField(blank=True, null=True, max_length=500)
    # имя сжатого файла при загрузке в облако
    fileName_compressed = models.TextField(blank=True, null=True)
    # последняя известная ссылка на сжатый файл в облаке
    url_compressed = models.URLField(blank=True, null=True, max_length=500)
    # строка с описанием текста на картинке
    textDescription = models.TextField(blank=True, null=True)
    # строка с описанием изображения
    imageDescription = models.TextField(blank=True, null=True)
    # список пользователей добавивших мем в коллекцию
    owner = models.ManyToManyField(User, related_name="ownImages", blank=True)
    # флаг что мем был доразмечен
    is_mark_up_added = models.NullBooleanField()
    # список тегов присвоенных мему
    tags = models.ManyToManyField(Tags, related_name="taggedMemes", blank=True)

    def delete(self, **kwargs):
        pass

    def save(self, *args, **kwargs):
        first_save = False
        if self.image is not None and self.image != '':
            first_save = True
            # Разметка мема (текст)
            # self.textDescription = re.sub("[^а-яa-z0-9 ]+", "", " ".join(getTextFromImage(self.image)).lower())

            # Сохранение мема на яндекс.диск
            y = settings.Y
            name = self.image.url.split(".")
            self.fileName = ".".join(name[:-1]) + "_{}".format(time.time()) + ".jpg"

        # Построение нового индекса по добавленному мему
        meme_index = indexer.full_index([info.MemeInfo(self.id, self.textDescription, self.imageDescription)])
        update_index_in_db(self.textDescription, self.imageDescription, meme_index.text_words, meme_index.descr_words)

        super(Memes, self).save(*args, **kwargs)
        if self.image is not None and self.image != '':
            if os.path.isfile(self.image.path):
                # сжатие картинки
                compress_image(self.image.path, self.fileName[1:])
                y.upload(self.fileName[1:], self.fileName)
                self.url = yadisk.functions.resources.get_download_link(y.get_session(), self.fileName)
                os.remove(self.image.path)
                os.remove(self.fileName[1:])
                self.image = None
                super(Memes, self).save(update_fields=['image'])

        if first_save and self.id % 100 == 0:
            y.upload("db.sqlite3", "backup/db_{}.sqlite3".format(self.id))
