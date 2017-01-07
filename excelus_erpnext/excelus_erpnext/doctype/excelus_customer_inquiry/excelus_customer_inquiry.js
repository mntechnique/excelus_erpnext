// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt

frappe.ui.form.on('Excelus Customer Inquiry', {
	refresh: function(frm) {
		cur_frm.set_query("item", "ci_requirements", function() {
            return {
               filters: [
    				['Item', 'item_group', '=', 'Products']
    		   ]
            };
        });
        frm.add_custom_button(__("Fetch Items"), function(){
            /*var req_items = [];
            var req = frm.doc.ci_requirements;
            for (var i = req.length - 1; i >= 0; i--) {
                req_items.push(req[i].item);
            }*/
            frm.set_value("ci_items", []);
            frappe.call({
                method: "excelus_erpnext.excelus_erpnext.doctype.excelus_customer_inquiry.excelus_customer_inquiry.calculate_fetch_item",
                //method: "calculate_fetch_item",
                args: {
                    "req_items": frm.doc.ci_requirements
                },
                callback: function(r, rt) {
                    if(r.message) {
                        frm.clear_table("ci_items");
                        $.each(r.message, function(i, d) {
                        var c = frm.add_child("ci_items");
                        c.item = d.item_code;
                        c.qty = d.qty;
                        c.uom = d.stock_uom;
                        });
                    }
                    refresh_field("ci_items");
                    frm.layout.refresh_sections();
                }
            });
        });
        frm.add_custom_button(__("PDF"), function() {
            //console.log(frm.doc.items);
            var requirements = [];

            $.each(cur_frm.doc.ci_requirements, function(key, value){
                requirements.push(value.name);
            });

            var w = window.open("/api/method/excelus_erpnext.ci_print.print_ci?"
                +"ci_name=" + cur_frm.doc.name + "&requirements="+encodeURIComponent(requirements));

            if(!w) {
                frappe.msgprint(__("Please enable pop-ups")); return;
            }
        },__("Print Cost Sheet"));
        //  frm.add_custom_button(__("PDF"), function() {
        //     //console.log(frm.doc.items);
        //    frappe.call({
        //         method: "excelus_erpnext.api.print_pdf",
        //         //method: "calculate_fetch_item",
        //         args: {
        //             "ci_requirements": frm.doc.ci_requirements
        //         },
        //         callback: function(r, rt) {
        //             msgprint(r);
        //         }
        // },__("Export"));
        // frm.add_custom_button(__("Fetch Rates"), function(){
            
        //     frappe.call({
        //         method: "excelus_erpnext.excelus_erpnext.doctype.excelus_customer_inquiry.excelus_customer_inquiry.fetch_rates",
        //         //method: "calculate_fetch_item",
        //         args: {
        //             "ci_items": frm.doc.ci_items
        //         },
        //         callback: function(r, rt) {
        //             if(r.message) {
        //                 $.each(r.message, function(i, d) {
        //                     var c = frm.doc.ci_requirements.prototype.filter()
        //                     c.item = d.item_code;
        //                     c.qty = d.qty;
        //                     c.uom = d.stock_uom;
        //                 });
        //             }
        //             refresh_field("ci_items");
        //             frm.layout.refresh_sections();
        //         }
        //     });
        // });
	}
});

cur_frm.add_fetch("item" ,"default_bom","bom")

/*frappe.ui.form.on("Excelus Customer Inquiry Item", "customer_rate", function(frm, cdt, cdn) {
    for (var i = frm.doc.ci_items.length - 1; i >= 0; i--) {
        if(ci_items[i.frm.doc.customer_rate] <= 0){
            frappe.msgprint("customer rate should be greater than zero ");
        }
    }
});

*/