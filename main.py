import pygame
import sys
import random
import os

pygame.init()

# ---------- 配置 ----------
# 请确认你的字体文件名和扩展名正确
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILENAME = "FangZhengKaiTiJianTi-1.ttf"   # ← 根据实际修改
FONT_PATH = os.path.join(BASE_DIR, FONT_FILENAME)

IS_ANDROID = "ANDROID_ARGUMENT" in os.environ or "ANDROID_PRIVATE" in os.environ

if IS_ANDROID:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    INIT_WIDTH, INIT_HEIGHT = 360, 640
    screen = pygame.display.set_mode((INIT_WIDTH, INIT_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("加减法计算游戏")
clock = pygame.time.Clock()

# ---------- 颜色 ----------
BG_COLOR = (30, 30, 30)
KEY_COLOR = (70, 130, 180)
KEY_HOVER = (100, 160, 210)
KEY_TEXT_COLOR = (255, 255, 255)
ERROR_COLOR = (255, 80, 80)
SCORE_COLOR = (255, 215, 0)
WRONG_BUTTON_COLOR = (200, 100, 100)
SOLVED_COLOR = (100, 255, 100)

# ---------- 自适应字体加载 ----------
def get_font(size):
    if os.path.exists(FONT_PATH):
        try:
            return pygame.font.Font(FONT_PATH, size)
        except:
            pass
    try:
        return pygame.font.Font(None, size)
    except:
        return pygame.font.SysFont("Arial", size)

# ---------- 游戏状态 ----------
score = 0
wrong_list = []
current_input = ""
current_num1 = 0
current_num2 = 0
current_op = '+'
feedback_text = ""
feedback_timer = 0
show_wrong_book = False
scroll_offset = 0

# ---------- 生成新题 ----------
def generate_question():
    global current_num1, current_num2, current_op, current_input, feedback_text, feedback_timer
    op = random.choice(['+', '-'])
    if op == '+':
        a = random.randint(1, 99)
        b = random.randint(1, 100 - a)
    else:
        a = random.randint(1, 100)
        b = random.randint(1, a)
    current_num1, current_num2, current_op = a, b, op
    current_input = ""
    feedback_text = ""
    feedback_timer = 0

# ---------- 检查答案 ----------
def check_answer():
    global score, feedback_text, feedback_timer, wrong_list, current_input
    if current_input == "":
        return
    user_ans = int(current_input)
    correct = current_num1 + current_num2 if current_op == '+' else current_num1 - current_num2

    if user_ans == correct:
        score += 10
        feedback_text = "✓ 正确！"
        feedback_timer = 90

        question_str = f"{current_num1} {current_op} {current_num2} = ?"
        for record in wrong_list:
            if record['question'] == question_str and not record['solved']:
                record['correct_ans'] = correct
                record['solved'] = True

        generate_question()
    else:
        question_str = f"{current_num1} {current_op} {current_num2} = ?"
        wrong_list.append({
            'question': question_str,
            'wrong_ans': user_ans,
            'correct_ans': correct,
            'solved': False
        })
        feedback_text = "✗ 答错了，再试一次"
        feedback_timer = 90
        current_input = ""

# ---------- 绘制界面（★ 修改：返回 line_height） ----------
def draw_ui(surface):
    w, h = surface.get_size()
    base_font_size = max(14, min(w, h) // 18)
    large_font_size = int(base_font_size * 2.5)
    mid_font_size = int(base_font_size * 1.5)
    small_font_size = int(base_font_size * 0.8)

    font_large = get_font(large_font_size)
    font_mid = get_font(mid_font_size)
    font_small = get_font(small_font_size)

    surface.fill(BG_COLOR)

    # 积分
    score_surf = font_small.render(f"积分: {score}", True, SCORE_COLOR)
    score_rect = score_surf.get_rect(topleft=(10, 10))
    surface.blit(score_surf, score_rect)

    # 错题本按钮
    btn_wrong = pygame.Rect(0, 0, w // 5, h // 15)
    btn_wrong.topright = (w - 10, 10)
    pygame.draw.rect(surface, (150, 50, 50), btn_wrong, border_radius=5)
    btn_text = font_small.render("错题本", True, (255, 255, 255))
    btn_text_rect = btn_text.get_rect(center=btn_wrong.center)
    surface.blit(btn_text, btn_text_rect)

    # 算式
    question_str = f"{current_num1} {current_op} {current_num2} = ?"
    q_surf = font_large.render(question_str, True, (255, 255, 255))
    q_rect = q_surf.get_rect(center=(w // 2, h // 5))
    surface.blit(q_surf, q_rect)

    input_display = current_input if current_input else "_"
    inp_surf = font_large.render(input_display, True, (200, 200, 200))
    inp_rect = inp_surf.get_rect(center=(w // 2, h // 5 + large_font_size + 10))
    surface.blit(inp_surf, inp_rect)

    if feedback_timer > 0:
        fb_surf = font_mid.render(feedback_text, True,
                                  (100, 255, 100) if "正确" in feedback_text else ERROR_COLOR)
        fb_rect = fb_surf.get_rect(center=(w // 2, inp_rect.bottom + mid_font_size))
        surface.blit(fb_surf, fb_rect)

    # 数字键盘
    keyboard_top = h // 2
    keyboard_height = h - keyboard_top - 10
    cols, rows = 3, 4
    btn_margin = 5
    btn_width = (w - (cols + 1) * btn_margin) // cols
    btn_height = (keyboard_height - (rows + 1) * btn_margin) // rows

    buttons = []
    for i in range(1, 10):
        r = (i - 1) // 3
        c = (i - 1) % 3
        x = btn_margin + c * (btn_width + btn_margin)
        y = keyboard_top + btn_margin + r * (btn_height + btn_margin)
        buttons.append((str(i), pygame.Rect(x, y, btn_width, btn_height)))

    r = 3
    buttons.append(("←", pygame.Rect(btn_margin, keyboard_top + btn_margin + r * (btn_height + btn_margin), btn_width, btn_height)))
    buttons.append(("0", pygame.Rect(btn_margin + (btn_width + btn_margin), keyboard_top + btn_margin + r * (btn_height + btn_margin), btn_width, btn_height)))
    buttons.append(("=", pygame.Rect(btn_margin + 2 * (btn_width + btn_margin), keyboard_top + btn_margin + r * (btn_height + btn_margin), btn_width, btn_height)))

    mouse_pos = pygame.mouse.get_pos()
    for text, rect in buttons:
        color = KEY_HOVER if rect.collidepoint(mouse_pos) else KEY_COLOR
        pygame.draw.rect(surface, color, rect, border_radius=8)
        txt_surf = font_mid.render(text, True, KEY_TEXT_COLOR)
        txt_rect = txt_surf.get_rect(center=rect.center)
        surface.blit(txt_surf, txt_rect)

    # 错题本覆盖层
    close_btn = None
    list_area = None
    # ★ 先定义 line_height 默认值，防止未赋值
    line_height = small_font_size + 10

    if show_wrong_book:
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        book_width = int(w * 0.85)
        book_height = int(h * 0.7)
        book_rect = pygame.Rect((w - book_width)//2, (h - book_height)//2, book_width, book_height)
        pygame.draw.rect(surface, (50, 50, 70), book_rect, border_radius=10)
        pygame.draw.rect(surface, (120, 120, 140), book_rect, 3, border_radius=10)

        title_surf = font_mid.render("错题本", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(book_rect.centerx, book_rect.top + mid_font_size))
        surface.blit(title_surf, title_rect)

        list_area = pygame.Rect(book_rect.left + 10, book_rect.top + 2*mid_font_size + 10,
                                book_width - 20, book_height - 3*mid_font_size - 20)
        surface.set_clip(list_area)
        start_y = list_area.top - scroll_offset
        for i, record in enumerate(wrong_list):
            y = start_y + i * line_height
            if y + line_height < list_area.top or y > list_area.bottom:
                continue

            question = record['question']
            wrong = record['wrong_ans']
            if record['solved']:
                correct = record['correct_ans']
                line = f"{question} 你答了 {wrong} → 已解决 (正确 {correct})"
                color = SOLVED_COLOR
            else:
                line = f"{question} 你答了 {wrong}"
                color = ERROR_COLOR

            line_surf = font_small.render(line, True, color)
            surface.blit(line_surf, (list_area.left, y))
        surface.set_clip(None)

        if len(wrong_list) * line_height > list_area.height:
            hint = font_small.render("上下滑动查看", True, (180, 180, 180))
            hint_rect = hint.get_rect(center=(book_rect.centerx, book_rect.bottom - small_font_size))
            surface.blit(hint, hint_rect)

        close_btn = pygame.Rect(book_rect.right - 40, book_rect.top + 5, 30, 30)
        pygame.draw.rect(surface, (200, 100, 100), close_btn, border_radius=5)
        close_x = font_small.render("X", True, (255, 255, 255))
        close_rect = close_x.get_rect(center=close_btn.center)
        surface.blit(close_x, close_rect)

    # ★ 返回 line_height
    return buttons, btn_wrong, close_btn, list_area, line_height

# ---------- 主循环 ----------
running = True
generate_question()
last_touch_pos = None

while running:
    dt = clock.tick(60)
    if feedback_timer > 0:
        feedback_timer -= 1
        if feedback_timer == 0:
            feedback_text = ""

    # ★ 接收 line_height
    buttons, wrong_btn, close_btn, list_area, line_height = draw_ui(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            if not IS_ANDROID:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if show_wrong_book:
                if close_btn and close_btn.collidepoint(pos):
                    show_wrong_book = False
                    scroll_offset = 0
                elif list_area and list_area.collidepoint(pos):
                    last_touch_pos = pos
                else:
                    last_touch_pos = None
            else:
                if wrong_btn.collidepoint(pos):
                    show_wrong_book = True
                    scroll_offset = 0
                for text, rect in buttons:
                    if rect.collidepoint(pos):
                        if text == "=":
                            check_answer()
                        elif text == "←":
                            current_input = current_input[:-1]
                        else:
                            if len(current_input) < 3:
                                current_input += text
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            last_touch_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if show_wrong_book and last_touch_pos and list_area:
                dy = event.pos[1] - last_touch_pos[1]
                # ★ 使用返回的 line_height
                max_scroll = max(0, len(wrong_list) * line_height - list_area.height)
                scroll_offset = max(0, min(scroll_offset - dy, max_scroll))
                last_touch_pos = event.pos

    pygame.display.flip()

pygame.quit()
sys.exit()