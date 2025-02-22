from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QSplitter, QTreeWidget,
    QTreeWidgetItem, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from .ui_components import UIComponents
from .category_handlers import CategoryHandlers
from .data_handlers import DataHandlers
from .group_handlers import GroupHandlers
from .tab_handlers import TabHandlers

class InitialSetupBase(QWidget, CategoryHandlers, DataHandlers, GroupHandlers, TabHandlers):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.group_categories = {}
        self.setup_ui()
        self.setup_initial_data()
        self.group_list.itemSelectionChanged.connect(self.on_group_selection_changed)

    def setup_ui(self):
        """UIの初期化"""
        main_layout = QVBoxLayout(self)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左側のパネル（グループリスト）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        group_label = QLabel("グループ")
        left_layout.addWidget(group_label)
        
        self.group_list = QListWidget()
        left_layout.addWidget(self.group_list)
        
        group_buttons = QHBoxLayout()
        add_group_btn = QPushButton("追加")
        edit_group_btn = QPushButton("編集")
        delete_group_btn = QPushButton("削除")
        
        add_group_btn.clicked.connect(self.add_group)
        edit_group_btn.clicked.connect(self.edit_group)
        delete_group_btn.clicked.connect(self.delete_group)
        
        group_buttons.addWidget(add_group_btn)
        group_buttons.addWidget(edit_group_btn)
        group_buttons.addWidget(delete_group_btn)
        left_layout.addLayout(group_buttons)
        
        splitter.addWidget(left_panel)
        
        # 右側のパネル（カテゴリーツリー）
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        category_label = QLabel("カテゴリー")
        right_layout.addWidget(category_label)
        
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabel("カテゴリーとスキル")
        right_layout.addWidget(self.category_tree)
        
        category_buttons = QHBoxLayout()
        add_category_btn = QPushButton("カテゴリー追加")
        add_skill_btn = QPushButton("スキル追加")
        edit_item_btn = QPushButton("編集")
        delete_item_btn = QPushButton("削除")
        
        add_category_btn.clicked.connect(self.add_category)
        add_skill_btn.clicked.connect(self.add_skill)
        edit_item_btn.clicked.connect(self.edit_item)
        delete_item_btn.clicked.connect(self.delete_item)
        
        category_buttons.addWidget(add_category_btn)
        category_buttons.addWidget(add_skill_btn)
        category_buttons.addWidget(edit_item_btn)
        category_buttons.addWidget(delete_item_btn)
        right_layout.addLayout(category_buttons)
        
        # UIコンポーネント（新規タブ追加ボタン）をカテゴリーパネルの最下部に追加
        self.ui_components = UIComponents(self.main_window)  # MainWindowを渡す
        right_layout.addWidget(self.ui_components.widget)
        
        splitter.addWidget(right_panel)
        
        # スプリッターの初期サイズ比を設定
        splitter.setSizes([200, 400])

    def check_group_selected(self):
        if not self.group_list.currentItem():
            QMessageBox.warning(self, "警告", "グループを選択してください。")
            return False
        return True

    def on_group_selection_changed(self):
        current_group = self.group_list.currentItem()
        if current_group:
            group_name = current_group.text()
            self.filter_categories(group_name)
    
    # 以下のメソッドは initial_setup.py からの移行
    def connect_signals(self):
        """シグナルの接続"""
        if self.main_window:
            self.group_list.currentItemChanged.connect(self.on_group_selected)
            self.category_tree.itemClicked.connect(self.on_category_tree_item_clicked)

    def on_group_selected(self, current, previous):
        """グループ選択時の処理"""
        if current and self.main_window:
            group_name = current.text()
            index = self.main_window.group_combo.findText(group_name)
            if index >= 0:
                self.main_window.group_combo.setCurrentIndex(index)

    def on_category_tree_item_clicked(self, item, column):
        """カテゴリー・スキルツリーアイテムクリック時の処理"""
        if item and self.main_window:
            self.main_window.on_category_tree_item_clicked(item)

    def update_category_tree(self, group_id, user_id=None):
        """カテゴリー・スキルツリーの更新"""
        if not self.main_window:
            return

        # UIアダプターを使用してツリーを更新
        self.main_window.ui_adapter.update_category_tree(
            self.category_tree,
            group_id,
            user_id
        )

    def update_group_list(self, groups):
        """グループリストの更新"""
        self.group_list.clear()
        for group in groups.values():
            self.group_list.addItem(group["name"])