# -*- coding: utf-8 -*-
# Copyright (c) 2015, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ExcelusCustomerInquiry(Document):
	pass


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