from PySide6.QtWidgets import (QPushButton, QStyle, QStyleOptionButton)
from PySide6.QtGui import QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QSize, Signal, Property, QPropertyAnimation, QEasingCurve


class SettingsButton(QPushButton):
    """可复用的设置按钮组件"""

    clickedWithData = Signal(object)  # 带额外数据的点击信号

    def __init__(self, parent=None):
        super().__init__(parent)

        # 默认设置
        self._icon_size = QSize(24, 24)
        self._hover_color = QColor(240, 240, 240)
        self._press_color = QColor(220, 220, 220)
        self._icon_color = QColor(100, 100, 100)
        self._animation_duration = 150
        self._corner_radius = 4
        self._show_menu_indicator = True
        self._rotate_angle = 0  # 用于旋转动画

        # 初始化UI
        self._setup_ui()

    def _setup_ui(self):
        """初始化UI设置"""
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        self.setIconSize(self._icon_size)

        # 默认图标（可以使用setIcon方法覆盖）
        self.setIcon(QIcon.fromTheme("preferences-system"))

        # 设置菜单指示器
        self._update_menu_indicator()

    def setMenu(self, menu):
        """设置关联菜单"""
        super().setMenu(menu)
        self._update_menu_indicator()

    def _update_menu_indicator(self):
        """更新菜单指示器状态"""
        if self.menu() and self._show_menu_indicator:
            self.setStyleSheet("""
                QPushButton::menu-indicator {
                    image: none;
                    width: 0;
                    height: 0;
                }
            """)
        else:
            self.setStyleSheet("")

    def setIconColor(self, color):
        """设置图标颜色"""
        self._icon_color = color
        self.update()

    def getIconColor(self):
        """获取图标颜色"""
        return self._icon_color

    iconColor = Property(QColor, getIconColor, setIconColor)

    def setHoverColor(self, color):
        """设置悬停颜色"""
        self._hover_color = color
        self.update()

    def setPressColor(self, color):
        """设置按下颜色"""
        self._press_color = color
        self.update()

    def setCornerRadius(self, radius):
        """设置圆角半径"""
        self._corner_radius = radius
        self.update()

    def setShowMenuIndicator(self, show):
        """设置是否显示菜单指示器"""
        self._show_menu_indicator = show
        self._update_menu_indicator()

    def setAnimationDuration(self, duration):
        """设置动画持续时间(毫秒)"""
        self._animation_duration = duration

    def paintEvent(self, event):
        """自定义绘制按钮"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        opt = QStyleOptionButton()
        self.initStyleOption(opt)

        rect = opt.rect
        if opt.state & QStyle.State_MouseOver:
            painter.setBrush(self._hover_color)
        elif opt.state & QStyle.State_Sunken:
            painter.setBrush(self._press_color)
        else:
            painter.setBrush(Qt.NoBrush)

        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, self._corner_radius, self._corner_radius)

        # 绘制图标（带旋转效果）
        if not self.icon().isNull():
            icon_rect = QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.iconSize(),
                rect
            )

            painter.save()
            painter.translate(icon_rect.center())
            painter.rotate(self._rotate_angle)
            painter.translate(-icon_rect.center())

            mode = QIcon.Normal
            if not self.isEnabled():
                mode = QIcon.Disabled
            elif opt.state & QStyle.State_Sunken:
                mode = QIcon.Active

            self.icon().paint(
                painter,
                icon_rect,
                Qt.AlignCenter,
                mode,
                QIcon.On if self.isChecked() else QIcon.Off
            )
            painter.restore()

        # 绘制文本
        if self.text():  # 修改此处：使用 Python 的标准方式判断字符串是否为空
            text_rect = rect.adjusted(
                self.iconSize().width() + 6, 0,
                -self._corner_radius, 0
            )
            painter.setPen(QColor(self._icon_color))
            painter.drawText(
                text_rect,
                Qt.AlignLeft | Qt.AlignVCenter,
                self.text()
            )

    def enterEvent(self, event):
        """鼠标进入事件"""
        self._start_hover_animation(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开事件"""
        self._start_hover_animation(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self._start_press_animation()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self._start_release_animation()
            if self.rect().contains(event.pos()):
                self.clickedWithData.emit(self.property("userData"))
        super().mouseReleaseEvent(event)

    def _start_hover_animation(self, hover):
        """开始悬停动画"""
        anim = QPropertyAnimation(self, b"iconColor")
        anim.setDuration(self._animation_duration)
        anim.setEasingCurve(QEasingCurve.OutQuad)

        if hover:
            anim.setStartValue(self._icon_color)
            anim.setEndValue(QColor(70, 70, 70))
        else:
            anim.setStartValue(QColor(70, 70, 70))
            anim.setEndValue(self._icon_color)

        anim.start()

    def _start_press_animation(self):
        """开始按下动画"""
        # 旋转动画
        anim = QPropertyAnimation(self, b"_rotate_angle")
        anim.setDuration(self._animation_duration * 2)
        anim.setEasingCurve(QEasingCurve.OutBack)
        anim.setStartValue(self._rotate_angle)
        anim.setEndValue(self._rotate_angle + 90)
        anim.start()

        # 颜色动画
        color_anim = QPropertyAnimation(self, b"iconColor")
        color_anim.setDuration(self._animation_duration)
        color_anim.setEasingCurve(QEasingCurve.OutQuad)
        color_anim.setStartValue(self._icon_color)
        color_anim.setEndValue(QColor(40, 40, 40))
        color_anim.start()

    def _start_release_animation(self):
        """开始释放动画"""
        color_anim = QPropertyAnimation(self, b"iconColor")
        color_anim.setDuration(self._animation_duration)
        color_anim.setEasingCurve(QEasingCurve.OutQuad)
        color_anim.setStartValue(QColor(40, 40, 40))
        color_anim.setEndValue(self._icon_color)
        color_anim.start()

    def sizeHint(self):
        """计算合适的尺寸"""
        hint = super().sizeHint()
        if len(self.text()) > 0:  # 使用 len() 判断字符串是否为空
            hint.setWidth(hint.width() + self.iconSize().width() + 6)
        return hint


    def setUserData(self, data):
        """设置用户数据"""
        self.setProperty("userData", data)

    def getUserData(self):
        """获取用户数据"""
        return self.property("userData")