$(document).ready(function(){

    StarNote(1);

});




function StarNote(article_id){
$.ajax({
    type: "POST",
    url: "/ajax/star/",
    dataType: "json",
    data: { "note-star": article_id },
    success: function(data) {
        alert("Starred");
    }
});
}
