# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ExcelusItemParameters(Document):
	

	def on_update(self):
		x = frappe.get_doc("Item",self.item)
		x.excelus_pm_length = self.length
		x.excelus_pm_width = self.width
		x.excelus_pm_height = self.height
		x.excelus_pm_thickness = self.thickness
		x.excelus_pm_fold_bleed = self.fold_bleed
		x.excelus_pm_flap_bleed = self.flap_bleed
		x.excelus_tape_bleed = self.tape_bleed
		x.excelus_packs_per_carton = self.packs_per_carton
		x.excelus_pm_length_uom = self.length_uom
		x.excelus_pm_width_uom = self.width_uom
		x.excelus_pm_height_uom = self.height_uom
		x.excelus_pm_thickness_uom = self.thickness_uom
		x.excelus_pm_fold_bleed_uom = self.fold_bleed_uom
		x.excelus_pm_flap_bleed_uom = self.flap_bleed_uom
		x.excelus_tape_bleed_uom = self.tape_bleed_uom
		x.excelus_conversion_cost = self.conversion_cost
		x.excelus_pm_wastage = self.wastage
		x.mrp_rate = self.mrp_rate
		x.hsm_code = self.hsm_code
		x.abetment_rate = self.abatement_rate

		x.save()
		frappe.db.commit() 

		# y = frappe.get_all("Item", filters={"farm":farm.name})			




