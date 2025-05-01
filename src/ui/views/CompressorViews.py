from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QTableView, QPushButton


class TableModel(QAbstractTableModel):

    def __init__(self, data=None, headers=None, parent=None):
        super().__init__(parent)
        self._data = data or []  # 数据列表，默认为空
        self._headers = headers or ["ID", "文件名", "文件大小", "文件路径", "输出路径"]  # 表头

    def rowCount(self, parent=None):
        """返回行数"""
        return len(self._data)

    def columnCount(self, parent=None):
        """返回列数"""
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        """返回指定索引处的数据"""
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            # 返回显示数据
            return self._data[row][col]
        elif role == Qt.EditRole:
            # 返回编辑数据
            return self._data[row][col]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """返回表头数据"""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)  # 显示行号
        return None

    def setData(self, index, value, role=Qt.EditRole):
        """设置指定索引处的数据"""
        if index.isValid() and role == Qt.EditRole:
            row = index.row()
            col = index.column()
            self._data[row][col] = value
            self.dataChanged.emit(index, index)  # 通知视图更新
            return True
        return False

    def flags(self, index):
        """设置单元格的标志位（如是否可编辑）"""
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def insertRows(self, position, rows, parent=Qt.QModelIndex()):
        """插入行"""
        self.beginInsertRows(parent, position, position + rows - 1)
        for _ in range(rows):
            self._data.insert(position, [""] * self.columnCount())
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=Qt.QModelIndex()):
        """删除行"""
        self.beginRemoveRows(parent, position, position + rows - 1)
        for _ in range(rows):
            del self._data[position]
        self.endRemoveRows()
        return True


class CompressorViews(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.header = ["ID", "文件名", "文件大小", "文件路径", "输出路径"]
        self.table = QTableView(self)
        self.setLayout(self.layout)
        self.setup_ui()

    def setup_ui(self):
        button = QPushButton("添加行")
        button = QPushButton("删除行")



if __name__ == "__main__":
    app = QApplication([])

    window = CompressorViews()
    window.show()
    window.resize(800, 600)
    app.exec()
