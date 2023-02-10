# Copyright (c) 2023, GSG and contributors
# For license information, please see license.txt
import self as self

import frappe
import frappe
from frappe.model.document import Document
from frappe.utils.data import time_diff_in_hours


class Attendance(Document):
    def validate(self):
        self.get_work_hour()

    def get_work_hour(self):
        work_hours = time_diff_in_hours(self.check_out ,self. check_in )
        frappe.msgprint(str(work_hours))
        self.work_hours = work_hours


        #late_entry = frappe.db.get_single_value('Attendance Settings', 'late_entry_grace_period')
        #early_exit= frappe.db.get_single_value('Attendance Settings', 'early_exit_grace_period')
        #end_time= frappe.db.get_single_value('Attendance Settings', 'end_time')
        #start_time = frappe.db.get_single_value('Attendance Settings', 'start_time')


        #self.check_in
        #self.check_out


#         start_time + late_entry
#          end_time - early_exit


