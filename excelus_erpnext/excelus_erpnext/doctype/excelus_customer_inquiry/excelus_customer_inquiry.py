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
        self.validate_ci_requirements()

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

            #Set item group in items
            item_group = frappe.db.get_value("Item", item.item, "item_group")
            if item.item_group != item_group:
                item.item_group = item_group

    def validate_ci_requirements(self):
        for req in self.ci_requirements:
            bom_workflow_state = frappe.db.get_value("BOM", req.get("bom"), "workflow_state")
            if bom_workflow_state != "Approved":
                frappe.throw(_("Row #{0}: Please select an approved BOM. Current status: {1}".format(req.get('idx'), bom_workflow_state)))



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
        else:
            bom_workflow_state = frappe.db.get_value("BOM", item.get("bom"), "workflow_state")
            if bom_workflow_state != "Approved":
                frappe.throw(_("Row #{0}: Please select an approved BOM. Current status: {1}".format(item.get('idx'), bom_workflow_state)))

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

@frappe.whitelist()
def get_high_and_low_rates(ci_items):
    import json
    ci_items = json.loads(ci_items)

    out = []

    ci_item_codes = [x.item_code for x in ci_items]

    # #Fetch SQ Items for all item codes
    # sqi_items = frappe.get_all("Supplier Quotation Item", filters=[["item_code", "in", ci_item_codes]], fields=["parent", "item_code", "rate"])
    
    #     sqi_items_for_ci_item = [x for x in sqi_items if x.item_code == item.item_code]

    for item in ci_items:
        sqi_items = frappe.get_all("Supplier Quotation Item", filters=[["item_code", "=", item.item_code]], fields=["parent", "item_code", "rate"])
        


