from ClientLauncher.MainFunctions.image import Image
from ClientLauncher.MainFunctions.mouse_and_keyboard import Mouse


image = Image()
mouse = Mouse()


def check_ok_button() -> bool:
    image.take_screenshot('imgs\\screenshots\\lobby\\is_there_ok_button.png', (900, 530, 1010, 565))
    return image.matching('imgs\\screenshots\\lobby\\is_there_ok_button.png',
                          'imgs\\templates\\lobby\\there_is_ok_button.png')


def click_ok_button():
    mouse.move_and_click(950, 540)