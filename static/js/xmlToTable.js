 function parseXML(val) {
                if (document.implementation && document.implementation.createDocument) {
                    xmlDoc = new DOMParser().parseFromString(val, 'text/xml');
                }
                else if (window.ActiveXObject) {
                    xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
                    xmlDoc.loadXML(val);
                }
                else
                {
                    alert("Your browser can't handle this script");
                    return null;
                }
                return xmlDoc;
            }

function ConvertToTable(xmlDoc)
{
var table = '<br> <br> <table class="tg">'
//create table header with variable names

var vars = xmlDoc.getElementsByTagName('variable');
table += '<tr>'
for(var i = 0; i < vars.length; i++) {
    table += '<th class="tg-9hbo">'+ vars[i].getAttribute('name') +'</th>'
}
table += '</tr>'


//create table content
var results = xmlDoc.getElementsByTagName('result');
for(var i = 0; i < results.length; i++) {
table += '<tr>'
//for every binding generate cell
	var bindings = results[i].getElementsByTagName('binding');
  for(var b = 0; b < bindings.length; b++){
	    table += '<td class="tg-yw4l">'+ bindings[b].textContent +'</td>'  
  }

table += '</tr>'
}

table += '</table>'
return table;
}

