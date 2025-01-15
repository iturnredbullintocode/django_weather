function expand_next(element) {
    if (element.nextElementSibling.style.display=='block') {
        element.nextElementSibling.style.display='none';     }
    else {
        element.nextElementSibling.style.display='block';    }
}//--/end function expand_next