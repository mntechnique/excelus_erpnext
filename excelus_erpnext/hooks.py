from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "excelus_erpnext"
app_title = "Excelus ERPNext"
app_publisher = "MN Technique"
app_description = "Excelus Customizations for ERPNext"
app_icon = "octicon octicon-diff-modified"
app_color = "scarlet"
app_email = "support@mntechnique.com"
app_license = "GPL v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/excelus_erpnext/css/excelus_erpnext.css"
# app_include_js = "/assets/excelus_erpnext/js/excelus_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/excelus_erpnext/css/excelus_erpnext.css"
# web_include_js = "/assets/excelus_erpnext/js/excelus_erpnext.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#   "Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "excelus_erpnext.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "excelus_erpnext.install.before_install"
# after_install = "excelus_erpnext.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "excelus_erpnext.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#   "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#   "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "BOM": {
        "validate": "excelus_erpnext.api.excelus_bom_validate",
    },
    "Purchase Order" : {
    	"autoname": "excelus_erpnext.api.po_autoname"
    },
    "Purchase Receipt" : {
    	"autoname": "excelus_erpnext.api.pr_autoname"
    },
    "Supplier Quotation" : {
    	"autoname": "excelus_erpnext.api.sqtn_autoname"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#   "all": [
#       "excelus_erpnext.tasks.all"
#   ],
#   "daily": [
#       "excelus_erpnext.tasks.daily"
#   ],
#   "hourly": [
#       "excelus_erpnext.tasks.hourly"
#   ],
#   "weekly": [
#       "excelus_erpnext.tasks.weekly"
#   ]
#   "monthly": [
#       "excelus_erpnext.tasks.monthly"
#   ]
# }

# Testing
# -------

# before_tests = "excelus_erpnext.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
#   "frappe.desk.doctype.event.event.get_events": "excelus_erpnext.event.get_events"
# }

fixtures = [
	{"dt": "Custom Script", "filters":[["name", "in", ['Item-client', 'BOM-client']]]},
	{"dt":"Custom Field", "filters":[["name", "in", [
			"Item-excelus_pm_length_uom","Item-cb_excelus_item_details_02","Item-sb_excelus_details_01",
			"Item-excelus_pm_thickness_uom","Item-excelus_pm_thickness","Item-cb_excelus_item_dtls_01",
			"Item-excelus_packs_per_carton","Item-excelus_pm_wastage","Item-excelus_pm_height_uom",
			"Item-excelus_pm_height","Item-excelus_pm_width_uom","Item-excelus_pm_width",
			"Item-excelus_pm_fold_bleed_uom","Item-excelus_pm_fold_bleed","Item-excelus_pm_flap_bleed_uom",
			"Item-excelus_pm_flap_bleed","Item-excelus_tape_bleed_uom","Item-excelus_tape_bleed",
			"Item-excelus_pm_length","Item-excelus_conversion_cost","Item-sb_excelus_item_details",
			"Item-excelus_price_details","Item-mrp_rate","Item-hsm_code","Item-column_break_item",
			"Item-abetment_rate","BOM Item-excelus_item_group",
			"Customer-customer_tax_details","Customer-vat_no","Customer-cst_no","Customer-excise_no",
			"Customer-service_tax_no","Customer-column_break_tax","Customer-gst_no","Customer-ifsc_no",
			"Customer-account_no","Customer-pan_no",
			"Supplier-supplier_tax_details","Supplier-vat_no","Supplier-cst_no","Supplier-excise_no",
			"Supplier-service_tax_no","Supplier-column_break_supplier_tax","Supplier-gst_no",
			"Supplier-ifsc_no","Supplier-account_no",
			"Purchase Receipt-excelus_pr_no",
			"Sales Invoice-excelus_transporter_details",
			"Sales Invoice-mode_of_transport",
			"Sales Invoice-vehicle_no",
			"Sales Invoice-cb_transporter_details",
			"Sales Invoice-date_and_time_of_supply",
			"Sales Invoice-place_of_supply"
	]]]},
	{"dt": "Print Format", "filters":[["name", "in", ["Excelus Production Order", "Excelus GST Sales Invoice"]]]}
]