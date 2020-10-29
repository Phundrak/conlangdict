var divContent = null;
var prevScrollPos = 0;
var pos = 75;
var ribbonElems = null;

function hideRibbon() {
    if (divContent == null) {
        divContent = document.getElementsByClassName("content")[0];
        prevScrollPos = divContent.scrollTop;
        ribbonElems = [
            document.getElementsByClassName("ribbon-nav")[0],
            document.getElementsByClassName("ribbon-searchbar")[0],
            document.getElementsByClassName("ribbon-user-account")[0]
        ];
        if (divContent == null) {
            return;
        }
    }
    var currentScrollPos = divContent.scrollTop;
    var diff_scroll = prevScrollPos - currentScrollPos;
    pos = diff_scroll + pos;
    if (pos < 0) {
        pos = 0;
    } else if (pos > 75) {
        pos = 75;
    }
    console.log("diff", diff_scroll);
    console.log("pos", pos);
    document.getElementsByTagName("body")[0].style.gridTemplateRows = pos + "px auto";

    var yOffset = pos * 2 - 150;
    console.log(yOffset);

    ribbonElems.forEach(function(element) {
        element.style.marginTop = yOffset + "px";
    });

    document.getElementById("language-select").style.marginTop = (yOffset + 20) + "px";
    prevScrollPos = currentScrollPos;
}
