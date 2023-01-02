from PyPDF2 import PdfWriter, PdfReader
from pdf2image import convert_from_path
from app import app
from PIL import Image
import shutil
import os
import math


PROJECT_DIR = app.config['PROJECTS_DIR']
# CUR_DIR = 'C:\\Работа\\Гуртяков\\flask-back\\app\\lib\\pdf2tiles'
CUR_DIR = os.path.join(app.config['BASE_DIR'], 'app\\lib\\pdf2tiles')


def __create_tiles__(img_high, img_medium, img_low, max_zoom, path):

    img_width, img_height = img_high.size

    for level in range(max_zoom + 1):

        log_tile_size = 0

        if max_zoom > level:
            log_tile_size = 256 << (max_zoom - level)
        else:
            log_tile_size = 256 >> (max_zoom - level)

        num_tiles_x = 0
        num_tiles_y = 0

        if img_width % log_tile_size == 0:
            num_tiles_x = int(img_width / log_tile_size)
        else:
            num_tiles_x = int(img_width / log_tile_size + 1)

        if img_height % log_tile_size == 0:
            num_tiles_y = int(img_height / log_tile_size)
        else:
            num_tiles_y = int(img_height / log_tile_size + 1)

        image_new_canvas = Image.new("RGBA", (256 * num_tiles_x, 256 * num_tiles_y), color='white')

        # Изменение размеров картинки
        size = int(img_width / (log_tile_size / 256)), int(img_height / (log_tile_size / 256))

        img_new = img_high.copy()
        if max(size) < max(img_low.size):
            img_new = img_low.copy()
        elif max(size) < max(img_medium.size):
            img_new = img_medium.copy()

        img_new = img_new.resize(size)
        image_new_canvas.paste(img_new, (0, 0))

        # Создание директивы
        zoom_count_str = str(level)
        pathz = path + zoom_count_str
        if not os.path.exists(pathz):
            os.mkdir(pathz)
        else:
            shutil.rmtree(pathz)
            os.mkdir(pathz)

        imag_width, imag_height = image_new_canvas.size

        row_count = 0
        column_count = 0

        # Нарезка тайлов
        for row in range(0, imag_height, 256):
            column_count = 0
            for column in range(0, imag_width, 256):
                sum_width = column + 256
                sum_height = row + 256

                im_crop = image_new_canvas.crop((column, row, sum_width, sum_height))

                im_crop.save(f'{pathz}/{row_count}x{column_count}.png')
                column_count += 1
            row_count += 1


class Pdf2Tiles:
    def __init__(self, project_name, pages, project_id, pages_id_list, project_dir=None):
        self.project_name = project_name
        self.pages = pages
        self.project_id = project_id
        self.pages_id_list = pages_id_list
        # [{'name': 'Floor 1', 'page': 15}, {'name': 'Floor 2', 'page': 17}, {'name': 'Floor 3', 'page': 22}]

        self.__WRITER__ = PdfWriter()
        self.__POPPLER__ = os.path.join(CUR_DIR, 'poppler-22.04.0\\Library\\bin')
        self.__TILE_SIZE__ = 256

        if project_dir is None:
            project_dir = os.path.join(PROJECT_DIR, str(self.project_id))
        self.project_dir = project_dir

        if not os.path.exists(self.project_dir):
            os.mkdir(self.project_dir)

    def run(self, path_to_pdf):
        self.__create_reader__(path_to_pdf)
        self.__create_pdf__()
        path_list = self.__create_image__(800)
        return path_list

    def __create_reader__(self, path_to_pdf):
        self.path_to_pdf = path_to_pdf
        self.reader = PdfReader(path_to_pdf)

    def __create_pdf__(self):
        for page in self.pages:
            self.__WRITER__.addPage(self.reader.getPage(page['pageNum'] - 1))

        with open(f"{self.project_dir}\\{self.project_name}.pdf", "wb") as f:
            self.__WRITER__.write(f)

    def __create_image__(self, max_dpi):
        """
            Конвертирует из pdf-файла страницы в изображения в разных качествах (максимальное, среднее и низкое).

            param max_dpi: Максимальный dpi 
        """

        # Создает папку ассетов проекта
        if not os.path.exists(f'{self.project_dir}'):
            os.mkdir(f'{self.project_dir}')

        path = os.path.join(self.project_dir, self.project_name + '.pdf')

        images_high_quality = convert_from_path(
            pdf_path=path,
            dpi=max_dpi,
            poppler_path=self.__POPPLER__
        )

        images_medium_quality = convert_from_path(
            pdf_path=path,
            dpi=int(max_dpi/2),
            poppler_path=self.__POPPLER__
        )

        images_low_quality = convert_from_path(
            pdf_path=path,
            dpi=int(max_dpi/5),
            poppler_path=self.__POPPLER__
        )

        path_list = []

        for i, image_high in enumerate(images_high_quality):
            if not os.path.exists(f'{self.project_dir}\\{self.pages_id_list[i]}'):
                os.mkdir(f'{self.project_dir}\\{self.pages_id_list[i]}')

            # path_list.append(f'{self.project_dir}\\{self.pages[i]["pageName"]}')
            page_dict = {}
            # page_dict['path'] = f'{self.project_dir}\\{self.pages[i]["pageName"]}'

            image_medium = images_medium_quality[i]
            image_low = images_low_quality[i]

            # Высчисление оригинального зумирования
            img_width, img_height = image_high.size
            size = max(img_height, img_width)
            number_tiles = size / self.__TILE_SIZE__

            original_zoom = math.ceil(math.log(number_tiles, 2))

            page_dict['zoom'] = original_zoom
            # dbmanager.create_blueprint(dbmanager.get_last_id(), blueprints_list[i]['name'], f'{project_name}\{i}', original_zoom)
            path_list.append(page_dict)
            
            __create_tiles__(image_high, image_medium, image_low, original_zoom,
                                  f'{self.project_dir}\\{self.pages_id_list[i]}\\')
        
        return path_list

