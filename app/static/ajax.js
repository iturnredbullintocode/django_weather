



    
function post_ajax_request(data_to_send, target_element, target_url) {

    // only proceed if target_element exists and target_url returns true
    if (target_element.get(0) && target_url) {

        console.log(target_element);
        console.log(target_url); 
    
        var xmlhttp;
        if (window.XMLHttpRequest) xmlhttp = new XMLHttpRequest(); 
        else xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");

        xmlhttp.onreadystatechange=function()  {

            // if successful response, show the template content
            if (xmlhttp.readyState==4 && xmlhttp.status==200) {
                target_element.html(xmlhttp.responseText);
            }

            // if we got a 500 error or other errors?
            else if (xmlhttp.readyState==4) {
                target_element.html(xmlhttp.responseText);
            }

            // if no successful response yet, show loading image
            else {
                if ($(target_element).has('.loading_img').length<1) { 
                     $('<object type="image/svg+xml" data="/static/polls/images/loading.svg" class="loading_img login"></object>').appendTo(target_element);   } 
            }

            // re-apply the button submission functionality
            apply_events();

         } //-- end onreadystatechange

        
        console.log("target_url="+target_url);
        console.log("data_to_send="+data_to_send); 

        xmlhttp.open("POST", target_url, true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.send(data_to_send); 

    }
    else {
        console.log(target_element);
        console.log(target_url);    }
        


} //-- end function post_ajax_request