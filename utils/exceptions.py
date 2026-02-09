class NoManageRoles(Exception):
    def __init__(self):
        self.message = "No \"Manage Roles\" permission"
        super().__init__(self.message)