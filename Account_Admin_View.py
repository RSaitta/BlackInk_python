import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList, ControlButton
from Account_View import UserWidget
from DB_Actions import pull_users


class AdminWidget(BaseWidget):
    def __init__(self, user=None, connection=None):
        BaseWidget.__init__(self)
        self._admin = user
        self._connection = connection

        self._userList = ControlList('Users',select_entire_row=True)
        self._userList.readonly=True
        self._userList.cell_double_clicked_event = self.__onSelect
        self._userList.horizontal_headers=['Name', 'Email']
        self._user_pull= pull_users(self._admin, self._connection)
        if self._user_pull!=[]:
            for i in self._user_pull:
                self._userList.__add__([self._user_pull[i]['name'], self._user_pull[i]['email']])

    def __onSelect(self, row, column):
        if self.parent!=None: self.parent.persist_login()
        name = self._userList.get_value(0, row)
        email  = self._userList.get_value(1, row)
        for i in self._user_pull:
            if self._user_pull[i]['email'] == email:
                permissions= self._user_pull[i]['permissions']
                services = self._user_pull[i]['services']
        win = UserWidget(self._admin, self._connection, email, name, permissions, services)
        win.parent = self
        win.show()

if __name__== "__main__":
    pyforms.start_app(AdminWidget, geometry=(400, 400, 600, 600))
