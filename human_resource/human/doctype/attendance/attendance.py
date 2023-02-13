# Copyright (c) 2023, GSG and contributors
# For license information, please see license.txt
from datetime import timedelta, datetime

import frappe
from frappe.model.document import Document
from frappe.utils.data import time_diff_in_hours


class Attendance(Document):
    def validate(self):
        self.get_work_hour()
        self.get_late_hours()
        self.update_status()

    def get_work_hour(self, check_in=None, check_out=None):
        work_hours = time_diff_in_hours(self.check_out, self. check_in)
        frappe.msgprint(str(work_hours))
        self.work_hours = work_hours

        late_entry = frappe.db.get_single_value('Attendance Settings', 'late_entry_grace_period')
        early_exit = frappe.db.get_single_value('Attendance Settings', 'early_exit_grace_period')
        end_time = frappe.db.get_single_value('Attendance Settings', 'end_time')
        start_time = frappe.db.get_single_value('Attendance Settings', 'start_time')

        start_time_with_late_entry = start_time + timedelta(minutes=late_entry)
        end_time_with_early_exit= end_time - timedelta(minutes=early_exit)

        total_start_time = datetime.strptime(str(start_time_with_late_entry), "%H:%M:%S")

        total_end_time = datetime.strptime(str(end_time_with_early_exit), "%H:%M:%S")

        if check_in <= total_start_time:
            check_in = datetime.strptime(str(start_time), "%H:%M:%S")

        else:
            check_in = check_in - timedelta(minutes=late_entry)


        if check_out >= total_end_time:
            check_out = datetime.strptime(str(end_time), "%H:%M:%S")
        else:

            check_out = check_out - timedelta(minutes=early_exit)


        check_sum = check_out - check_in
        second = check_sum.total_seconds()
        work_hours = second / (60*60)
        self.work_hours = work_hours


    def get_late_hours(self):
        end_time = frappe.db.get_single_value('Attendance Settings', 'end_time')
        start_time = frappe.db.get_single_value('Attendance Settings', 'start_time')

        start_time = datetime.strptime(start_time, "%H:%M:%S")
        end_time = datetime.strptime(end_time, "%H:%M:%S")

        sum_working_hours_threshold = end_time - start_time
        second = sum_working_hours_threshold.total_seconds()
        working_hours_threshold = second / (60*60)
        self.late_hours = working_hours_threshold - self.work_hours


    def update_status(self):
        working_hours_threshold_for_absent = frappe.db.get_single_value('Attendance Settings', 'working_hours_threshold_for_absent')

        if self.late_hours >= working_hours_threshold_for_absent:
            self.status= 'Absent'












