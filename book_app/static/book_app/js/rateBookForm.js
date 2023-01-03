$(document).ready(function() {
    $('.mybtn').click(function() {
        var btn_id = $(this).attr('id');
        var path = $('#rateBookForm').attr('action');

        $('#rateBookForm').attr('action', function(i, origValue){
            return origValue + btn_id;
        });  

        $('.btn-close').click(function() {
            $('input[name="stars"]').prop('checked', false);
            
            $('#rateBookForm').attr('action', function(i, origValue){
                return path; 
            }); 
        }); 
    });
}); 