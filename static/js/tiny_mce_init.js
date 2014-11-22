tinymce.init({
    selector: "textarea",
    theme: "modern",

    height:375,

        plugins: [
        "advlist autolink lists link image charmap print preview hr anchor pagebreak",
        "searchreplace wordcount visualblocks visualchars code fullscreen",
        "insertdatetime media nonbreaking save table contextmenu directionality",
        "emoticons template paste textcolor colorpicker textpattern",
        "spellchecker"
    ],
            theme_advanced_buttons3_add : "spellchecker",
        spellchecker_languages : "+English=en",

    toolbar1: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | spellchecker",
        image_advtab: true,
    templates: [
        {title: 'Meeting Notes Template', content: '<ul><li>&#160;DATE:</li><li>&#160;ATTENDEES:</li></ul><h2>WEATHER</h2><ul><li>&#160;</li></ul><h2>BACKGROUND / REFERENCE:</h2><ul><li>&#160;</li></ul><h2>NOTES</h2><ul><li>&#160;</li><li>&#160;</li></ul><h2>ACTION ITEMS FOR ME:</h2><ul><li>&#160;</li></ul><h2>ACTION ITEMS FOR OTHERS:</h2><ul><li>&#160;</li></ul><p>&nbsp;</p>'},
    ]
});
