
function getMoreDocuments(number){
    $.getJSON($SCRIPT_ROOT + '/_more_research', "",
        function(documents){
            for (i = 0; i < number && i < documents.length; i++) {
                document.getElementById("research_documents").innerHTML +=
                    "<a href=" + $SCRIPT_ROOT + "/_download_research/" + String(documents[i]['filename']) + " ><figure class='research-main'> "
                    + "<div class='research-title'><h3>"+documents[i]['title']+ "</h3></div>" +
                    "<div class='research-filename'>"+documents[i]['filename'] + "</div>" +
                    "<div class='research-abstract'>"+documents[i]['abstract'] + "</div>" +
                    "</figure></a><br>";
            }

        }
    );
}


function filter_search(){

}

