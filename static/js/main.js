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

        //styles the search form dropdwon list in the Tenders.html page.
        $('#searchRegion').multiselect({
            buttonWidth: '100%',
            nonSelectedText: 'Select Province(s)',
            includeSelectAllOption: true,
            maxHeight: 300
        });

        //styles the search form drop down list for tender categories.
        $('#searchCategory').multiselect({
            buttonWidth: '100%',
            nonSelectedText: 'Select Category(s)',
            includeSelectAllOption: true,
            maxHeight: 300
        });
});
