<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    %for inv in objects :
    <% setLang(inv.partner_id.lang) %>
    <table class="dest_address">
        <tr><td >Foresatte til <b>${inv.partner_id.title or ''|entity}  ${inv.partner_id.name |entity}</b></td></tr>
        <tr><td>${inv.partner_id.street or ''|entity}</td></tr>
        <tr><td>${inv.partner_id.street2 or ''|entity}</td></tr>
        <tr><td>${inv.partner_id.zip or ''|entity} ${inv.partner_id.city or ''|entity}</td></tr>
        %if inv.partner_id.country_id :
        <tr><td>${inv.partner_id.country_id.name or ''|entity} </td></tr>
        %endif
        %if inv.partner_id.phone :
        <tr><td>${_("Tel")}: ${inv.partner_id.phone|entity}</td></tr>
        %endif
        %if inv.partner_id.fax :
        <tr><td>${_("Fax")}: ${inv.partner_id.fax|entity}</td></tr>
        %endif
        %if inv.partner_id.email :
        <tr><td>${_("E-mail")}: ${inv.partner_id.email|entity}</td></tr>
        %endif
        %if inv.partner_id.vat :
        <tr><td>${_("VAT")}: ${inv.partner_id.vat|entity}</td></tr>
        %endif
    </table>

    <% taxes = False %>

    <br />
    %if inv.type == 'out_invoice' :
    <span class="title">${_("Invoice")} ${inv.number or ''|entity}</span>
    %elif inv.type == 'in_invoice' :
    <span class="title">${_("Supplier Invoice")} ${inv.number or ''|entity}</span>   
    %elif inv.type == 'out_refund' :
    <span class="title">${_("Refund")} ${inv.number or ''|entity}</span> 
    %elif inv.type == 'in_refund' :
    <span class="title">${_("Supplier Refund")} ${inv.number or ''|entity}</span> 
    %endif
    <br/>
    <br/>
	<!-- I paavente av date_duue -->
	${_("Invoice Date")} : ${formatLang(inv.date_invoice, date=True)|entity}
	<br/>
<!--
    <table class="basic_table" width="90%">
        <tr><td>${_("Invoice Date")}</td><td>${_("Due Date")}</td></tr>
        <tr><td>${formatLang(inv.date_invoice, date=True)|entity}</td><td>${formatLang(inv.date_due, date=True) }</td></tr>
    </table> -->
    <h1><br /></h1>
    <table class="list_table"  width="90%">
        <thead><tr><th>${_("Description")}</th><th>${_("Unit Price")}</th><th >${_("Disc.(%)")}</th><th>${_("Price")}</th></tr></thead>
        %for line in inv.invoice_line :
        <tbody>
        <tr><td>${line.name|entity}</td><td style="text-align:right;">${formatLang(line.price_unit)}</td><td  style="text-align:center;">${line.discount or 0.00}</td><td style="text-align:right;">${formatLang(line.price_subtotal)}</td></tr>
        %if line.product_id :
            %if line.product_id.membership :
                <tr><td>${ formatLang(line.product_id.membership_date_from, date=True) } til ${ formatLang(line.product_id.membership_date_to, date=True) }</td></tr>
            %endif
        %endif

        %endfor
        %if taxes :
        <tr><td style="border-style:none"/><td style="border-style:none"/><td style="border-style:none"/><td style="border-style:none"/><td style="border-top:2px solid"><b>Net Total:</b></td><td style="border-top:2px solid;text-align:right">${formatLang(inv.amount_untaxed)}</td></tr>
        <tr><td style="border-style:none"/><td style="border-style:none"/><td style="border-style:none"/><td style="border-style:none"/><td style="border-style:none"><b>Taxes:</b></td><td style="text-align:right">${formatLang(inv.amount_tax)}</td></tr>
        %endif
        <tr><td style="border-style:none"/><td style="border-style:none"/><td style="border-style:none"/><td style="border-style:none"/><td style="border-top:2px solid"><b>Total:</b></td><td style="border-top:2px solid;text-align:right">${formatLang(inv.amount_total)}</td></tr>
        </tbody>
    </table>

    %if taxes :
    <table class="list_table" width="40%">
        <tr><th>Tax</th><th>${_("Base")}</th><th>${_("Amount")}</th></tr>
       %if inv.tax_line :
        %for t in inv.tax_line :
        <tr>
            <td>${ t.name|entity } </td>
            <td>${ t.base|entity}</td>
            <td>${ formatLang(t.amount) }</td>
        </tr>
        %endfor
        %endif
        <tr>
            <td style="border-style:none"/>
            <td style="border-top:2px solid"><b>${_("Total")}</b></td>
            <td style="border-top:2px solid">${ formatLang(inv.amount_tax) }</td>
        </tr>
    </table>
    %endif
    <p style="page-break-after:always"></p>
    %endfor
</body>
</html>
