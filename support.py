from os import walk
from typing import Any, List

import pygame


def import_folder(path: Any) -> List[Any]:
    surface_list: List[Any] = []

    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
