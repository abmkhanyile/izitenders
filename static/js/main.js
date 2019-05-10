$(document).ready(function () {

          //pagination feautre for all the data tables.
            $('.tenders_table').simplePagination({
                perPage:15,
                previousButtonClass: "btn btn-primary btn-sm",
                nextButtonClass: "btn btn-primary btn-sm"
            });


        //this is for styling the select field for Provinces
        $('#provinces').multiselect({
            buttonWidth: '100%',
            nonSelectedText: 'Please Select Your Provinces',
            includeSelectAllOption: true,
            maxHeight: 300
        });

        //this is for styling the select field for Categories
        $('#catSelect').multiselect({
            buttonWidth: '100%',
            nonSelectedText: 'Please Select Your Industry',
            maxHeight: 300
        });
});
