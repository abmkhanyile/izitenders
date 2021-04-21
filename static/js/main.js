$(document).ready(function () {

    // $('#subscribeCallModal').on('shown.bs.modal', function () {
    //     $('#subscribeCallModal').trigger('focus')
    //   })

          //pagination feautre for all the data tables.
            $('.tenders_table').simplePagination({
                perPage:30,
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

        // $(".cat_outer_container").niceScroll(".cats_container",{cursorcolor:"aquamarine"});


        //auto complete ajax code.
    keywordArr = [];

        $('.keywordInput').autocomplete({
            source: function(request, response ){
                if(request.term.length >= 3){
                    $.ajax({
                        url: "/user_accounts/auto_complete_search/",
                        type: 'POST',
                        data: {
                            'search_text': request.term,
                            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                        },
                        success: function(data){
                            $('.keywordsList').empty();
                            if(data != ""){
                                $('.keywordsList').append('<li><label class="keywordLabel" style="font-size: 12px; font-family: Helvetica;"><input id="selectAll" type="checkbox"><span><i><b>SELECT ALL</b></i></span></label></li>');
                                var dataArr = [];
                                var tempHolder = '';

                                $.each(data, function(i, jsonObj){
                                            keyword_pk = jsonObj.pk;
                                            keyword = jsonObj.fields.keyword;
                                            $('.keywordsList').append('<li><label class="keywordLabel" style="font-size: 12px; font-family: Helvetica; color: red;"><input type="checkbox" class="keywordCheckbox" data-keyword_pk="'+keyword_pk+'" data-keyword="'+keyword+'" />'+keyword+'</label></li>');
                                        });

                                response([]);
                            }
                            else{
                                response([]);
                            }
                        },
                        dataType: 'json'
                    });
                }
                else{
                    $('.keywordsList').empty();
                    response([]);
                }
            }
        });


         $('.keywordsList').on('click', '#selectAll', function(event){
            if(this.checked == true){
                $('.keywordCheckbox').each(function(){ this.checked = true; });
            }
            else{
                $('.keywordCheckbox').each(function(){ this.checked = false; });
            }
        });

        function get_keywords(){
            var kw_container = []
            if($('.addedKeywordsList li').length > 0){
                $('.keywordsAdded').each(function(event){
                    kw_container.push($(this).attr('data-keyword_pk'))
                });

                kw_str = kw_container.toString()
                $('.keywordListItem').val(kw_str);
            }
            else{
                kw_str = kw_container.toString()
                $('.keywordListItem').val(kw_str);
            }
        }


        //on click event handler for the Add button between the two container divs.
        $('.addingBtn').on('click', function(){
            $('.keywordCheckbox').each(function(event){
                if(this.checked == true){
                    var keyword_pk_obj = $(this).attr('data-keyword_pk');
                    var keyword_obj = $(this).attr('data-keyword');
                    $(this).closest("li").remove();
                    $('.addedKeywordsList').append('<li><label class="keywordLabel" style="font-size: 12px; font-family: Helvetica; color: green;"><input type="checkbox" name="addedKeywords" class="keywordsAdded" value="'+keyword_pk_obj+'" data-keyword_pk="'+keyword_pk_obj+'" data-keyword="'+keyword_obj+'">'+keyword_obj+'</label></li>');
                }

            });


        });

        //function below handles the remove btn event for the keywords.
        $('.removeBtn').on('click', function(){
            $('.keywordsAdded').each(function(event){
                if(this.checked == true){
                    var data_pk = $(this).attr('data-keyword_pk');
                    var data_keyword = $(this).attr('data-keyword');
                    $('.keywordsList').append('<li><label class="keywordLabel" style="font-size: 12px; font-family: Helvetica; color: red;"><input type="checkbox" class="keywordCheckbox" data-keyword_pk="'+data_pk+'" data-keyword="'+data_keyword+'" />'+data_keyword+'</label></li>')
                    $(this).closest("li").remove();
                }
            });


        });


        // selects all the chosen keywords for removal. 
        $('.selectAllChosen_kw').on('click', function(event){
            if(this.checked == true){
                $('.keywordsAdded').each(function(){ this.checked = true; });
            }
            else{
                $('.keywordsAdded').each(function(){ this.checked = false; });
            }
        });

        $('.saveProfBtn').on('click', function(){
            get_keywords()
        });


});
