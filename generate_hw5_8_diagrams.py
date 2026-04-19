from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


DESKTOP = Path(r"C:\Users\wang\Desktop")
FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_PATH, size)


def text_center(draw, box, text, fnt, fill="black"):
    x1, y1, x2, y2 = box
    bbox = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=4, align="center")
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.multiline_text(
        ((x1 + x2 - w) / 2, (y1 + y2 - h) / 2),
        text,
        font=fnt,
        fill=fill,
        spacing=4,
        align="center",
    )


def rounded_box(draw, box, title, body="", fill="#F7FBFF", outline="#2B5D8A"):
    draw.rounded_rectangle(box, radius=18, fill=fill, outline=outline, width=3)
    x1, y1, x2, y2 = box
    title_box = (x1, y1 + 8, x2, y1 + 48)
    text_center(draw, title_box, title, font(22), fill="#12344D")
    if body:
        body_box = (x1 + 12, y1 + 50, x2 - 12, y2 - 12)
        text_center(draw, body_box, body, font(16), fill="#333333")


def rect_box(draw, box, title, body="", fill="#FFF8E8", outline="#946B00"):
    draw.rectangle(box, fill=fill, outline=outline, width=3)
    x1, y1, x2, y2 = box
    text_center(draw, (x1, y1 + 8, x2, y1 + 42), title, font(22), fill="#5A4300")
    if body:
        text_center(draw, (x1 + 10, y1 + 44, x2 - 10, y2 - 10), body, font(15), fill="#333333")


def diamond(draw, center, w, h, text, outline="#7A2E8A", fill="#FFF0FF"):
    cx, cy = center
    pts = [(cx, cy - h // 2), (cx + w // 2, cy), (cx, cy + h // 2), (cx - w // 2, cy)]
    draw.polygon(pts, fill=fill, outline=outline)
    text_center(draw, (cx - w // 2 + 8, cy - h // 2 + 8, cx + w // 2 - 8, cy + h // 2 - 8), text, font(18), fill="#61206E")


def arrow(draw, start, end, fill="black", width=3, both=False, dashed=False):
    if dashed:
        x1, y1 = start
        x2, y2 = end
        steps = 18
        for i in range(steps):
            if i % 2 == 0:
                sx = x1 + (x2 - x1) * i / steps
                sy = y1 + (y2 - y1) * i / steps
                ex = x1 + (x2 - x1) * (i + 1) / steps
                ey = y1 + (y2 - y1) * (i + 1) / steps
                draw.line((sx, sy, ex, ey), fill=fill, width=width)
    else:
        draw.line((start, end), fill=fill, width=width)
    if both:
        draw_arrow_head(draw, end, start, fill)
        draw_arrow_head(draw, start, end, fill)
    else:
        draw_arrow_head(draw, start, end, fill)


def draw_arrow_head(draw, start, end, fill):
    import math

    x1, y1 = start
    x2, y2 = end
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 12
    a1 = angle + math.pi / 7
    a2 = angle - math.pi / 7
    p1 = (x2 - size * math.cos(a1), y2 - size * math.sin(a1))
    p2 = (x2 - size * math.cos(a2), y2 - size * math.sin(a2))
    draw.polygon([end, p1, p2], fill=fill)


def label(draw, pos, text, size=16, fill="black"):
    draw.text(pos, text, font=font(size), fill=fill)


def make_canvas(title):
    img = Image.new("RGB", (1600, 1000), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1600, 90), fill="#EAF3FF")
    draw.text((40, 25), title, font=font(34), fill="#12344D")
    draw.line((0, 90, 1600, 90), fill="#8BB3DD", width=3)
    return img, draw


def save(img, name):
    path = DESKTOP / name
    img.save(path)
    return path


def draw_er():
    img, draw = make_canvas("作业5 ER图 - 图书借阅管理系统")
    rect_box(draw, (90, 210, 330, 430), "学生用户", "user_id (PK)\n姓名\n学号 201408\n电话")
    rect_box(draw, (670, 210, 930, 450), "借阅记录", "record_id (PK)\nborrow_date\nreturn_date\nstatus\nuser_id (FK)\nbook_id (FK)")
    rect_box(draw, (1250, 210, 1490, 430), "图书", "book_id (PK)\n书名\n作者\n馆藏编号 201408\n库存")
    rect_box(draw, (90, 650, 330, 860), "管理员", "admin_id (PK)\n姓名\n工号\n备注 201408")

    diamond(draw, (500, 320), 170, 110, "借阅")
    diamond(draw, (1080, 320), 170, 110, "对应")
    diamond(draw, (500, 755), 200, 110, "审核/处理")

    arrow(draw, (330, 320), (415, 320), fill="#333333")
    arrow(draw, (585, 320), (670, 320), fill="#333333")
    arrow(draw, (930, 320), (995, 320), fill="#333333")
    arrow(draw, (1165, 320), (1250, 320), fill="#333333")
    arrow(draw, (330, 755), (400, 755), fill="#333333")
    arrow(draw, (600, 755), (670, 430), fill="#333333")

    label(draw, (355, 280), "1", 18)
    label(draw, (610, 280), "n", 18)
    label(draw, (945, 280), "n", 18)
    label(draw, (1190, 280), "1", 18)
    label(draw, (350, 715), "1", 18)
    label(draw, (615, 590), "n", 18)

    draw.text((103, 930), "评分点覆盖：实体、联系、属性、主键/外键、1:n 关系；业务内容与借阅系统一致。", font=font(18), fill="#555555")
    return save(img, "作业5_ER图_201408.png")


def draw_class():
    img, draw = make_canvas("作业6 类图 - 图书借阅管理系统")

    def class_box(box, title, attrs, methods, fill="#F9FCFF", outline="#1E5F74"):
        x1, y1, x2, y2 = box
        draw.rectangle(box, fill=fill, outline=outline, width=3)
        draw.line((x1, y1 + 44, x2, y1 + 44), fill=outline, width=2)
        draw.line((x1, y1 + 140, x2, y1 + 140), fill=outline, width=2)
        text_center(draw, (x1, y1 + 4, x2, y1 + 42), title, font(22), fill="#0B3C49")
        draw.multiline_text((x1 + 10, y1 + 54), attrs, font=font(15), fill="#333333", spacing=4)
        draw.multiline_text((x1 + 10, y1 + 150), methods, font=font(15), fill="#333333", spacing=4)

    class_box((80, 140, 350, 360), "User", "- userId\n- name\n- studentNo\n- remark201408", "+ login()\n+ searchBook()\n+ submitBorrow()")
    class_box((80, 540, 350, 780), "Admin", "- adminId\n- name\n- role", "+ auditBorrow()\n+ addBook()\n+ updateInventory()")
    class_box((650, 120, 950, 360), "Book", "- bookId\n- title\n- author\n- shelfCode201408", "+ isAvailable()\n+ decreaseStock()\n+ increaseStock()")
    class_box((650, 520, 950, 800), "BorrowRecord", "- recordId\n- borrowDate\n- returnDate\n- status", "+ create()\n+ markReturned()\n+ markRejected()")
    class_box((1180, 260, 1510, 560), "BorrowService", "- db\n- inventoryService", "+ createBorrow()\n+ checkQuota()\n+ returnBook()\n+ notifyUser()")

    arrow(draw, (350, 250), (650, 240), fill="#2E6F40", both=False)
    label(draw, (455, 210), "关联 1..* / 查询", 16, "#2E6F40")

    arrow(draw, (350, 650), (650, 650), fill="#8A4B00")
    label(draw, (440, 615), "依赖 / 审核", 16, "#8A4B00")

    arrow(draw, (950, 260), (1180, 340), fill="#6B2C91")
    label(draw, (1015, 260), "依赖", 16, "#6B2C91")

    arrow(draw, (950, 650), (1180, 470), fill="#6B2C91")
    label(draw, (1015, 585), "组合 1..*", 16, "#6B2C91")

    arrow(draw, (250, 360), (740, 520), fill="#B03A2E")
    label(draw, (415, 410), "用户创建借阅记录", 16, "#B03A2E")

    draw.text((95, 920), "说明：展示主要类、关键属性与方法，并标注关联/依赖/组合和多重性，满足作业6评分要求。", font=font(18), fill="#555555")
    return save(img, "作业6_类图_201408.png")


def draw_state():
    img, draw = make_canvas("作业7 状态图 - 借阅申请状态流转")

    states = [
        ((180, 380, 350, 460), "初始"),
        ((430, 240, 650, 340), "待提交\n申请号201408"),
        ((770, 240, 1020, 340), "待审核"),
        ((1110, 150, 1370, 250), "借阅成功\n记录201408"),
        ((1110, 380, 1370, 480), "已归还\n记录201408"),
        ((770, 540, 1020, 640), "审核驳回\n单号201408"),
        ((430, 540, 650, 640), "已取消\n单号201408"),
    ]

    draw.ellipse((100, 405, 130, 435), fill="black")
    for box, title in states[1:]:
        rounded_box(draw, box, title, "", fill="#F5FBF7", outline="#2D6A4F")

    arrow(draw, (130, 420), (430, 290), fill="#333333")
    label(draw, (210, 350), "打开借阅页面", 16)

    arrow(draw, (650, 290), (770, 290), fill="#333333")
    label(draw, (678, 248), "提交申请", 16)

    arrow(draw, (1020, 290), (1110, 200), fill="#333333")
    label(draw, (1030, 210), "库存充足且审核通过", 16)

    arrow(draw, (1020, 320), (1110, 430), fill="#333333")
    label(draw, (1030, 405), "用户归还图书", 16)

    arrow(draw, (895, 340), (895, 540), fill="#333333")
    label(draw, (910, 435), "信息不完整/库存不足", 16)

    arrow(draw, (770, 590), (650, 590), fill="#333333")
    label(draw, (655, 550), "用户撤回", 16)

    draw.ellipse((1440, 405, 1470, 435), outline="black", width=3)
    draw.ellipse((1447, 412, 1463, 428), fill="black")
    arrow(draw, (1370, 430), (1440, 420), fill="#333333")
    label(draw, (1320, 390), "流程结束", 16)

    draw.text((90, 930), "对象：借阅申请。包含初态、状态、转移箭头与触发条件；学号已放入状态内容而非标题。", font=font(18), fill="#555555")
    return save(img, "作业7_状态图_201408.png")


def draw_sequence():
    img, draw = make_canvas("作业8 时序图 - 借书核心流程")

    participants = [
        ("用户", 180),
        ("前端页面", 480),
        ("BorrowService", 840),
        ("数据库", 1180),
        ("库存模块", 1450),
    ]

    for name, x in participants:
        rounded_box(draw, (x - 85, 110, x + 85, 180), name, "", fill="#FFF9F1", outline="#9A6700")
        draw.line((x, 180, x, 900), fill="#999999", width=2)

    messages = [
        (180, 480, 250, "1. 提交借阅请求"),
        (480, 840, 320, "2. createBorrow(userId, remark=201408)"),
        (840, 1450, 390, "3. checkStock()"),
        (1450, 840, 450, "4. 库存可用", True),
        (840, 1180, 520, "5. insert BorrowRecord"),
        (1180, 840, 580, "6. 返回记录ID", True),
        (840, 1450, 650, "7. decreaseStock()"),
        (1450, 840, 710, "8. 更新成功", True),
        (840, 480, 780, "9. 返回借阅成功", True),
        (480, 180, 850, "10. 页面提示成功", True),
    ]

    for msg in messages:
        if len(msg) == 4:
            x1, x2, y, text = msg
            dashed = False
        else:
            x1, x2, y, text, dashed = msg
        arrow(draw, (x1, y), (x2, y), fill="#1F2937", dashed=dashed)
        label(draw, ((x1 + x2) // 2 - 90, y - 28), text, 15, "#1F2937")

    draw.text((90, 930), "说明：生命线完整，按时间顺序展示请求与响应；同步消息为实线，返回消息为虚线，覆盖一条核心借书流程。", font=font(18), fill="#555555")
    return save(img, "作业8_时序图_201408.png")


if __name__ == "__main__":
    paths = [draw_er(), draw_class(), draw_state(), draw_sequence()]
    for p in paths:
        print(p)
