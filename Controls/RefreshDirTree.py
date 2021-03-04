from PyQt5.QtGui import QStandardItem, QFont
from PyQt5 import QtCore
from PyQt5.QtWidgets import qApp

######################################
# Refresh or generate dir tree view
######################################


class RefreshDirTree:

    model = ''
    tokenhandler = ''

    def __init__(self, model, tokenhandler):
        self.model = model
        self.tokenhandler = tokenhandler

    def refresh_dir_tree(self):
        account = self.tokenhandler.get_account()
        account.root.refresh()
        # add father node to the tree
        itemFather = QStandardItem(account.root.name)
        fnt = QFont()
        fnt.setPointSize(10)
        fnt.setBold(True)
        itemFather.setFont(fnt)
        self.model.appendRow(itemFather)
        self.model.setItem(0, 1, QStandardItem(account.root.id))
        self.model.setItem(0, 2, QStandardItem(account.root.changekey))
        self.model.setItem(0, 3, QStandardItem(account.root.name))
        # add sub-tree of father node to the tree
        self.generate_tree_of_a_node(account.root, itemFather, account.root.name, 0)

    # add sub-tree of a node to tree
    # father = folder object of target father node
    # itemfather = QStandardItem object of target father node
    # path = path of target father node
    # j = layer number of the target father node in its own sub-tree, always 0!
    def generate_tree_of_a_node(self, father, itemfather, path, j):
        now_list = father.children  # direct children of the target father node
        # add each direct children node to the tree
        for f in now_list:
            p = path
            p = p + '/////' + f.name
            itemChildren = QStandardItem(f.name)
            fnt = QFont()
            fnt.setPointSize(10)
            fnt.setBold(False)
            itemChildren.setFont(fnt)
            if(f.unread_count != None and f.unread_count > 0):
                itemChildren.setForeground(QtCore.Qt.red)
                itemfather.setForeground(QtCore.Qt.red)
            itemfather.appendRow(itemChildren)
            itemfather.setChild(j, 1, QStandardItem(f.id))
            itemfather.setChild(j, 2, QStandardItem(f.changekey))
            itemfather.setChild(j, 3, QStandardItem(p))
            qApp.processEvents()
            # if a children has it own sub-tree too, recursive calling to draw its sub-tree
            if (len(f.children) > 0):
                fnt = QFont()
                fnt.setPointSize(10)
                fnt.setBold(True)
                itemChildren.setFont(fnt)
                self.generate_tree_of_a_node(f, itemChildren, p, 0)
            j += 1
