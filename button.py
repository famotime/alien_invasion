import pygame.font


class Button():
    def __init__(self, ai_settings, screen, msg):
        """初始化按钮属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (79,195,247)
        self.text_color = (255, 255, 255)
        # 使用默认字体，48号大小
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮(带标签的实心矩形)并居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # 按钮的文本只需创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将msg文本渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)    # True表示开启反锯齿
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
