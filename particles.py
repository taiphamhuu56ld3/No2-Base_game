import pygame

from support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, _type: str) -> None:
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        if _type == "jump":
            self.frames = import_folder(
                './graphics/character/dust_particles/jump')
        if _type == "land":
            self.frames = import_folder(
                './graphics/character/dust_particles/land')
        self.image: pygame.Surface = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self) -> None:
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift) -> None:
        self.animate()
        self.rect.x += x_shift  # type: ignore
