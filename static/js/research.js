
function getMoreDocuments(){
    $.getJSON($SCRIPT_ROOT + '/_more_research', "",
        function(documents){
            for (i = 0; i < documents.length; i++) {
                document.getElementById("research_documents").innerHTML += "<a href="+$SCRIPT_ROOT+"/_download_research/" + String(documents[i]) + " >"+ String(documents[i]) + "</a><br>";
            }

        }
    );
}


function filter_search(){

}

