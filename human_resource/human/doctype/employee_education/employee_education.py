# Copyright (c) 2023, GSG and contributors
# For license information, please see license.txt
import datetime

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

# test
def get_today():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return today


class EmployeeEducation(Document):
    def get_age(self):
        if self.date_of_birth < get_today():
            self.age = int((getdate(get_today()) - getdate(self.date_of_birth)).day / 356)
        else:
            frappe.throw("the dob can not be set as today date")

    def validate_age(self):
        if self.age >= 60 and self.status == "Active":
            frappe.throw("Age should be less than 60")

    def validate_mobile(self):
        if len(self.mobile) == 10:
            if self.mobile.startwith('05'):
                pass
            else:
                frappe.throw("mobile num should start with 05")
        else:
            frappe.throw("mobile number should be 10 digital num")
