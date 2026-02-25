function changeSortingHeaders(sortHeader, sortOrder) {
    $('.sorting-icon').each(function() {
        $(this).attr('class', 'bi bi-funnel sorting-icon');
    })
    var headerToChange = sortHeader.find('.sorting-icon');

    if (sortOrder == "ascending") {
        headerToChange.attr('class', 'bi bi-sort-up sorting-icon');
    } else {
        headerToChange.attr('class', 'bi bi-sort-down sorting-icon');
    }

    return;
}

function sortColumn(wrapperDiv, sortOrder, columnToSort) {
    let rows = $('.document-wrapper').get();

    rows.sort(function(a, b) {
        if (columnToSort == ".payment-amount .payment-amount-number" || columnToSort == ".document-name .invoice-id") {
            var keyA = parseInt($(a).find(columnToSort).text());
            var keyB = parseInt($(b).find(columnToSort).text());
        
        } else if (columnToSort == ".document-date") {
            var keyA = Date.parse($(a).find(columnToSort).text());
            var keyB = Date.parse($(b).find(columnToSort).text());
        } else {
            var keyA = $(a).find(columnToSort).text().toUpperCase();
            var keyB = $(b).find(columnToSort).text().toUpperCase();
        }
      
        if (sortOrder == "ascending") {
            if (keyA < keyB) return -1;
            if (keyA > keyB) return 1;
            return 0;
        } else {
            if (keyA > keyB) return -1;
            if (keyA < keyB) return 1;
            return 0;
        }
    });

    $.each(rows, function(i, row) {
        wrapperDiv.append(row); 
      });
}

document.addEventListener("DOMContentLoaded", function(event) {
    let wrapperDiv = $('#allDocuments');
    var columnToSort;
    var sortInvoiceType = "ascending";

    $(document).on('click', '.sort-button', function() {
        const id = this.id;
        switch(id) {
            case 'dealIDSort':
                columnToSort = ".document-name .invoice-id";
                break;
            case 'invoiceTypeSort':
                columnToSort = ".invoice-type";
                break;
            case 'statusTypeSort':
                columnToSort = ".payment-status .payment-status-text";
                break;
            case 'dateIssuedSort':
                columnToSort = ".document-date";
                break;
            case 'amountSort':
                columnToSort = ".payment-amount .payment-amount-number";
                break;
            
            default:
                console.log("Unknown ID");
        }

        if (sortInvoiceType == "ascending") {
            sortInvoiceType = "descending";
            changeSortingHeaders($(this), sortInvoiceType);
            sortColumn(wrapperDiv, sortInvoiceType, columnToSort);
        } else {
            sortInvoiceType = "ascending";
            changeSortingHeaders($(this), sortInvoiceType);
            sortColumn(wrapperDiv, sortInvoiceType, columnToSort);
        }

    })
});
