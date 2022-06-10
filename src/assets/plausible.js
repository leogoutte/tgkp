var header = document.getElementsByTagName("head")[0]        
var plausible = document.createElement("script");
var domain_name = window.location.hostname;
var rollup_name = "plausible-rollup.materialscloud.org";
plausible.async = "";
plausible.defer = "";
plausible.dataset["domain"] = domain_name + "," + rollup_name;
plausible.src = "https://plausible.io/js/plausible.js";
header.appendChild(plausible);
