$(document).ready(function() {
    var book_id = $('#bookId').val();

    $('.mybtn').each(function(){ 
        if (book_id !='' && book_id !=$(this).attr('id')){
            $(this).prop('disabled', true).css({'background':'black', 'color':'white'});
        }
    });
    
    $('.mybtn').click(function($this) {
        var btn_id = $(this).attr('id');
        var path = $('#editBookForm').attr('action');
        
        if (book_id ==''){
            var selectedRow = (this).parentElement.parentElement;
            var numOfCells = selectedRow.cells.length;
            
            $('#id_title').val(selectedRow.cells[0].innerHTML);

            if (numOfCells == 7){
                var date = selectedRow.cells[3].innerHTML;
            }

            else {
                var date = selectedRow.cells[2].innerHTML;
            }
            
            date = date.split("/").reverse().join("-");
            $('#id_pub_date').val(date);

            $('#rstEditBook').click(function() {
                $('#id_title').val(selectedRow.cells[0].innerHTML);
                $('#id_pub_date').val(date); 
            });

            $('#editBookForm').attr('action', function(i, origValue){
                return origValue + btn_id;
            });  
            
            $('.btn-close').click(function() {
                $('#editBookForm').attr('action', function(i, origValue){
                    return path; 
                }); 
            });
        }

        else {
            $('#rstEditBook').click(function() {
                $('#editBookForm').trigger('reset');
            });

            $('.btn-close').click(function() { 
                $('#editBookForm').trigger('reset');
            });
        }   
    });
}); 