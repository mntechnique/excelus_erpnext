# -*- coding: utf-8 -*-
# Copyright (c) 2015, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ExcelusCustomerInquiry(Document):
    def validate(self):
        self.validate_ci_item()

    def validate_ci_item(self):
        items_without_rate_from = [x for x in self.ci_items if x.rate_from == ""]
        if len(items_without_rate_from) > 0:
            frappe.throw(_("Please set 'Rate From' in all items."))


        #items_rate_from_customer = [x for x in self.ci_items if x.rate_from = "Customer"]
        count = 1
        for item in self.ci_items:
            # if item.rate_from == "Customer" and item.customer_rate:
            if item.customer_rate >= 0:
                if not item.rate_from == "Customer" and item.customer_rate==0 :
                    frappe.throw(_("Customer Rate should be greater than zero at row " + str(count) +" item: {0}. Beacuse Rate from is other than customer. ").format(item.item))
            else:
                frappe.throw(_("Customer Rate should not be less than zero."))
            count = count+1


@frappe.whitelist()
def calculate_fetch_item(req_items):
    #final_item list created for result to fetch into ci_items table
    final_items = []
    import json
    #req_items_js load ci_requiremnt input like item_code, qty and bom list.
    req_items_js = json.loads(req_items)
    for item in req_items_js:
        # throws error message if default bom not selected for item.
        if not item.get('bom'):
            frappe.throw(_("Please select BOM for all requirement Items"))
        bom_items = frappe.db.get_all("BOM Item", filters={"parent":item.get('bom')}, fields=["*"])

        #Calculate (bom item qty / bom qty) * input ci_requirment qty. Addition does becasue of duplicate item in bom.
        for bom_item in bom_items:
            found_item = [x for x in final_items if x.item_code==bom_item.item_code]
            qty_ratio = bom_item.qty / frappe.db.get_value("BOM", item.get("bom"), "quantity")
            if len(found_item)==1:
                found_item[0].qty += float(qty_ratio) * (float(item.get("qty_kg")) or 1.0)
            else:
                bom_item["qty"] = float(qty_ratio) * (float(item.get("qty_kg")) or 1.0)
                final_items.append(bom_item)

    # for i in final_items:

    return final_items

