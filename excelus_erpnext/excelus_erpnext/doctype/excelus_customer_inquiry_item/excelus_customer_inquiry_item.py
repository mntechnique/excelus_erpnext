# -*- coding: utf-8 -*-
# Copyright (c) 2015, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ExcelusCustomerInquiryItem(Document):
    def validate(self):
        self.validate_ci_item()

    def validate_ci_item(self):
        if self.customer_rate >= 0.0:
            if not rate_form == "Customer" & customer_rate==0.0:
                frappe.throw(_("Customer Rate should be greater than zero."))
        else:
            frappe.throw(_("Customer Rate should not be less than zero."))
